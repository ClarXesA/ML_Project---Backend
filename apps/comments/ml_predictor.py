import joblib
import re
import nltk # <-- Tambahkan import nltk
from nltk.corpus import stopwords
import os
from django.conf import settings

# --- SALIN FUNGSI INI DARI tes_model.py ---
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        # Kita akan handle download stopwords di Dockerfile
        # Jika masih gagal, setidaknya tidak crash
        stop_words = set() 
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)
# --- AKHIR FUNGSI PREPROCESSING ---

# Impor model yang akan dimuat dari apps.py
from .apps import CommentsConfig

def predict_sentiment(text: str) -> bool | None:
    """
    Memprediksi sentimen menggunakan model yang sudah dimuat.
    """
    try:
        # 1. Preprocess teks (WAJIB SAMA DENGAN TRAINING)
        processed_text = preprocess_text(text)
        
        # 2. Vectorize teks
        vectorized_text = CommentsConfig.vectorizer.transform([processed_text])
        
        # 3. Prediksi
        # Asumsikan model Anda mengembalikan 'POSITIVE' atau 'NEGATIVE'
        prediction = CommentsConfig.model.predict(vectorized_text)[0] 
        
        # 4. Konversi ke Boolean (True=Positif, False=Negatif)
        return prediction.upper() == 'POSITIVE'

    except Exception as e:
        print(f"❌ Error predicting sentiment: {e}")
        return None