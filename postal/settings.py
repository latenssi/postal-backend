import os

def str2bool(v):
  return str(v).lower() in ("yes", "true", "t", "1")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = str2bool(os.environ.get('POSTAL_DEBUG', False))

# Security settings
# SESSION_COOKIE_SECURE = True  # Can only be used when using HTTPS
# CSRF_COOKIE_SECURE = True  # Can only be used when using HTTPS
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ALLOWED_HOSTS = os.getenv('POSTAL_ALLOWED_HOSTS', '').split()

SECRET_KEY = os.getenv('POSTAL_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_ENV_POSTGRES_DB', 'postgres'),
        'USER': os.getenv('POSTGRES_ENV_POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_ENV_POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('POSTGRES_PORT_5432_TCP_ADDR', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT_5432_TCP_PORT', '5432')
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': os.getenv('MEMCACHED_PORT_11211_TCP_ADDR', '127.0.0.1'),
    }
}

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

    # 3rd party
	'rest_framework',
    'taggit',
    'taggit_serializer',
    'sorl.thumbnail',
	'corsheaders',

    # Own
    'postal.posts'
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'postal.urls'

WSGI_APPLICATION = 'postal.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = os.getenv('POSTAL_LANGUAGE_CODE', 'en-us')

USE_I18N = False

USE_L10N = False

USE_TZ = True

TIME_ZONE = os.getenv('POSTAL_TIME_ZONE', 'Europe/Helsinki')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = os.getenv('POSTAL_STATIC_URL', '/static/')
STATIC_ROOT = os.environ.get('POSTAL_STATIC_ROOT', os.path.join(BASE_DIR, 'static'))

MEDIA_URL = os.getenv('POSTAL_MEDIA_URL', '/media/')
MEDIA_ROOT = os.environ.get('POSTAL_MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] [%(name)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        }
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '10000/day'
    }
}

CORS_ALLOW_CREDENTIALS = str2bool(os.environ.get('CORS_ALLOW_CREDENTIALS', True))
CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST', '').split()

try:
	from local_settings import *
except ImportError:
	pass

CORS_ORIGIN_ALLOW_ALL = DEBUG
