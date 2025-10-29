from rest_framework import generics, permissions # <-- Add 'generics'
from rest_framework import viewsets
from .models import Comment, Film # <-- Add 'Film'
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating and listing ALL comments.
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# --- ADD THIS NEW VIEW ---
class FilmCommentListView(generics.ListAPIView):
    """
    API endpoint to list comments for a specific film.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny] # Anyone can view comments

    def get_queryset(self):
        """
        Filter comments based on the 'film_pk' URL parameter.
        """
        # Get the film ID from the URL (e.g., /api/films/5/comments/)
        film_id = self.kwargs['film_pk'] 
        # Return only comments related to that film
        return Comment.objects.filter(film_id=film_id).order_by('-created_at')
# --- END OF NEW VIEW ---