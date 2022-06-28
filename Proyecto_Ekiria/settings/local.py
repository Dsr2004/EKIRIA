from .base import *

# esta es para mysql
Domain = "127.0.0.1:8000"
ALLOWED_HOSTS = []
DEBUG = True
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'db_ekiria',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '',
#         'OPTIONS': {
#             'init_command': 'SET default_storage_engine=INNODB',
#             'charset': 'utf8mb4',
#         }
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS  = (os.path.join(BASE_DIR, '../static/'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'../media')

LOGIN_URL = "/IniciarSesion/"
LOGIN_REDIRECT_URL = 'Inicio'
LOGOUT_REDIRECT_URL = '/'