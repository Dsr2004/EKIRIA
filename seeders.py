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
        try:
            Objecto = Group.objects.get(pk=rol['id'])
            Objecto.id = rol['id']
            Objecto.name = rol['name']
            Objecto.save()
        except:
            try:
                Objecto=Group.objects.get(id = rol['id'])
                Objecto.delete()
                Group.objects.create(id = rol['id'], name  = rol['name'])
            except:
                Group.objects.create(id = rol['id'], name  = rol['name'])
            

def Municipios():
    # Lista de datos a insertar
    Municipios = [
        {'id':'1','nom_municipio':'Medellín'},
        {'id':'2','nom_municipio':'Bello'},
        ]
    for municipio in Municipios:
        try:
            Objecto = Municipio.objects.get(pk=municipio['id'])
            Objecto.id_municipio = municipio['id']
            Objecto.nom_municipio = municipio['nom_municipio']
            Objecto.save()
        except:
            try:
                Objecto = Municipio.objects.get(nom_municipio=municipio['nom_municipio'])
                Objecto.delete()
                Municipio.objects.create(pk=municipio['id'],nom_municipio=municipio['nom_municipio'])
            except:
                Municipio.objects.create(pk=municipio['id'],nom_municipio=municipio['nom_municipio'])
                

                
def Tipo_Documento():
    # Lista de datos a insertar
    Tipo = [
        {'id':'1','nom_tipo_documento':'C.C'}
        ]
    for TDocumento in Tipo:
        try:
            Objecto = TipoDocumento.objects.get(pk=TDocumento['id'])
            Objecto.id_tipo_documento = TDocumento['id']
            Objecto.nom_tipo_documento = TDocumento['nom_tipo_documento']
            Objecto.save()
        except:
            try:
                Objecto=TipoDocumento.objects.get(nom_tipo_documento=TDocumento['nom_tipo_documento'])
                Objecto.delete()
                TipoDocumento.objects.create(pk=TDocumento['id'],nom_tipo_documento=TDocumento['nom_tipo_documento'])
            except:
                TipoDocumento.objects.create(pk=TDocumento['id'],nom_tipo_documento=TDocumento['nom_tipo_documento'])
            
def Tiposervicio():
    # Lista de datos a insertar
    Tipo=[
        {'id':'1','nombre':'Manicure'}
    ]
    for TServicio in Tipo:
        try:
            Objecto = Tipo_servicio.objects.get(pk=TServicio['id'])
            Objecto.id_tipo_servicio = TServicio['id']
            Objecto.nombre = TServicio['nombre']
            Objecto.save()
        except:
            try:
                Objecto=Tipo_servicio.objects.get(pk=TServicio["id"])
                Objecto.delete()
                Tipo_servicio.objects.create(pk=TServicio["id"], nombre=TServicio['nombre'])
            except:
                Tipo_servicio.objects.create(pk=TServicio["id"], nombre=TServicio['nombre'])
            
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