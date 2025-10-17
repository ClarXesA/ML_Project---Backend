# 🎬 Backend API Analisis Sentimen Film

Ini adalah **backend API** untuk aplikasi *Analisis Sentimen Ulasan Film*.  
Proyek ini dibangun menggunakan **Django**, **Django REST Framework**, dan **PostgreSQL**.  
Seluruh lingkungan pengembangan dikonfigurasi menggunakan **Docker** dan **Docker Compose** untuk kemudahan setup.

---

## 💻 Teknologi yang Digunakan    

- **Backend**: Django & Django REST Framework  
- **Database**: PostgreSQL  
- **Autentikasi**: JWT (*djangorestframework-simplejwt*)  
- **Lingkungan**: Docker & Docker Compose


## ⚙️ Prasyarat

Sebelum memulai, pastikan Anda telah menginstal:

1. [Git](https://git-scm.com/downloads)  
2. [Docker Desktop](https://www.docker.com/products/docker-desktop/) *(termasuk Docker Compose)*

---

## 🚀 Instalasi & Setup

Ikuti langkah-langkah berikut untuk menjalankan proyek secara lokal.

### 1. Clone Repositori

```bash
git clone [URL-GIT-ANDA]
cd film_sentiment_back-end
```

---

### 2. Konfigurasi Environment (Wajib)

Proyek ini menggunakan file `.env` untuk menyimpan variabel lingkungan penting.

#### a. Salin File Template

Untuk **Mac/Linux**:

```bash
cp .env.example .env
```

Untuk **Windows (Command Prompt)**:

```bash
copy .env.example .env
```

#### b. Isi File `.env`

Buka file `.env` dengan teks editor, lalu isi variabel berikut:

```bash
# Database
POSTGRES_DB=film_db
POSTGRES_USER=film_user
POSTGRES_PASSWORD=MASUKKAN_PASSWORD_DB_AMAN_DI_SINI

# Django
SECRET_KEY=MASUKKAN_DJANGO_SECRET_KEY_ACAK_DI_SINI
DEBUG=True
```

### 3. Jalankan Docker

Pastikan Docker Desktop aktif, lalu jalankan perintah berikut.

#### a. Build & Jalankan Kontainer

```bash
docker-compose up --build -d
```

#### b. Jalankan Migrasi Database

```bash
docker-compose exec web python manage.py migrate
```

#### c. Buat Akun Admin

```bash
docker-compose exec web python manage.py createsuperuser
```

Masukkan email, nama lengkap, dan password sesuai petunjuk di terminal.

---

### 4. Selesai!

Proyek Anda sekarang **berjalan sepenuhnya!**

- 🚀 **Server API** → [http://localhost:8000/](http://localhost:8000/)  
- 🔑 **Admin Panel** → [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🛠️ Perintah Sehari-hari

Menyalakan proyek:

```bash
docker-compose up -d
```

Menghentikan proyek:

```bash
docker-compose down
```

Melihat log (debugging):

```bash
docker-compose logs -f web
```

> 💡 **Tips:**
> - Gunakan [Djecrety](https://djecrety.ir/) untuk membuat `SECRET_KEY` baru.  
> - `POSTGRES_PASSWORD` bisa diisi bebas, misal: `superaman123`.

## ⚛️ Panduan API untuk Frontend (React + TypeScript)

Berikut panduan singkat untuk mengonsumsi API ini dari aplikasi React.

---

### 1. Alur Autentikasi (JWT)

API menggunakan **Bearer Token** untuk autentikasi.

1. **Login** → Kirim `email` & `password` ke endpoint:  
   `/api/token/`
2. **Terima Token** → Server membalas dengan `access_token` & `refresh_token`
3. **Simpan Token** → Simpan `access_token` (misalnya di `localStorage`)
4. **Gunakan Token** → Setiap permintaan ke endpoint terproteksi harus menyertakan header:

```
Authorization: Bearer <access_token_anda>
```

---

### 2. Setup Axios (Rekomendasi)

Buat file `src/api/apiClient.ts`:

```ts
import axios from 'axios';

// Buat instance axios dengan baseURL
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Tambahkan interceptor untuk otomatis menambahkan token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;
```

---

### 3. Contoh Penggunaan API

#### a. Definisikan Tipe Data (`src/types/index.ts`)

```ts
export interface Film {
  id: number;
  title: string;
  cover_img_url: string;
  created_at: string;
}

export interface Comment {
  id: number;
  film: number;
  user: string; // fullname user
  comment: string;
  is_good: boolean;
  created_at: string;
}
```

#### b. Fetch Data Film (Tidak Perlu Login)

`src/services/filmService.ts`:

```ts
import apiClient from '../api/apiClient';
import { Film } from '../types';

// Mengambil semua film
export const getFilms = async (): Promise<Film[]> => {
  try {
    const response = await apiClient.get<Film[]>('/films/');
    return response.data;
  } catch (error) {
    console.error('Gagal mengambil data film:', error);
    throw error;
  }
};
```

#### c. Post Komentar (Perlu Login)

`src/services/commentService.ts`:

```ts
import apiClient from '../api/apiClient';
import { Comment } from '../types';

interface NewCommentData {
  film: number; // ID film yang dikomentari
  comment: string; // Isi komentar
}

// Mengirim komentar baru
export const postComment = async (data: NewCommentData): Promise<Comment> => {
  try {
    const response = await apiClient.post<Comment>('/comments/', data);
    return response.data;
  } catch (error) {
    console.error('Gagal mengirim komentar:', error);
    throw error;
  }
};
```
## 🧠 Catatan Tambahan

- Pastikan endpoint API di frontend sesuai dengan `baseURL` backend Anda.  
- Jika ingin mengganti port, sesuaikan di file `docker-compose.yml` dan `settings.py`.  
- Gunakan `DEBUG=False` untuk mode produksi.
- Selalu commit file `.env.example` saja — jangan pernah commit file `.env` asli ke repository publik.

---

✅ **Proyek Siap Digunakan!**  
Anda sekarang memiliki backend API Django yang siap diintegrasikan dengan aplikasi frontend React/TypeScript Anda.
