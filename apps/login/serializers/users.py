from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    def get_token(self) -> dict:
        refresh = RefreshToken.for_user(self.instance)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        self.instance = User.objects.create_user(**validated_data)
        return self.instance


class UserTokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    username = serializers.CharField()


class UserTokenRequestSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["username"] = self.user.get_username()

        return data
