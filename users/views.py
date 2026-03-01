from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserMeSerializer
from core.authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication


# ✅ REGISTER
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# ✅ LOGIN (TOKEN BASED)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def post(self, request):
        mobile = request.data.get("mobile")
        password = request.data.get("password")

        user = authenticate(username=mobile, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful",
            "token": token.key
        })


# ✅ LOGOUT
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # delete token
        return Response(
            {"message": "Successfully logged out"},
            status=status.HTTP_200_OK
        )


# ✅ PROFILE (GET + UPDATE)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)