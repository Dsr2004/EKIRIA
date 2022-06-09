from django.urls import path
from django.contrib.auth.decorators import login_required
from Ventas.views import admin, citas, serviciosPersonalizados, servicios, tipoServicios, views
from Ventas import carrito
app_name="Ventas"
urlpatterns = [
    path('AddtoCarrito/', login_required(carrito.actualizarItem), name="addtoCarrito"),

    path('AgregarCita/', login_required(citas.AgregarCita.as_view()), name="agregarCita"),
    path('ListadoCitas/', login_required(citas.ListarCita.as_view()), name="listarCitas"),
    path('DetalleCita/<int:pk>', login_required(citas.DetalleCitaCliente.as_view()), name="detalleCita"),
    path('DetalleEditarCita/<int:pk>', login_required(citas.EditarCitaDetalle.as_view()), name="detalleEditarCita"),
    path('EditarCita/<int:pk>', login_required(citas.EditarCita.as_view()), name="editarCita"),
    path('EditarCitaCliente/<int:pk>', login_required(citas.EditarCitaCliente.as_view()), name="editarCitaCliente"),
    path('CambiarEstadoCita/', login_required(citas.CambiarEstadoDeCita.as_view()), name="cambiarEstadoCita"),
    path('CancelarCita/', login_required(citas.CancelarCita.as_view()), name="cancelarCita"),
    path('DetalleCalendario/<int:pk>', login_required(citas.DetalleCitaCalendario.as_view()), name="detalleCalendario"),

    path("BuscarEmpleadoParaCita/", login_required(citas.BuscarDisponibilidadEmpleado.as_view()), name="buscarEmpleadoParaCita"),
    path("BuscarEmpleadoParaEditarCita/", login_required(citas.BuscarDisponibilidadEmpleadoEditarCita.as_view()), name="buscarEmpleadoParaEditarCita"),

    path('Catalogo/', login_required(views.Catalogo.as_view()), name="catalogo"),
    path('AgregarServicioCatalogo/', login_required(admin.AgregarServicioalCatalogo.as_view()), name="agregarServicioCatalogo"),
    path("CambiarEstadoServicioEnCatalogo/",login_required(admin.CambiarEstadoServicioEnCatalogo), name="cambiarEstadoServicioEnCatalogo"),
    
    path('pruebas/', views.pruebas, name="pruebas"),
    path('correo/', views.correoPrueba, name="correo"),

    path('Carrito/', login_required(views.Carrito), name="carrito"),
    path('TerminarPedido/', login_required(citas.AgandarCita.as_view()), name="terminarPedido"),
    path('Calendario/', login_required(views.Calendario.as_view()), name="calendario"),
    path('PersonalizarSer/', login_required(serviciosPersonalizados.ServiciosPersonalizados.as_view()), name="personalizar"),
    path('ActualizarServicioPer/<int:pk>', login_required(serviciosPersonalizados.EditarServiciosPersonalizados.as_view()), name="actualizarServicioPer"),
    # path("AgendarCita/", AgandarCita.as_view(), name="agendarCita"),
    
    
    path('AdminVentas/', login_required(admin.AdminVentas.as_view()), name="adminVentas"),
    path('AgregarTipoServicio/', login_required(tipoServicios.AgregarTipo_Servicio.as_view()), name="agregarTipoServicio"),
    path('EditarTipoServicio/<int:pk>', login_required(tipoServicios.EditarTipo_Servicio.as_view()), name="editarTipoServicio"),
    path('EditarEstadoTipoServicio/', login_required(tipoServicios.CambiarEstadoTipoServicio), name="editarEstadoTipoServicio"),
    path('ElimiarTipoServicio/<int:pk>', login_required(tipoServicios.ElimininarTipoServicio.as_view()), name="eliminarTipoServicio"),

    path('AgregarServicio/', login_required(servicios.AgregarServicio.as_view()), name="agregarServicio"),
    path('ListadoServicios/', login_required(servicios.ListarServicio.as_view()), name="listarServicios"),
    path('CambiarEstadoServicio/', login_required(servicios.CambiarEstadoServicio), name="cambiarEstadoServicio"),
    path('EditarServicio/<int:pk>', login_required(servicios.EditarServicio.as_view()), name="editarServicio"),
    path('<slug>/', servicios.ServicioDetalle.as_view(), name="detalleSer"),
]

    # SIN LOGIN REQUIRED

    # path('AddtoCarrito/',  (carrito.actualizarItem), name="addtoCarrito"),

    # path('AgregarCita/',citas.AgregarCita.as_view(), name="agregarCita"),
    # path('ListadoCitas/',citas.ListarCita.as_view(), name="listarCitas"),
    # path('DetalleCita/<int:pk>', citas.DetalleCitaCliente.as_view(), name="detalleCita"),
    # path('DetalleEditarCita/<int:pk>', citas.EditarCitaDetalle.as_view(), name="detalleEditarCita"),
    # path('EditarCita/<int:pk>', citas.EditarCita.as_view(), name="editarCita"),
    # path('EditarCitaCliente/<int:pk>', citas.EditarCitaCliente.as_view(), name="editarCitaCliente"),
    # path('CambiarEstadoCita/', citas.CambiarEstadoDeCita.as_view(), name="cambiarEstadoCita"),
    # path('CancelarCita/', citas.CancelarCita.as_view(), name="cancelarCita"),

    # path("BuscarEmpleadoParaCita/", citas.BuscarDisponibilidadEmpleado.as_view(), name="buscarEmpleadoParaCita"),

    # path('Catalogo/', views.Catalogo.as_view(), name="catalogo"),
    # path('AgregarServicioCatalogo/', admin.AgregarServicioalCatalogo.as_view(), name="agregarServicioCatalogo"),
    # path("CambiarEstadoServicioEnCatalogo/",admin.CambiarEstadoServicioEnCatalogo, name="cambiarEstadoServicioEnCatalogo"),
    
    # path('pruebas/', views.pruebas, name="pruebas"),
    # path('correo/', views.correoPrueba, name="correo"),

    # path('Carrito/', views.Carrito, name="carrito"),
    # path('TerminarPedido/', citas.AgandarCita.as_view(), name="terminarPedido"),
    # path('Calendario/', views.Calendario.as_view(), name="calendario"),
    # path('PersonalizarSer/', serviciosPersonalizados.ServiciosPersonalizados.as_view(), name="personalizar"),
    # path('ActualizarServicioPer/<int:pk>', serviciosPersonalizados.EditarServiciosPersonalizados.as_view(), name="actualizarServicioPer"),
    # # path("AgendarCita/", AgandarCita.as_view(), name="agendarCita"),
    
    
    # path('AdminVentas/', admin.AdminVentas.as_view(), name="adminVentas"),
    # path('AgregarTipoServicio/', tipoServicios.AgregarTipo_Servicio.as_view(), name="agregarTipoServicio"),
    # path('EditarTipoServicio/<int:pk>', tipoServicios.EditarTipo_Servicio.as_view(), name="editarTipoServicio"),
    # path('EditarEstadoTipoServicio/', tipoServicios.CambiarEstadoTipoServicio, name="editarEstadoTipoServicio"),
    # path('ElimiarTipoServicio/<int:pk>', tipoServicios.ElimininarTipoServicio.as_view(), name="eliminarTipoServicio"),

    # path('AgregarServicio/', servicios.AgregarServicio.as_view(), name="agregarServicio"),
    # path('ListadoServicios/', servicios.ListarServicio.as_view(), name="listarServicios"),
    # path('CambiarEstadoServicio/', servicios.CambiarEstadoServicio, name="cambiarEstadoServicio"),
    # path('EditarServicio/<int:pk>', servicios.EditarServicio.as_view(), name="editarServicio"),
    # path('<slug>/', servicios.ServicioDetalle.as_view(), name="detalleSer"),

