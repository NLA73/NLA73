import os
from dotenv import load_dotenv
from pathlib import Path

# 1. Alamat Folder Proyek
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Keamanan (Isi random aja kalau buat belajar)
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ['*']

# 3. Daftar Aplikasi
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app', # Aplikasi kamu
]

# 4. Satpam (Middleware) - URUTAN WAJIB SAMA
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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

load_dotenv()
# 7. KONEKSI MYSQL (Ganti sesuai Workbench kamu)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'app_db', # Ganti nama DB kamu
        'USER': 'root',
        'PASSWORD': os.getenv('DB_PASSWORD'), # Ganti password kamu
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# 8. Bahasa & Waktu
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 9. File Statis (CSS/JS)
# --- BAGIAN STATIC ---
STATIC_URL = '/static/'

# WAJIB TAMBAH INI supaya folder static di luar app kebaca
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Kasih tahu Django jangan pakai User standar, tapi pakai buatan Nathan
AUTH_USER_MODEL = 'app.User'