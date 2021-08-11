import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-_tykokhjkt6785pw#o693pf#1+*0(#dmop-tu'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ps_db',
        'USER': 'user_name',
        'PASSWORD': 'passqz9qz',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


ALLOWED_HOSTS = ['*']

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
