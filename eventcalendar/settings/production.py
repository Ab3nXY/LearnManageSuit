from .base import *

# Production-specific settings
DEBUG = False

# Add production-specific settings here
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME_PROD'),
        'USER': config('DB_USER_PROD'),
        'PASSWORD': config('DB_PASSWORD_PROD'),
        'HOST': config('DB_HOST_PROD'),
        'PORT': '5432',
    }
}
