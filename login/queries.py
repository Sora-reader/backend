from .models import Profile


class ProfileQueries:
    def create(username, password, email="no email"):
        return Profile.objects.create_user(username, email, password)
