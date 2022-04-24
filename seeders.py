"""
WSGI config for Proyecto_Ekiria project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from pprint import pprint
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Proyecto_Ekiria.settings")
import django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
# --------------------------------Import models------------------------------
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
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
        {'id':'5', 'name':'Nivel 4'},
        {'id':'6', 'name':'Empleado'},
        ]
    for rol in Roles:
        Rol = Group.objects.filter(pk = rol['id'])
        for queryset in Rol:
            if queryset is not None:
                Objecto = Group.objects.get(pk=rol['id'])
                Objecto.id = rol['id']
                Objecto.name = rol['name']
                Objecto.save()
            else:
                Group.objects.create(id = rol['id'], name  = rol['name'])
            

def Municipios():
    # Lista de datos a insertar
    Municipios = [
        {'id':'1','nom_municipio':'Medellín'}
        ]
    for municipio in Municipios:
        municipality = Municipio.objects.filter(pk=municipio['id'])
        for queryset in municipality:
            if queryset is None:
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
        for queryset in tipoDocumento:
            if queryset is None:
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
        for queryset in tipoServicio:
            if queryset is None:
                Tipo_servicio.objects.create(pk=TServicio["id"], nombre=TServicio['nombre'])
            else:
                Objecto = Tipo_servicio.objects.get(pk=TServicio['id'])
                Objecto.id_tipo_servicio = TServicio['id']
                Objecto.nombre = TServicio['nombre']
                Objecto.save()
            
def Rol_Permisos():
    roles = Group.objects.all()
    for rol in roles:
        if rol.id == 1:
            Permisos = Permission.objects.all()
            for permiso in Permisos:
                rol.permissions.add(permiso)
                rol.save()
        if rol.id == 2:
                        #    Permission - Can view notifications
            content_type_Notificacion = ContentType.objects.get_for_model(Notificacion)
            permission_view_notificacion = Permission.objects.get(
                codename='view_notificacion',
                content_type=content_type_Notificacion,
            )
            rol.permissions.add(permission_view_notificacion)
                        #    Permission - Can delete notifications
            permission_delete_notificacion = Permission.objects.get(
                codename="delete_notificacion",
                content_type=content_type_Notificacion,
            )
            rol.permissions.add(permission_delete_notificacion)
# -----------------------------------Perfomance---------------------------
def Seeders():
    Roles()
    Municipios()
    Tipo_Documento()
    Tiposervicio()
    Rol_Permisos()
    
Seeders()