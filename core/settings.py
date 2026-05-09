"""
Django settings for core project.
Developed by: Kelvin Chacha (Junior System Architect)
Project: Order System Backend API
Architecture: N-Tier with JWT Authentication
"""

from pathlib import Path
from datetime import timedelta

# --- Directory Configuration ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security Configuration ---
# WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o+*8y+wx@+k@1g=wfpsu)+#o*c$@vhl3+ei6)9j0jm%6hi!cfg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# --- Application Definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    
    # Third-party Packages
    'rest_framework',
    'rest_framework_simplejwt', # Kwa ajili ya Token-based Auth
    'corsheaders',             # Inaruhusu React Native kuvuta data
    'drf_spectacular', 
    'django_filters',       # Swagger Documentation
    
    # Internal Apps
    'users.apps.UsersConfig',                 # Identity & Access Management (Kelvin's App)
    'order',  
    'menu',    
    'payment',                        #   Business Logic App
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Lazima iwe juu ya CommonMiddleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', # Disabled for API focus
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# --- Database Configuration ---
# Using SQLite for development phase
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static Files ---
STATIC_URL = 'static/'

# --- CORS Configuration ---
CORS_ALLOW_ALL_ORIGINS = True  # Inaruhusu frontend yoyote kuvuta data
CORS_ALLOW_CREDENTIALS = True  # Inaruhusu tokens (muhimu kwa login)
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
CORS_ALLOW_HEADERS = [
    "accept", "accept-encoding", "authorization", "content-type",
    "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with",
]

# --- REST Framework Configuration ---
REST_FRAMEWORK = {
    # Swagger/OpenAPI Setup
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    # Centralized Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# --- Simple JWT Configuration (High Security Layer) ---
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Token inadumu saa 1
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Refresh inadumu siku 1
    'ROTATE_REFRESH_TOKENS': True,                  # Usalama zaidi: Token inabadilika ikitumiwa
    'AUTH_HEADER_TYPES': ('Bearer',),               # Standard header for React Native Axios
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# --- Swagger/Spectacular Settings ---
SPECTACULAR_SETTINGS = {
    'TITLE': 'aXeraf Technologies - Order API', # Rebranded to aXeraf
    'DESCRIPTION': 'Ramani ya API kwa ajili ya mfumo wa oda - Kelvin Chacha',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_PATCH': True,
}

# --- Custom User Model ---
# Overriding default Auth to use Phone Number via Kelvin's Architecture
AUTH_USER_MODEL = 'users.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'