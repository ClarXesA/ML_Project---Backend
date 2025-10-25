from rest_framework import serializers
from .models import Comment
from .ml_predictor import predict_sentiment # <-- Impor placeholder ML kita

class CommentSerializer(serializers.ModelSerializer):
    # Tampilkan 'fullname' user, bukan cuma ID-nya
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        # Tentukan field yang akan dipakai
        fields = ('id', 'film', 'user', 'comment', 'is_good', 'created_at')
        
        # Field ini tidak boleh diisi manual oleh user
        read_only_fields = ('user', 'is_good', 'created_at')

    def create(self, validated_data):
        """
        Timpa metode create standar.
        """
        # 1. Ambil teks komentar dari data yang sudah divalidasi
        comment_text = validated_data.get('comment')
        
        # 2. Panggil fungsi model ML kita
        sentiment_result = predict_sentiment(comment_text)
        
        # 3. Tambahkan hasil prediksi ke dalam data
        validated_data['is_good'] = sentiment_result
        
        # 4. Simpan komentar ke database
        comment = Comment.objects.create(**validated_data)
        return comment