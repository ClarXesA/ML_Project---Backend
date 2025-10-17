from rest_framework import viewsets, permissions
from .models import Film
from .serializers import FilmSerializer
from apps.users.permissions import IsAdminOrReadOnly # <-- Impor izin kustom kita

class FilmViewSet(viewsets.ModelViewSet):
    """
    API endpoint yang memungkinkan Film untuk dilihat atau diedit (oleh admin).
    """
    queryset = Film.objects.all().order_by('-created_at') # Tampilkan film terbaru dulu
    serializer_class = FilmSerializer
    
    # Terapkan aturan izin:
    # 1. IsAuthenticatedOrReadOnly: User harus login untuk mengubah data.
    # 2. IsAdminOrReadOnly: DAN user juga harus admin untuk mengubah data.
    # (Kita bisa pakai IsAdminOrReadOnly saja karena sudah mencakup kasus GET)
    permission_classes = [IsAdminOrReadOnly]