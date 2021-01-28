"""
Django settings for hth project.

For more information on this file, see:
https://docs.djangoproject.com/en/dev/topics/settings/
https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

For the full list of settings and their values, see:
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import environ
import sys

project_root = environ.Path(__file__) - 2
src_root = project_root.path('hth')

env = environ.Env(
    DEBUG=(bool, False),
    TESTING=(bool, 'pytest' in sys.argv[0]),
)
env.read_env()

DEBUG = env('DEBUG')
TESTING = env('TESTING')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'cloudinary',
    'embed_video',

    'hth.core',
    'hth.news',
    'hth.shows',
    'hth.music',
]

MIDDLEWARE_CLASSES = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar.apps.DebugToolbarConfig',
    ]

    MIDDLEWARE_CLASSES = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
     ] + MIDDLEWARE_CLASSES

ROOT_URLCONF = 'hth.urls'

WSGI_APPLICATION = 'hth.wsgi.application'


# Database & Cache
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# https://docs.djangoproject.com/en/dev/ref/settings/#caches

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': src_root('jahhills.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'M j, Y'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = project_root('staticfiles')
STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#django.contrib.staticfiles.storage.ManifestStaticFilesStorage.manifest_strict
    # https://stackoverflow.com/a/58299776/3188289
    if not TESTING else
    'django.contrib.staticfiles.storage.StaticFilesStorage'
)
STATICFILES_DIRS = [
    src_root('static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = project_root('media')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            src_root('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]


# Email

vars().update(env.email_url())

ADMINS = [
    ('Brian', 'bhrutledge@gmail.com'),
]

DEFAULT_FROM_EMAIL = 'band@hallelujahthehills.com'
SERVER_EMAIL = env('SERVER_EMAIL')


# Security

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = [] if DEBUG else [
    '127.0.0.1',
    'localhost',
    '.debugged.org',
    '.hallelujahthehills.com',
]


# App settings

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}
