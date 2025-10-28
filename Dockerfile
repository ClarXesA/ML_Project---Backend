FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# --- OPTIMIZATION ---
# 1. Copy ONLY requirements.txt first
COPY requirements.txt /app/

# 2. Install dependencies (this layer gets cached)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 3. Download NLTK data after installing nltk
RUN python -m nltk.downloader stopwords
# --- END OPTIMIZATION ---

# 4. NOW copy the rest of your project code
COPY . /app/