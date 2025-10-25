from rest_framework import viewsets, permissions
from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk melihat dan membuat komentar.
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    
    # Aturan izin:
    # Siapa saja boleh BACA (GET), tapi harus LOGIN untuk POST (nulis komentar)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Otomatis isi field 'user' dengan user yang sedang login saat POST.
        """
        serializer.save(user=self.request.user)