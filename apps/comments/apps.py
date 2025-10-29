from django.apps import AppConfig
import joblib
import os
from django.conf import settings
import nltk # <-- Tambahkan import

class CommentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.comments'

    # Path ke file model di dalam container Docker
    # settings.BASE_DIR menunjuk ke /app
    model_path = os.path.join(settings.BASE_DIR, 'models', 'sentiment_model.joblib')
    vectorizer_path = os.path.join(settings.BASE_DIR, 'models', 'tfidf_vectorizer.joblib')

    model = None
    vectorizer = None

    def ready(self):
        """Kode ini dijalankan saat Django siap."""
        print("⏳ Memuat model ML...")
        try:
            CommentsConfig.model = joblib.load(CommentsConfig.model_path)
            CommentsConfig.vectorizer = joblib.load(CommentsConfig.vectorizer_path)
            print("✅ Model dan vectorizer berhasil dimuat.")
            
            # Download NLTK data jika belum ada
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                print("⬇️ Mendownload NLTK stopwords...")
                nltk.download('stopwords', quiet=True) # quiet=True agar tidak verbose
                print("👍 NLTK stopwords siap.")
                
        except FileNotFoundError:
            print(f"❌ Error: File model tidak ditemukan di {CommentsConfig.model_path} atau {CommentsConfig.vectorizer_path}")
        except Exception as e:
            print(f"❌ Error saat memuat model: {e}")