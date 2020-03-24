from config.settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'django_test',
        'USER': 'saurabh',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '',
    }
}