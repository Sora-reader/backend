from allauth.exceptions import ImmediateHttpResponse
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect

from apps.core.api.schemas import ErrorSchema

frontend_url_key = "frontend_url"


def save_frontend_url(request):
    """Use this method in initial API view that starts auth process to later send a session."""
    # Save as http to allow it to work on localhost, production UI redirects to HTTPS by default
    url = request.POST["redirectUrl"]
    if any([url.startswith(o) for o in settings.CSRF_TRUSTED_ORIGINS]):
        request.session[frontend_url_key] = url
    else:
        return "Host is not in the trusted origins list."


def auto_save_frontend_url(f):
    """Just a view decorator to call save_frontend_url."""

    def wrapper(request, *args, **kwargs):
        if e := save_frontend_url(request):
            return HttpResponse(ErrorSchema(error=e).json(), status=400)
        return f(request, *args, **kwargs)

    return wrapper


def redirect_with_cookie(request):
    """Get host url and session from session and send session token via a redirect."""
    host = request.session[frontend_url_key]
    resp = redirect(f"{host}?t={request.session.session_key}")

    raise ImmediateHttpResponse(resp)
