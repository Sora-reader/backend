from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.login.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    def get_token(self) -> dict:
        refresh = RefreshToken.for_user(self.instance)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    class Meta:
        model = Profile
        fields = ("username", "password")

    def create(self, validated_data):
        self.instance = Profile.objects.create_user(**validated_data)
        return self.instance
