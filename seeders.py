import os
import time 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Proyecto_Ekiria.settings")
import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.auth.models import Group
from Usuarios.models import *

django.setup()

def Roles():
    Roles = [{'id':'1','name':'Administrador'},{'id':'2', 'name':'Nivel 1'}]
    for rol in Roles:
        if Group.objects.filter(pk = rol['id']) :
            Group.objects.create(id = rol['id'], name  = rol['name'])
        print(roles)
Roles()