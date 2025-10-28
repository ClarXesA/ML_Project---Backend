import joblib
import re
import nltk 
from nltk.corpus import stopwords
import os
from django.conf import settings
from googletrans import Translator # <-- Impor Translator
from .apps import CommentsConfig # <-- Impor model yang sudah dimuat

# --- Fungsi Preprocessing (Tetap Sama) ---
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        stop_words = set() 
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

# --- Instansiasi Translator (di luar fungsi agar efisien) ---
translator = Translator()

# --- FUNGSI BARU UNTUK TERJEMAHAN ---
def translate_to_english(text: str) -> str:
    """
    Mendeteksi bahasa teks dan menerjemahkannya ke Bahasa Inggris 
    jika perlu. Mengembalikan teks asli jika sudah Bahasa Inggris 
    atau jika terjadi error.
    """
    try:
        detected_lang = translator.detect(text).lang
        if detected_lang != 'en':
            print(f"🔄 Menerjemahkan dari '{detected_lang}' ke 'en': '{text}'")
            translated_text = translator.translate(text, src=detected_lang, dest='en').text
            print(f"   Hasil: '{translated_text}'")
            return translated_text
        else:
            # Teks sudah Bahasa Inggris
            return text
    except Exception as e:
        print(f"⚠️ Warning: Gagal menerjemahkan teks '{text}'. Error: {e}")
        # Jika terjemahan gagal, kembalikan teks asli saja
        return text 
# --- AKHIR FUNGSI TERJEMAHAN ---


def predict_sentiment(text: str) -> bool | None:
    """
    Menerjemahkan teks ke Bahasa Inggris, melakukan preprocessing, 
    lalu memprediksi sentimen menggunakan model yang sudah dimuat.
    """
    try:
        # 1. Terjemahkan teks ke Bahasa Inggris
        english_text = translate_to_english(text)
        
        # 2. Preprocess teks (yang sudah pasti Inggris)
        processed_text = preprocess_text(english_text)
        
        # 3. Vectorize teks
        vectorized_text = CommentsConfig.vectorizer.transform([processed_text])
        
        # 4. Prediksi
        prediction = CommentsConfig.model.predict(vectorized_text)[0] 
        
        # 5. Konversi ke Boolean (True=Positif, False=Negatif)
        return prediction.upper() == 'POSITIVE'

    except Exception as e:
        print(f"❌ Error predicting sentiment: {e}")
        return None