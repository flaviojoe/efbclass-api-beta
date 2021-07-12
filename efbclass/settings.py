import os
from pathlib import Path

import environ
from corsheaders.defaults import default_headers
from django.conf.locale.pt_BR import formats

BASE_DIR = Path(__file__).resolve().parent.parent

# Lendo configurações do .env
env = environ.Env(DEBUG=(bool, False))
# env_file = os.path.join(BASE_DIR, ".env.exemplo")
env_file = os.path.join(BASE_DIR, ".env.dev")
environ.Env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
DEBUG_TOOLBAR = env.bool('DEBUG_TOOLBAR', default=False)
DB_POSTGRESQL = env.bool('DB_POSTGRESQL', default=False)
REDIS_CACHE = env.bool('REDIS_CACHE', default=False)
STORAGE_S3 = env.bool('STORAGE_S3', default=False)
VIMEO_HABILITADO = env.bool('VIMEO_HABILITADO', default=False)
RESTFRAMEWORK_NAVEGADOR_API = env.bool('RESTFRAMEWORK_NAVEGADOR_API', default=False)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # Admin

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Pip
    'rest_framework',
    'rest_framework.authtoken',
    'knox',
    'corsheaders',
    'django_filters',
    'nested_inline',
    'widget_tweaks',
    # 's3upload',

    # apps
    'empresas',
    'contas',
    'cursos',
    'materiais',
    'alunos',
    'faqs',
    'questionarios',
    'notificacoes',
    'configuracoes',
    'core',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'middleware.current_user.CurrentUserMiddleware',
]

ROOT_URLCONF = 'efbclass.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'efbclass.wsgi.application'

# Database
if DB_POSTGRESQL:
    DATABASES = {
        "default": {
            "ENGINE": env("SQL_ENGINE"),
            "NAME": env("SQL_DATABASE"),
            "USER": env("SQL_USER"),
            "PASSWORD": env("SQL_PASSWORD"),
            "HOST": env("SQL_HOST"),
            "PORT": env("SQL_PORT"),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

LOCALE_NAME = 'pt_BR'

LANGUAGE_CODE = 'pt-br'

# Locale PT_BR Formatos
formats.DATETIME_FORMAT = 'd/m/Y'

TIME_ZONE = 'America/Belem'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    'content-disposition',
]

# Django Rest Framework
AUTHENTICATION_BACKENDS = [
    'knox.auth.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
    'django.contrib.auth.backends.ModelBackend'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'django.contrib.auth.backends.ModelBackend'
    ],
    'DATETIME_FORMAT': "%m/%d/%Y %H:%M:%S",
    'SEARCH_PARAM': 'filter',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

if not RESTFRAMEWORK_NAVEGADOR_API:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',),

# Django Debug Toolbar
if DEBUG and DEBUG_TOOLBAR:
    INSTALLED_APPS.insert(5, 'debug_toolbar', )
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Django Storage
# if DEBUG:
#     DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

FILE_UPLOAD_MAX_MEMORY_SIZE = 429916160
DATA_UPLOAD_MAX_MEMORY_SIZE = 429916160

# Vimeo API
if VIMEO_HABILITADO:
    VIMEO_CLIENT_ID = env('VIMEO_KEY')
    VIMEO_CLIENT_SECRET = env('VIMEO_SECRET')
    VIMEO_ACCESS_TOKEN = env('VIMEO_ACCESS_TOKEN')
    VIMEO_CACHE_BACKEND = 'default'

# Redis Django-Redis
# if REDIS_CACHE:
#     CACHES = {
#         "default": {
#             "BACKEND": "django_redis.cache.RedisCache",
#             "LOCATION": "redis://127.0.0.1:6379/1",
#             "OPTIONS": {
#                         "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             },
#             "KEY_PREFIX": "efbclass"
#         }
#     }
#     SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
#     SESSION_CACHE_ALIAS = 'default'


# S3
if STORAGE_S3:
    # print('Entrou em STORAGE_S3')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    # AWS_QUERYSTRING_AUTH = False
    # S3_USE_SIGV4 = True
    # AWS_S3_SIGNATURE_VERSION = 's3v4'
    # S3UPLOAD_REGION = 'us-west-1'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# Autenticacao
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = 'logout'