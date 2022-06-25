from .base import *

# esta es para mysql
DEBUG = True
ALLOWED_HOSTS = ['ekiriatest.herokuapp.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd3b89n552k778a',
        'USER': 'rcskocaksnkrso',
        'PASSWORD': '690bc2558a6cf8313324ea8ffe7483a74e9f3d452b9bbd9bcd2e0351e3265055',
        'HOST': 'ec2-34-200-35-222.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS  = (os.path.join(BASE_DIR, '../static/'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'../media')

LOGIN_URL = "/IniciarSesion/"
LOGIN_REDIRECT_URL = 'Inicio'
LOGOUT_REDIRECT_URL = '/'