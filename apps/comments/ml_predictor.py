import joblib
import re
import nltk 
from nltk.corpus import stopwords
import os
from django.conf import settings
from googletrans import Translator
from .apps import CommentsConfig

# --- Fungsi Preprocessing ---
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

# --- Instansiasi Translator ---
translator = Translator()

# --- Fungsi Terjemahan ---
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

# --- Fungsi Prediksi ---
def predict_sentiment_from_processed(processed_text: str) -> bool | None:
    """
    HANYA melakukan prediksi dari teks yang SUDAH di-preprocess.
    """
    try:
        # 1. Vectorize teks
        vectorized_text = CommentsConfig.vectorizer.transform([processed_text])
        
        # 2. Prediksi
        prediction = CommentsConfig.model.predict(vectorized_text)[0] 
        
        # 3. Konversi ke Boolean
        return prediction.upper() == 'POSITIVE'

    except Exception as e:
        print(f"❌ Error predicting sentiment: {e}")
        return None