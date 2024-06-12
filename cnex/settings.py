"""
Django settings for cnex project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from myconfig.env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [host for host in os.getenv('ALLOWED_HOSTS').split(',') if host != '']

# Application definition

INSTALLED_APPS = [
    'daphne',
    # 'admin_interface',
    # "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'accounts',
    'variations',
    'products',
    'coupon',
    'order',
    'payment',
    'appointment',
    'compaign',
    'deliverycharge',
    'reviewrating',
    'accountsmanagement',
    'notification',
]

ASGI_APPLICATION = 'cnex.asgi.application'


AUTH_USER_MODEL = "accounts.CustomUser" 

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    # 'whitenoise.middleware.WhiteNoiseMiddleware',#for media,static serving dphane

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cnex.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'NAME': os.getenv('DATABASES_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'account.backend.EmailUserBackend'
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
import os

STATIC_URL = '/static/'
# ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [white for white in os.getenv('CORS_ORIGIN_WHITELIST').split(',') if white != '']
CSRF_TRUSTED_ORIGINS = [trusted for trusted in os.getenv('CSRF_TRUSTED_ORIGINS').split(',') if trusted != '']

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=600),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
}


# EMAIL_USE_TLS = True
# EMAIL_HOST = os.getenv('smtp.gmail.com')
# EMAIL_PORT = os.getenv('EMAIL_PORT')
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
# EMAIL_HOST_USER = 'manojdas.py@gmail.com'
EMAIL_HOST_USER="info@cnex.com.np"
# EMAIL_HOST_PASSWORD = 'snhz riaw dfjl mncb'
EMAIL_HOST_PASSWORD = "fpsg yspd yalp wpwu"

SMS_KEY_PASSWORD = os.getenv('SMS_KEY_PASSWORD')

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': os.getenv('REDIS_CACHE_LOCATION'),  # Update with your Redis server details
#         'KEY_PREFIX': os.getenv('REDIS_CACHE_KEY_PREFIX'),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'MASTER_NAME': 'mymaster_cnex_local',
#         }
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

APPLE_CLIENT_ID = "com.vrit.cnex"
APPLE_TEAM_ID = "X3TZ8A2M5B"
APPLE_PRIVATE_KEY="""-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgtS7Qxob1z7AZ1j4DoIe9pHL/1YR/XtJPrIjc3S0yIkugCgYIKoZIzj0DAQehRANCAAR02UUVvKxiiL1C4+2mc6c5d5jbt4qJYnxVVBeVoZ5Fa1alcWtUzuEFkIBC9EuyBv0B6UkLjxT3/oLeqSpSYFe/
-----END PRIVATE KEY----"""

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB, for POST forms
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB, for file uploads



# settings.py

# Import required modules
import os
from storages.backends.s3boto3 import S3Boto3Storage

# Set AWS credentials
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

# Set custom domain for static and media files (Optional)
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Static files (CSS, JavaScript, images)
STATICFILES_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
STATICFILES_STORAGE =  'cnex.custom_storage.StaticStorage'

# Media files (Uploaded files)
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
DEFAULT_FILE_STORAGE = 'cnex.custom_storage.MediaStorage'

AWS_DEFAULT_ACL = 'public-read'  # Set the default ACL for uploaded files to public-read


#ESEWA
ESEWA_MERCHANT_ID = os.getenv('ESEWA_MERCHANT_ID')
ESEWA_MERCHANT_SECRETE = os.getenv('ESEWA_MERCHANT_SECRETE')

#applelogin
# social auth for apple login
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_APPLE_ID_CLIENT = "com.vrittechnologies.cnex"
SOCIAL_AUTH_APPLE_ID_TEAM = "X3TZ8A2M5B"
SOCIAL_AUTH_APPLE_ID_KEY = "A342S53TXS"
SOCIAL_AUTH_APPLE_ID_SECRET = """
-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgfCRGSJVxXTXdUAx4
e9Fl55st5wnKHMNt+IMpwG+O2nWgCgYIKoZIzj0DAQehRANCAAQnkIQ2sHoE9slg
aL+QPW2zF+kOQdqXe8r/GDBDneS87sKf0futOQ7RVdR/BXBmpyJg/F1nzhLE0ps0
NfiR3GXO
-----END PRIVATE KEY-----"""
SOCIAL_AUTH_APPLE_PRIVATE_KEY = """
-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgfCRGSJVxXTXdUAx4
e9Fl55st5wnKHMNt+IMpwG+O2nWgCgYIKoZIzj0DAQehRANCAAQnkIQ2sHoE9slg
aL+QPW2zF+kOQdqXe8r/GDBDneS87sKf0futOQ7RVdR/BXBmpyJg/F1nzhLE0ps0
NfiR3GXO
-----END PRIVATE KEY-----"""
SOCIAL_AUTH_APPLE_ID_SCOPE = ["email", "name"]
SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME = True

#ONE_SIGNAL_API
ONE_SIGNAL_API_KEY = os.getenv('ONE_SIGNAL_API_KEY')
APP_ID = os.getenv('APP_ID')