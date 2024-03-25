from .base import *

# Production-specific settings
DEBUG = False

# Add production-specific settings here
DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
