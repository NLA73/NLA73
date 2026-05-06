import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# 1. Alamat Folder Proyek
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Keamanan (Isi random aja kalau buat belajar)
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-ganti-ini')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']  # Biarkan sementara agar mudah akses
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'https://*.ngrok-free.dev',
    'https://*.lhr.life',
    'https://*.pythonanywhere.com',
    'https://*.railway.app',       # Domain Railway
    'https://*.up.railway.app',    # Domain Railway (format baru)
]

# 3. Daftar Aplikasi
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'app',
]

# 4. Satpam (Middleware) - URUTAN WAJIB SAMA
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 5. Pintu Utama URL
ROOT_URLCONF = 'app_project.urls'

# 6. Mesin Template HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app_project.wsgi.application'


# 7. KONEKSI DATABASE
# Kalau ada DATABASE_URL dari Railway, pakai itu. Kalau tidak, pakai SQLite lokal.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'
    )
}

# 8. Bahasa & Waktu
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 9. File Statis (CSS/JS)
STATIC_URL = '/static/'

# Lokasi folder static asli di project kamu
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Folder tempat Django mengumpulkan semua file statis saat dideploy
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Mengaktifkan kompresi dan caching otomatis (biar web lebih kencang)
# Django 6.0 pakai STORAGES, bukan STATICFILES_STORAGE
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Supaya WhiteNoise tidak crash kalau ada file static yang belum ke-collect
WHITENOISE_MANIFEST_STRICT = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Kasih tahu Django jangan pakai User standar, tapi pakai buatan Nathan
AUTH_USER_MODEL = 'app.User'