# --------------------------------------------

# CON LOGIN REQUIRED 
# path('AddtoCarrito/', login_required(carrito.actualizarItem), name="addtoCarrito"),

#     path('AgregarCita/', login_required(citas.AgregarCita.as_view()), name="agregarCita"),
#     path('ListadoCitas/', login_required(citas.ListarCita.as_view()), name="listarCitas"),
#     path('DetalleCita/<int:pk>', login_required(citas.DetalleCitaCliente.as_view()), name="detalleCita"),
#     path('DetalleEditarCita/<int:pk>', login_required(citas.EditarCitaDetalle.as_view()), name="detalleEditarCita"),
#     path('EditarCita/<int:pk>', login_required(citas.EditarCita.as_view()), name="editarCita"),
#     path('EditarCitaCliente/<int:pk>', login_required(citas.EditarCitaCliente.as_view()), name="editarCitaCliente"),
#     path('CambiarEstadoCita/', login_required(citas.CambiarEstadoDeCita.as_view()), name="cambiarEstadoCita"),
#     path('CancelarCita/', login_required(citas.CancelarCita.as_view()), name="cancelarCita"),

#     path("BuscarEmpleadoParaCita/", login_required(citas.BuscarDisponibilidadEmpleado.as_view()), name="buscarEmpleadoParaCita"),

