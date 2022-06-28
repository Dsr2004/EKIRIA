from django.urls import path
from Modulo_compras.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path ("creartp/",login_required(Creartp.as_view()), name="creartp"),
    path ("listarcompra/", Listcompra, name="listarcompra"),
    path ("crearcompra/", login_required(Crearcompra.as_view()), name="crearcompra"),
    path ("listarprod/", Listproductos, name="listarprod"),
    path ("crearprod/", login_required(Crearprod.as_view()), name="crearprod"),
    path ("modificarprod/<int:pk>", login_required(Modificarprod.as_view()), name="modificarprod"),
    path ("listarprov/", Listarprov, name="listarprov"),
    path ("crearprov/", login_required(Crearprov.as_view()), name="crearprov"),
    path ("eliminarprov/<int:id_proveedor>", Eliminarprov, name="eliminarprov"),
    path ("modificarprov/<int:pk>", login_required(modificarprov.as_view()), name="modificarprov"),
    path ("modificartp/<int:pk>", login_required(modificartp.as_view()), name="modificartp"),
    path ("actprov/", Actprov, name="actprov"),
    path ("cambiarestado/", cambiarestado, name="camestado"),
    path ("cambiarestadoDeProducto/", cambiarestadoProducto, name="camestadoProducto"),
    path ("cambiarestadoDeCompra/", cambiarestadoCompra, name="camestadoCompra"),
    path ("cambiarestadoDeTProducto/", cambiarestadoTProducto, name="camestadoTProducto"),
    path("VerDetalleCompra/<int:pk>", login_required(verDetalleCompra.as_view()), name="VerDetalle"),
    path("crearHistory/", login_required(crearHistorial), name="CrearHistorial"),
    path("restarProductos/", login_required(eliminarProductos.as_view()), name="RestarProductos"),
    path("ListaCompra/", login_required(ListaCompra.as_view()), name="ListaCompra"),
    path("Graficos/", login_required(GraficoCompras.as_view()), name="GraficoCompras"),
]
 