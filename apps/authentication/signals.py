from allauth.account.utils import perform_login
from allauth.socialaccount.signals import pre_social_login
from allauth.utils import get_user_model
from django.conf import settings
from django.dispatch import receiver

from apps.authentication.utils import redirect_with_cookie


@receiver(pre_social_login)
def pre_social_login_handler(request, sociallogin, *args, **kwargs):
    """
    Take email out and try to find user with the same email
    If the user exists, verify email if needed, login and redirect to home
    """
    email_address = sociallogin.account.extra_data["email"]
    user_model = get_user_model()
    users = user_model.objects.filter(email=email_address)
    if users:
        user = users[0]

        email_addrs = sociallogin.email_addresses
        if email_addrs:
            addr = sociallogin.email_addresses[0]
            # Verify if needed
            if not addr.verified:
                addr.verified = True
                addr.save()

        # allauth.account.app_settings.EmailVerificationMethod
        perform_login(request, user, email_verification=settings.ACCOUNT_EMAIL_VERIFICATION)

        redirect_with_cookie(request)