#     path('Catalogo/', login_required(views.Catalogo.as_view()), name="catalogo"),
#     path('AgregarServicioCatalogo/', login_required(admin.AgregarServicioalCatalogo.as_view()), name="agregarServicioCatalogo"),
#     path("CambiarEstadoServicioEnCatalogo/",login_required(admin.CambiarEstadoServicioEnCatalogo), name="cambiarEstadoServicioEnCatalogo"),
    
#     path('pruebas/', views.pruebas, name="pruebas"),
#     path('correo/', views.correoPrueba, name="correo"),

#     path('Carrito/', login_required(views.Carrito), name="carrito"),
#     path('TerminarPedido/', login_required(citas.AgandarCita.as_view()), name="terminarPedido"),
#     path('Calendario/', login_required(views.Calendario.as_view()), name="calendario"),
#     path('PersonalizarSer/', login_required(serviciosPersonalizados.ServiciosPersonalizados.as_view()), name="personalizar"),
#     path('ActualizarServicioPer/<int:pk>', login_required(serviciosPersonalizados.EditarServiciosPersonalizados.as_view()), name="actualizarServicioPer"),
#     # path("AgendarCita/", AgandarCita.as_view(), name="agendarCita"),
    
    
#     path('AdminVentas/', login_required(admin.AdminVentas.as_view()), name="adminVentas"),
#     path('AgregarTipoServicio/', login_required(tipoServicios.AgregarTipo_Servicio.as_view()), name="agregarTipoServicio"),
#     path('EditarTipoServicio/<int:pk>', login_required(tipoServicios.EditarTipo_Servicio.as_view()), name="editarTipoServicio"),
#     path('EditarEstadoTipoServicio/', login_required(tipoServicios.CambiarEstadoTipoServicio), name="editarEstadoTipoServicio"),
#     path('ElimiarTipoServicio/<int:pk>', login_required(tipoServicios.ElimininarTipoServicio.as_view()), name="eliminarTipoServicio"),

#     path('AgregarServicio/', login_required(servicios.AgregarServicio.as_view()), name="agregarServicio"),
#     path('ListadoServicios/', login_required(servicios.ListarServicio.as_view()), name="listarServicios"),
#     path('CambiarEstadoServicio/', login_required(servicios.CambiarEstadoServicio), name="cambiarEstadoServicio"),
#     path('EditarServicio/<int:pk>', login_required(servicios.EditarServicio.as_view()), name="editarServicio"),
#     path('<slug>/', login_required(servicios.ServicioDetalle.as_view()), name="detalleSer"),