from rest_framework import serializers
from .models import Comment
# Impor 3 fungsi spesifik dari ml_predictor
from .ml_predictor import translate_to_english, preprocess_text, predict_sentiment_from_processed

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    # Tampilkan field baru di respons API
    translated_comment = serializers.CharField(read_only=True) 

    class Meta:
        model = Comment
        # Tambahkan 'translated_comment' ke daftar fields
        fields = ('id', 'film', 'user', 'comment', 'translated_comment', 'is_good', 'created_at')
        read_only_fields = ('user', 'is_good', 'created_at', 'translated_comment')

    def create(self, validated_data):
        original_text = validated_data.get('comment')
        
        # 1. Terjemahkan
        translated_text = translate_to_english(original_text)
        
        # 2. Preprocess
        processed_text = preprocess_text(translated_text)
        
        # 3. Prediksi
        sentiment_result = predict_sentiment_from_processed(processed_text)
        
        # Tentukan apa yang akan disimpan di field terjemahan
        translated_to_store = None
        if original_text.lower() != translated_text.lower():
            # Hanya simpan jika teksnya benar-benar diterjemahkan
            translated_to_store = translated_text

        # 4. Simpan semuanya ke database
        comment_instance = Comment.objects.create(
            **validated_data, # (Berisi film, user, dan 'comment' asli)
            is_good = sentiment_result,
            translated_comment = translated_to_store # Simpan hasil terjemahan
        )
        
        return comment_instance