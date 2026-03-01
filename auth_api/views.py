from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)

        return Response({"message": "User created"})


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        login(request, user)   # ✅ CRITICAL LINE

        return Response({
            "message": "Login successful",
            "username": user.username
        })

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        user = request.user

        user.email = request.data.get("email", user.email)
        user.phone_number = request.data.get("phone_number", user.phone_number)

        user.save()

        return Response(UserSerializer(user).data)