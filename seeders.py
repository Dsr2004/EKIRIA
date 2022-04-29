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
from Configuracion.models import *
# ---------------------------------Import information-------------------------
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
        {'id':'1','nombre':'Manicure'},
        {'id':'2','nombre':'Pedicure'},
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

def PermisosCliente(rol):
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
                            # Permission - can view calendario
            content_type_Calendario = ContentType.objects.get_for_model(Calendario)
            permission_view_Calendario = Permission.objects.get(
                codename='view_calendario',
                content_type=content_type_Calendario,
            )
            rol.permissions.add(permission_view_Calendario)
                            #   Permission - can view citas
            content_type_Citas = ContentType.objects.get_for_model(Cita)
            permission_view_Cita = Permission.objects.get(
                codename='view_cita',
                content_type=content_type_Citas,
            )
            rol.permissions.add(permission_view_Cita)
                                # Permission - can change citas
            permission_change_Cita = Permission.objects.get(
                codename='change_cita',
                content_type=content_type_Citas,
            )
            rol.permissions.add(permission_change_Cita)
                                # Permisssion - can delete citas
            permission_delete_Cita = Permission.objects.get(
                codename='delete_cita',
                content_type=content_type_Citas,
            )
            rol.permissions.add(permission_delete_Cita)
                                # Permisssion - can add citas
            permission_add_Cita = Permission.objects.get(
                codename='add_cita',
                content_type=content_type_Citas,
            )
            rol.permissions.add(permission_add_Cita)
                                #   Permission - can view pedidos
            content_type_Pedido = ContentType.objects.get_for_model(Pedido)
            permission_view_Pedido = Permission.objects.get(
                codename='view_pedido',
                content_type=content_type_Pedido,
            )
            rol.permissions.add(permission_view_Pedido)
                                 # Permission - can change Pedido
            permission_change_Pedido = Permission.objects.get(
                codename='change_Pedido',
                content_type=content_type_Pedido,
            )
            rol.permissions.add(permission_change_Pedido)
                                # Permisssion - can delete Pedido
            permission_delete_Pedido = Permission.objects.get(
                codename='delete_Pedido',
                content_type=content_type_Pedido,
            )
            rol.permissions.add(permission_delete_Pedido)
                                # Permisssion - can add Pedido
            permission_add_Pedido = Permission.objects.get(
                codename='add_Pedido',
                content_type=content_type_Pedido,
            )
            rol.permissions.add(permission_add_Pedido)
                                #   Permission - can view pedidos
            content_type_catalogo = ContentType.objects.get_for_model(Catalogo)
            permission_view_catalogo = Permission.objects.get(
                codename='view_catalogo',
                content_type=content_type_catalogo,
            )
            rol.permissions.add(permission_view_catalogo)
                                #   Permission - can view pedidoItem
            content_type_PedidoItem = ContentType.objects.get_for_model(PedidoItem)
            permission_view_PedidoItem = Permission.objects.get(
                codename='view_PedidoItem',
                content_type=content_type_PedidoItem,
            )
            rol.permissions.add(permission_view_PedidoItem)
                                #   Permission - can change PedidoItem
            permission_change_PedidoItem = Permission.objects.get(
                codename='change_PedidoItem',
                content_type=content_type_PedidoItem,
            )
            rol.permissions.add(permission_change_PedidoItem)
                            #   Permission - can add PedidoItem
            permission_add_PedidoItem = Permission.objects.get(
                codename='add_PedidoItem',
                content_type=content_type_PedidoItem,
            )
            rol.permissions.add(permission_add_PedidoItem)
                            #   Permission - can delete PedidoItem
            permission_delete_PedidoItem = Permission.objects.get(
                codename='delete_PedidoItem',
                content_type=content_type_PedidoItem,
            )
            rol.permissions.add(permission_delete_PedidoItem)
                                #   Permission - can view TipoServicio
            content_type_TipoServicio = ContentType.objects.get_for_model(Tipo_servicio)
            permission_view_TipoServicio = Permission.objects.get(
                codename='view_Tipo_servicio',
                content_type=content_type_TipoServicio,
            )
            rol.permissions.add(permission_view_TipoServicio)
                                #   Permission - can view Municipio
            content_type_Municipio = ContentType.objects.get_for_model(Municipio)
            permission_view_Municipio = Permission.objects.get(
                codename='view_Municipio',
                content_type=content_type_Municipio,
            )
            rol.permissions.add(permission_view_Municipio)
                                #   Permission - can view TipoDocumento
            content_type_TipoDocumento = ContentType.objects.get_for_model(TipoDocumento)
            permission_view_TipoDocumento = Permission.objects.get(
                codename='view_TipoDocumento',
                content_type=content_type_TipoDocumento,
            )
            rol.permissions.add(permission_view_TipoDocumento)
                                #   Permission - can view Servicio_Personalizado
            content_type_Servicio_Personalizado = ContentType.objects.get_for_model(Servicio_Personalizado)
            permission_view_Servicio_Personalizado = Permission.objects.get(
                codename='view_Servicio_Personalizado',
                content_type=content_type_Servicio_Personalizado,
            )
            rol.permissions.add(permission_view_Servicio_Personalizado)
                                #   Permission - can change Servicio_Personalizado
            permission_change_Servicio_Personalizado = Permission.objects.get(
                codename='change_Servicio_Personalizado',
                content_type=content_type_Servicio_Personalizado,
            )
            rol.permissions.add(permission_change_Servicio_Personalizado)
                            #   Permission - can add Servicio_Personalizado
            permission_add_Servicio_Personalizado = Permission.objects.get(
                codename='add_Servicio_Personalizado',
                content_type=content_type_Servicio_Personalizado,
            )
            rol.permissions.add(permission_add_Servicio_Personalizado)
                            #   Permission - can delete Servicio_Personalizado
            permission_delete_Servicio_Personalizado = Permission.objects.get(
                codename='delete_Servicio_Personalizado',
                content_type=content_type_Servicio_Personalizado,
            )
            rol.permissions.add(permission_delete_Servicio_Personalizado)

