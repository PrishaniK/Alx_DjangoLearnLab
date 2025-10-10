from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "bio", "profile_picture", "profile_image")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = get_user_model().objects.create_user(  
            password=password, **validated_data
        )
        Token.objects.create(user=user) 
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs.get("username"), password=attrs.get("password"))
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        attrs["user"] = user
        return attrs

class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)

    class Meta:
        model = User
        fields = (
            "id", "username", "email", "bio", "profile_picture", "profile_image",
            "followers_count", "following_count"
        )
        read_only_fields = ("username", "email")