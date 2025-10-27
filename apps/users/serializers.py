from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer untuk registrasi user baru."""
    class Meta:
        model = User
        fields = ('fullname', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} # Password tidak akan ditampilkan

    def create(self, validated_data):
        # Memanggil create_user dari UserManager untuk hashing password
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    """Serializer untuk melihat/mengedit data profil user."""
    class Meta:
        model = User
        fields = ('id', 'email', 'fullname', 'created_at')
        read_only_fields = ('id', 'email', 'created_at')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer kustom untuk JWT untuk menambahkan data user ke payload token.
    """
    @classmethod
    def get_token(cls, user):
        # Ambil token bawaan
        token = super().get_token(user)

        # Tambahkan data kustom
        token['fullname'] = user.fullname
        token['email'] = user.email
        token['is_admin'] = user.is_admin

        return token