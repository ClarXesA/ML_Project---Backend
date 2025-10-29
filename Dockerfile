FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# --- TAMBAHAN UNTUK NLTK ---
RUN python -m nltk.downloader stopwords
# --- AKHIR TAMBAHAN ---

COPY . /app/