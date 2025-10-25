from rest_framework import serializers
from .models import Thumb

class ThumbSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Thumb
        fields = ('id', 'film', 'user', 'is_good')
        read_only_fields = ('user',)

    def create(self, validated_data):
        """
        Timpa metode create untuk menangani logika update-or-create.
        """
        # Ambil data user dan film dari data yang divalidasi
        user = validated_data.get('user')
        film = validated_data.get('film')
        is_good = validated_data.get('is_good')

        # Cari 'thumb' yang ada berdasarkan user dan film.
        # Jika tidak ada, 'defaults' akan digunakan untuk membuat yang baru.
        # Jika sudah ada, 'defaults' akan memperbaruinya.
        thumb, created = Thumb.objects.update_or_create(
            user=user,
            film=film,
            defaults={'is_good': is_good}
        )

        return thumb