def Rol_Permisos():
    roles = Group.objects.all()
    for rol in roles:
        if rol.id == 1:
            Permisos = Permission.objects.all()
            for permiso in Permisos:
                rol.permissions.add(permiso)
                rol.save()
        if rol.id == 2:
            PermisosCliente(rol)
        if rol.id == 3:
            PermisosCliente(rol)
        if rol.id == 4:
            PermisosCliente(rol)
        if rol.id == 5:
            PermisosCliente(rol)
        if rol.id == 6:
            Permisos = Permission.objects.all()
            for permiso in Permisos:
                rol.permissions.add(permiso)
                rol.save()

def Cambios():
    Cambios = {
        'id':'1',
        'Color_letra':'#000', 
        'Color_fondo':'#fff', 
        'tamano_Titulo':'24', 
        'tamano_Texto':'18', 
        'Tipo_Letra':'Arial', 
        'Texto_Mision':'hola',
        'Texto_Vision':'hola2',
        }
    try: 
        Objecto = cambios.objects.get(pk = Cambios['id'])
        Objecto.Color_Letra = Cambios['Color_letra']
        Objecto.Color_Fondo = Cambios['Color_fondo']
        Objecto.tamano_Titulo = Cambios['tamano_Titulo']
        Objecto.tamano_Texto = Cambios['tamano_Texto']
        Objecto.Tipo_Letra = Cambios['Tipo_Letra']
        Objecto.Texto_Mision = Cambios['Texto_Mision']
        Objecto.Texto_Vision = Cambios['Texto_Vision']
        Objecto.save()
    except:
        cambios.objects.create(pk = Cambios['id'],
        Color_Letra = Cambios['Color_letra'],
        Color_Fondo = Cambios['Color_fondo'],
        tamano_Titulo = Cambios['tamano_Titulo'],
        tamano_Texto = Cambios['tamano_Texto'],
        Tipo_Letra = Cambios['Tipo_Letra'],
        Texto_Mision = Cambios['Texto_Mision'],
        Texto_Vision = Cambios['Texto_Vision'],
        )

def Footer():
    Footer = {
        'id':'1',
        'Direccion':'Cr 13 Cll 10 -A', 
        'Telefono':'3206374472', 
        'Derechos':'2022', 
        'Footer_Color_Letra':'#fff', 
        'Footer_Color_Fondo':'#000', 
        'Footer_tamano_Titulo':'24',
        'Footer_tamano_Texto':'18',
        'Footer_Tipo_Letra':'Sans-serif',
        }
    try: 
        Objecto = cambiosFooter.objects.get(pk = Footer['id'])
        Objecto.Direccion = Footer['Direccion']
        Objecto.Telefono = Footer['Telefono']
        Objecto.Derechos = Footer['Derechos']
        Objecto.Footer_Color_Letra = Footer['Footer_Color_Letra']
        Objecto.Footer_Color_Fondo = Footer['Footer_Color_Fondo']
        Objecto.Footer_tamano_Titulo = Footer['Footer_tamano_Titulo']
        Objecto.Footer_tamano_Texto = Footer['Footer_tamano_Texto']
        Objecto.Footer_Tipo_Letra = Footer['Footer_Tipo_Letra'],
        Objecto.save()
    except:
        cambiosFooter.objects.create(pk = Footer['id'],
        Direccion = Footer['Direccion'],
        Telefono = Footer['Telefono'],
        Derechos = Footer['Derechos'],
        Footer_Color_Letra = Footer['Footer_Color_Letra'],
        Footer_Color_Fondo = Footer['Footer_Color_Fondo'],
        Footer_tamano_Titulo = Footer['Footer_tamano_Titulo'],
        Footer_tamano_Texto = Footer['Footer_tamano_Texto'],
        Footer_Tipo_Letra = Footer['Footer_Tipo_Letra'],
        )
# -----------------------------------Perfomance---------------------------

def Seeders():
    Roles()
    Municipios()
    Tipo_Documento()
    Tiposervicio()
    Rol_Permisos()
    Cambios()
    Footer()
    
Seeders()