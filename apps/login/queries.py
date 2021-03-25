from .models import Profile


class ProfileQueries:
    @staticmethod
    def create(username: str, password: str, email: str = "no email") -> Profile:
        return Profile.objects.create_user(username, email, password)
