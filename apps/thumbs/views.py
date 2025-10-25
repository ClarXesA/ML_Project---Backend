from rest_framework import viewsets, permissions
from .models import Thumb
from .serializers import ThumbSerializer

class ThumbViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk Thumbs (Like/Dislike).
    """
    queryset = Thumb.objects.all()
    serializer_class = ThumbSerializer
    permission_classes = [permissions.IsAuthenticated] # Wajib login

    # Kita batasi agar user tidak bisa 'update' atau 'delete' via ID
    # Logika 'update' sudah ditangani oleh Serializer.
    http_method_names = ['get', 'post', 'head', 'options']

    def perform_create(self, serializer):
        """
        Otomatis isi field 'user' dengan user yang sedang login.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        (Opsional) Filter agar user hanya melihat thumbs milik mereka sendiri.
        Jika Anda ingin semua user melihat semua like, hapus fungsi ini.
        """
        return self.queryset.filter(user=self.request.user)