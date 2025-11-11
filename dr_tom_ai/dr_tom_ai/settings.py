from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # load environment variables

# ------------------------------------------------
# 🔐 Security / Debug
# ------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key")  # Railway will store this
DEBUG = os.getenv("DEBUG", "False") == "True"

# Allow Railway domains + local dev
#ALLOWED_HOSTS = ['*', 'dr-tomai.up.railway.app']

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
CSRF_TRUSTED_ORIGINS = [
    "https://" + os.environ.get("RAILWAY_STATIC_URL", "dr-tomai.up.railway.app"),
]


# ------------------------------------------------
# 📦 Installed apps
# ------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'medical',
    'accounts',
    'widget_tweaks',
]

# ------------------------------------------------
# 🧱 Middleware
# ------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ add this for Railway static support
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dr_tom_ai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # templates folder
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

WSGI_APPLICATION = 'dr_tom_ai.wsgi.application'

# ------------------------------------------------
# 🗄️ Database (Railway auto-provides DATABASE_URL)
# ------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default="postgresql://postgres:$i3rv0T0m@db.prtvrkypphxtgkdcmbuo.supabase.co:5432/postgres",
        conn_max_age=600,
        ssl_require=True
    )
}


# ------------------------------------------------
# 🖼️ Static / Media
# ------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------
# 🌐 Security (for later production)
# ------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
]

# ------------------------------------------------
# 🔑 Authentication
# ------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'analyze'
LOGOUT_REDIRECT_URL = 'home'
