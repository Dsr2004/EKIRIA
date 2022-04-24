"""
WSGI config for Proyecto_Ekiria project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import time
from tokenize import group 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Proyecto_Ekiria.settings")
import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
# --------------------------------Import models------------------------------
from django.contrib.auth.models import Group
from Usuarios.models import *
from Ventas.models import *
# ---------------------------------Django setup-------------------------------
django.setup()
# ----------------------------------Seeders----------------------------
def Roles():
    # Lista de datos a insertar
    Roles = [
        {'id':'1','name':'Administrador'},
        {'id':'2', 'name':'Nivel 1'},
        {'id':'3', 'name':'Nivel 2'},
        {'id':'4', 'name':'Nivel 3'},
        {'id':'5', 'name':'Nivel 4'}
        ]
    for rol in Roles:
        Rol = Group.objects.filter(pk = rol['id'])
        if Rol is None:
            Group.objects.create(id = rol['id'], name  = rol['name'])
        # else:
        #     Objecto = Group.objects.get(pk=rol['id'])
        #     Objecto.id = rol['id']
        #     Objecto.name = rol['name']
        #     Objecto.save()
            

def Municipios():
    # Lista de datos a insertar
    Municipios = [
        {'id':'1','nom_municipio':'Medellín'}
        ]
    for municipio in Municipios:
        municipality = Municipio.objects.filter(pk=municipio['id'])
        if municipality is None:
            Municipio.objects.create(nom_municipio=municipio['nom_municipio'])
        else:
            Objecto = Municipio.objects.get(pk=municipio['id'])
            Objecto.id_municipio = municipio['id']
            Objecto.nom_municipio = municipio['nom_municipio']
            Objecto.save()
def Tipo_Documento():
    # Lista de datos a insertar
    Tipo = [
        {'id':'1','nom_tipo_documento':'C.C'}
        ]
    for TDocumento in Tipo:
        tipoDocumento = TipoDocumento.objects.filter(pk=TDocumento['id'])
        if tipoDocumento is None:
            TipoDocumento.objects.create(nom_tipo_documento=TDocumento['nom_tipo_documento'])
        else:
            Objecto = TipoDocumento.objects.get(pk=TDocumento['id'])
            Objecto.id_tipo_documento = TDocumento['id']
            Objecto.nom_tipo_documento = TDocumento['nom_tipo_documento']
            Objecto.save()
def Tiposervicio():
    # Lista de datos a insertar
    Tipo=[
        {'id':'1','nombre':'Manicure'}
    ]
    for TServicio in Tipo:
        tipoServicio = Tipo_servicio.objects.filter(id_tipo_servicio=TServicio['id'])
        if tipoServicio is None:
            Tipo_servicio.objects.create(pk=TServicio["id"], nombre=TServicio['nombre'])
        else:
            Objecto = Tipo_servicio.objects.get(pk=TServicio['id'])
            Objecto.id_tipo_servicio = TServicio['id']
            Objecto.nombre = TServicio['nombre']
            Objecto.save()
# -----------------------------------Perfomance---------------------------
def Seeders():
    Roles()
    Municipios()
    Tipo_Documento()
    Tiposervicio()
    
Seeders()