"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0*t^^0^%9ijn*3b89nq$oi78vmozjei3@v(9#9!9k)6!06icc5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS = True

MSG_TYPE_MESSAGE = 0  # For standard messages
MSG_TYPE_WARNING = 1  # For yellow messages
MSG_TYPE_ALERT = 2  # For red & dangerous alerts
MSG_TYPE_MUTED = 3  # For just OK information that doesn't bother users
MSG_TYPE_ENTER = 4  # For just OK information that doesn't bother users
MSG_TYPE_LEAVE = 5  # For just OK information that doesn't bother users
MSG_TYPE_UPDATE = 6
MESSAGE_TYPES_CHOICES = (
    (MSG_TYPE_MESSAGE, 'MESSAGE'),
    (MSG_TYPE_WARNING, 'WARNING'),
    (MSG_TYPE_ALERT, 'ALERT'),
    (MSG_TYPE_MUTED, 'MUTED'),
    (MSG_TYPE_ENTER, 'ENTER'),
    (MSG_TYPE_LEAVE, 'LEAVE'),
)

MESSAGE_TYPES_LIST = [
    MSG_TYPE_MESSAGE,
    MSG_TYPE_WARNING,
    MSG_TYPE_ALERT,
    MSG_TYPE_MUTED,
    MSG_TYPE_ENTER,
    MSG_TYPE_LEAVE,
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #lib apps
    'corsheaders',
    'rest_framework',
    'django_extensions',
    'taggit',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework.authtoken',  # if you use the same token auth system as the example
    'social_django',

    # django social auth
    # custom apps
    'apps.users.apps.UsersConfig',
    'api.v1.apps.V1Config',
    'apps.blogs.apps.BlogsConfig',


]

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_UPLOAD_PATH ='uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
ROOT_URLCONF = 'config.urls'

from corsheaders.defaults import default_headers
CORS_ALLOW_HEADERS = default_headers + ('access-control-allow-origin', '*', 'charset', 'enctype')
CORS_ORIGIN_WHITELIST = [
    "https://analyticssteps.com",
    "http://127.0.0.1:8000"
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.routing.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/backend/static/'
STATIC_ROOT = os.path.dirname(BASE_DIR) + '/staticfiles/'
# STATIC_ROOT='static/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "data/")

# Setting abstract user as user
AUTH_USER_MODEL = 'users.User'
IMPORT_EXPORT_USE_TRANSACTIONS = True

# Authentication backends email and call back
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'libraries.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

MEDIA_URL = '/backend/media/'

CUSTOM_DIRS = {
    'BLOG_THUMB_DIR': 'blog-thumbnails',
    'BLOG_MEDIA': 'blog-media',
    'MAILERS_DIR': '',
    'CAREER_DIR': 'career',
    'USER_IMAGE': 'user-profile',
    'NEWS_DIR': 'news',
    'TESTIMONIAL_DIR': 'testimonials',
    'UPLOADED_BLOG': 'uploaded-blog',
    'THUMBNAIL_DIR': 'thumbnail',
    'THUMBNAIL_NEWS_DIR': 'news_thumbnail',
    'PROFILE_PIC_DIR': 'profile_pic',
    'UTILITY_IMAGE_DIR': 'utility_image',

}

# Rest framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=120),
    'GET_USER_SECRET_KEY': 'apps.users.models.get_global_login_token',
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'password',
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=30),
}



# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'




SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '185382870222-p1jilu2lciv65654vjt4tg7s53lu2287.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'xPpJEDHvqZIoQCH1LWJmZ8ai'


SOCIAL_AUTH_URL_NAMESPACE = 'social'


try:
    from .local_settings import *
except Exception as e:
    pass


