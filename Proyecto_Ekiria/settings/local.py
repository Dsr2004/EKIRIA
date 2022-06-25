from .base import *

# esta es para mysql
ALLOWED_HOSTS = []
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_ekiria',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',
            'charset': 'utf8mb4',
        }
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS  = (os.path.join(BASE_DIR, '../static/'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'../media')

LOGIN_URL = "/IniciarSesion/"
LOGIN_REDIRECT_URL = 'Inicio'
LOGOUT_REDIRECT_URL = '/'