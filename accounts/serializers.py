from django.contrib.auth import get_user_model
from rest_framework import serializers
from .services import AccountService

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        style={'input_type': 'password'},
        label='password'
    )
    confirm_password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True,
        style={'input_type': 'password'},
        label='confirm password'
    )

    class Meta:
        model = User
        fields = (
            "email", "first_name",
            "last_name", "birth_date",
            "bio", "password",
            "confirm_password",
        )

    def create(self, validated_data):
        if AccountService.check_passwords_are_the_same(validated_data) is not True:
            raise serializers.ValidationError("Passwords don't match")
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email", "first_name",
            "last_name", "birth_date",
            "bio", "last_visit"
        )
