from .base import *  # noqa

# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

ALLOWED_HOSTS = [
    'localhost',
    '.debugged.org',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
