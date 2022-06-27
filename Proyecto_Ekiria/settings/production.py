from .base import *

# esta es para mysql
DEBUG = True
ALLOWED_HOSTS = ['ekiriatest.herokuapp.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sql10502612',
        'USER': 'sql10502612',
        'PASSWORD': 'usDS2My7PZ',
        'HOST': 'sql10.freemysqlhosting.net',
        'PORT': '3306',
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