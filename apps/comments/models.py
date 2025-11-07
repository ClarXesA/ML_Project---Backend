from django.db import models
from django.conf import settings
from apps.films.models import Film

class Comment(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField() # Komentar asli
    
    # --- TAMBAHAN BARU ---
    # Field untuk menyimpan hasil terjemahan (jika ada)
    translated_comment = models.TextField(null=True, blank=True)
    # --- AKHIR TAMBAHAN ---
    
    is_good = models.BooleanField(null=True, blank=True) # Hasil sentimen
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)