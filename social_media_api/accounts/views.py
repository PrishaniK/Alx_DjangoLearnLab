from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

User = get_user_model()

class RegisterView(APIView):
    """
    POST /register
    Body: {username, email, password, bio?, profile_picture?}
    Returns: {user, token}
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"user": ProfileSerializer(user).data, "token": token.key},
            status=status.HTTP_201_CREATED,
        )

class LoginView(APIView):
    """
    POST /login
    Body: {username, password}
    Returns: {user, token}
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"user": ProfileSerializer(user).data, "token": token.key})

class ProfileView(RetrieveUpdateAPIView):
    """
    GET /profile  -> current user profile
    PUT/PATCH /profile -> update bio/profile_picture
    Auth: Token
    """
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

