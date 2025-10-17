from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegistrationSerializer, UserSerializer
from .models import User

class UserRegisterView(generics.CreateAPIView):
    """View untuk mendaftarkan user baru."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # Izinkan siapa saja mendaftar

class ManageUserView(generics.RetrieveUpdateAPIView):
    """View untuk melihat dan mengedit profil user yang sedang login."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Selalu kembalikan profil user yang sedang login
        return self.request.user

class LogoutView(APIView):
    """View untuk logout (blacklist refresh token)."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)