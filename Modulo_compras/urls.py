from unicodedata import name
from django.urls import path
from Modulo_compras.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path ("creartp/",login_required(Creartp.as_view()), name="creartp"),
    path ("listarcompra/", Listcompra, name="listarcompra"),
    path ("crearcompra/", login_required(Crearcompra.as_view()), name="crearcompra"),
    path ("listarprod/", Listproductos, name="listarprod"),
    path ("crearprod/", login_required(Crearprod.as_view()), name="crearprod"),
    path ("modificarprod/<int:pk>", login_required(modificarprov.as_view()), name="modificarprod"),
    path ("listarprov/", Listarprov, name="listarprov"),
    path ("crearprov/", login_required(Crearprov.as_view()), name="crearprov"),
    path ("eliminarprov/<int:id_proveedor>", Eliminarprov, name="eliminarprov"),
    path ("modificarprov/<int:pk>", login_required(modificarprov.as_view()), name="modificarprov"),
    path ("actprov/", Actprov, name="actprov"),
    path ("cambiarestado/", cambiarestado, name="camestado"),
    path ("cambiarestadoDeProducto/", cambiarestadoProducto, name="camestadoProducto"),
]
 