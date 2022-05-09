from django.urls import path
from django.contrib.auth.decorators import login_required
from Ventas.views import *
from Ventas import carrito
app_name="Ventas"
urlpatterns = [
    path('AddtoCarrito/', login_required(carrito.actualizarItem), name="addtoCarrito"),

    path('AgregarCita/', login_required(AgregarCita.as_view()), name="agregarCita"),
    path('ListadoCitas/', login_required(ListarCita.as_view()), name="listarCitas"),
    path('DetalleCita/<int:pk>', login_required(DetalleCitaCliente.as_view()), name="detalleCita"),
    path('DetalleEditarCita/<int:pk>', login_required(EditarCitaDetalle.as_view()), name="detalleEditarCita"),
    path('EditarCita/<int:pk>', login_required(EditarCita.as_view()), name="editarCita"),
    path('EditarCitaCliente/<int:pk>', login_required(EditarCitaCliente.as_view()), name="editarCitaCliente"),
    path('CambiarEstadoCita/', login_required(CambiarEstadoDeCita.as_view()), name="cambiarEstadoCita"),
    path('CancelarCita/', login_required(CancelarCita.as_view()), name="cancelarCita"),

    path("BuscarEmpleadoParaCita/", login_required(BuscarDisponibilidadEmpleado.as_view()), name="buscarEmpleadoParaCita"),

    path('Catalogo/', login_required(Catalogo.as_view()), name="catalogo"),
    path('AgregarServicioCatalogo/', login_required(AgregarServicioalCatalogo.as_view()), name="agregarServicioCatalogo"),
    path("CambiarEstadoServicioEnCatalogo/",login_required(CambiarEstadoServicioEnCatalogo), name="cambiarEstadoServicioEnCatalogo"), 
    
    path('pruebas/', pruebas, name="pruebas"),
    path('correo/', correoPrueba, name="correo"),

    path('Carrito/', login_required(Carrito), name="carrito"),
    path('TerminarPedido/', login_required(AgandarCita.as_view()), name="terminarPedido"),
    path('Calendario/', login_required(Calendario.as_view()), name="calendario"),
    path('PersonalizarSer/', login_required(ServiciosPersonalizados.as_view()), name="personalizar"),
    path('ActualizarServicioPer/<int:pk>', login_required(EditarServiciosPersonalizados.as_view()), name="actualizarServicioPer"),
    # path("AgendarCita/", AgandarCita.as_view(), name="agendarCita"),
    
    
    path('AdminVentas/', login_required(AdminVentas.as_view()), name="adminVentas"),
    path('AgregarTipoServicio/', login_required(AgregarTipo_Servicio.as_view()), name="agregarTipoServicio"),
    path('EditarTipoServicio/<int:pk>', login_required(EditarTipo_Servicio.as_view()), name="editarTipoServicio"),
    path('EditarEstadoTipoServicio/', login_required(CambiarEstadoTipoServicio), name="editarEstadoTipoServicio"),
    path('ElimiarTipoServicio/<int:pk>', login_required(ElimininarTipoServicio.as_view()), name="eliminarTipoServicio"),

    path('AgregarServicio/', login_required(AgregarServicio.as_view()), name="agregarServicio"),
    path('ListadoServicios/', login_required(ListarServicio.as_view()), name="listarServicios"),
    path('CambiarEstadoServicio/', login_required(CambiarEstadoServicio), name="cambiarEstadoServicio"),
    path('EditarServicio/<int:pk>', login_required(EditarServicio.as_view()), name="editarServicio"),
    path('<slug>/', login_required(ServicioDetalle.as_view()), name="detalleSer"),                    
]

