from rest_framework import serializers
from .models import User

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