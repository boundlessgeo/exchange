import os

from .base import *  # noqa

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.getenv('STATIC_ROOT',
                        os.path.join(BASE_DIR, "../.storage/static_root"))
MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(BASE_DIR,
                                                  "../.storage/media"))

# ensures tests are run on writing to file
AUDIT_TO_FILE = True

FILESERVICE_CONFIG = {
    'store_dir': os.path.join(MEDIA_ROOT, 'fileservice'),
    'types_allowed': ['.jpg', '.jpeg', '.png'],
    'streaming_supported': True
}

SECRET_KEY = os.getenv('SECRET_KEY', 'unit tests only not for production')
DEBUG = True
ALLOWED_HOSTS = ['testserver']
_INSTALLED_APPS = (
    'geonode',
    'exchange.core',
    'exchange.themes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
GEOQUERY_ENABLED = True
SOCIAL_BUTTONS = True
STORYSCAPES_ENABLED = True
ES_SEARCH = True
ENABLE_SOCIAL_LOGIN = True
GEOQUERY_URL = 'http://www.example.com'
NOMINATIM_ENABLED = False
