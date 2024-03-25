import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Set DJANGO_SETTINGS_MODULE to the value specified in .env file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv('DJANGO_SETTINGS_MODULE'))

application = get_wsgi_application()
