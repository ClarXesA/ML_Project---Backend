import joblib
import re
import nltk 
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
from django.conf import settings
from googletrans import Translator
from .apps import CommentsConfig

# Pastikan resource NLTK ada (penting untuk server/deployment)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    
try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')

# Inisialisasi satu kali saja
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


# --- Fungsi Preprocessing ---
def preprocess_text(text: str) -> str:
    """
    Fungsi untuk membersihkan dan memproses teks review:
    INI HARUS SAMA PERSIS DENGAN FUNGSI TRAINING.
    """
    # 1. Menghapus tag HTML
    text = re.sub(r'<[^>]+>', ' ', text)

    # 2. Lowercasing
    text = text.lower()

    # 3. Menghapus karakter selain huruf dan spasi
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # 4. Tokenisasi
    words = text.split()

    # 5. Lemmatization dan penghapusan stopwords
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]

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
    Mengembalikan True untuk 'POSITIVE', False untuk 'NEGATIVE', atau None jika ada error/neutral.
    """
    if not processed_text:
        # Menghindari error jika input kosong setelah preprocessing
        return None 
        
    try:
        # 1. Vectorize teks
        # Pastikan input adalah list/iterable meskipun hanya satu item
        vectorized_text = CommentsConfig.vectorizer.transform([processed_text])

        # 2. Pilih fitur menggunakan selector (WAJIB menggunakan selector yang sudah di-fit)
        selected_text = CommentsConfig.selector.transform(vectorized_text)
        
        # 3. Prediksi (mengembalikan array, ambil elemen pertama)
        prediction = CommentsConfig.model.predict(selected_text)

        print(prediction)
        
        # 4. Konversi ke Boolean
        if prediction == 'positive':
            return True
        elif prediction == 'negative':
            return False
        else:
            # Jika kelasnya 'NEUTRAL' atau kelas lain yang tidak di mapping
            return None 

    except Exception as e:
        print(f"❌ Error predicting sentiment: {e}")
        return None