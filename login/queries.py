from .models import Profile


class ProfileQueries:
    @staticmethod
    def create(username, password, email="no email"):
        return Profile.objects.create_user(username, email, password)
