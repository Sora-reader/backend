from .models import Profile


class ProfileQueries:
    @staticmethod
    def create(username: str, password: str, email: str = "no email") -> Profile:
        profile = Profile.objects.create_user(username, email)
        profile.set_password(password)
        profile.save()
