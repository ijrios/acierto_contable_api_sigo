from .base import *
from dotenv import load_dotenv
import os
load_dotenv()

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME_DATABASE'),
        'USER': os.getenv('USER_DATABASE'),
        'PASSWORD': os.getenv('PASS_DATABASE'),
        'HOST': os.getenv('HOST_DATABASE'),
        'PORT': os.getenv('PORT_DATABASE'),
    }
}

STATIC_URL = 'static/'