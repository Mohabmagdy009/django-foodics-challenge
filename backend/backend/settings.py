"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
# region Imports
from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
# endregion

# Load environment variables from .env.dev file
load_dotenv()

# -------------------------------------------------------------------
# Base Directory and Paths
# -------------------------------------------------------------------
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# region Security -------------------------------------------------------------------
# -------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = ['*']
CORS_ALLOW_CREDENTIALS = True
# endregion

# region Installed Applications -------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',

    # Third-party apps
    'django_extensions',  # For dev tools like shell_plus
    'corsheaders',  # Cross-Origin Resource Sharing (CORS)
    'rest_framework',  # Django REST framework
    'rest_framework_simplejwt',
    'drf_spectacular',  # Swagger Documentation
    'safedelete',  # Safe Delete DRF

    # Your apps
    'utils',
    'inventory'
]
# endregion

# region Middleware -------------------------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# endregion

# region Django REST Framework Configuration -------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'utils.endpointhandling.exception_handler.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
# endregion

# -------------------------------------------------------------------
# URL Configuration
# -------------------------------------------------------------------
ROOT_URLCONF = 'backend.urls'

#  region Template Configuration -------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
# endregion

# -------------------------------------------------------------------
# WSGI Application
# -------------------------------------------------------------------
WSGI_APPLICATION = 'backend.wsgi.application'

# -------------------------------------------------------------------
# Database Configuration
# -------------------------------------------------------------------
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------------------------------------------------
# Spectacular Swagger Settings
# -------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your API',
    'DESCRIPTION': 'Description of your API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SECURITY': [
        {
            'BearerAuth': []
        }
    ],
    'COMPONENT_SPLIT_REQUEST': True,
}

# -------------------------------------------------------------------
# Password Validation
# -------------------------------------------------------------------
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------------------
# Internationalization
# -------------------------------------------------------------------
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False

# -------------------------------------------------------------------
# CORS Configuration
# -------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# -------------------------------------------------------------------
# Security Settings
# -------------------------------------------------------------------
CSRF_COOKIE_SECURE = True

# -------------------------------------------------------------------
# Static and Media Files
# -------------------------------------------------------------------
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -------------------------------------------------------------------
# Default Auto Field
# -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------------
# Custom User Model
# -------------------------------------------------------------------
AUTH_USER_MODEL = 'utils.User'

# -------------------------------------------------------------------
# Shell Plus (django-extensions)
# -------------------------------------------------------------------
SHELL_PLUS = "ipython"

# region Logging Configuration -------------------------------------------------------------------
os.makedirs('logs', exist_ok=True)
LOG_FILE = os.path.join(BASE_DIR, 'logs/django.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO' if DEBUG else 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO' if DEBUG else 'DEBUG',
            'propagate': True,
        },
    }
}
# endregion

# region JWT Token Configuration (SIMPLE_JWT)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=3),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
}
# endregion

# region Email Configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL')  # Your email address
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # Your email password
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL')
