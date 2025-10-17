from django.db import models
from django.conf import settings
from apps.films.models import Film

class Thumb(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='thumbs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_good = models.BooleanField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Memastikan satu user hanya bisa memberikan satu thumb per film
        unique_together = ('user', 'film')