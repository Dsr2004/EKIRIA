from unicodedata import name
from django.urls import  path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns=[
    path("Roles/", login_required(views.ListarRol), name="Roles"),
    path("Cambios/", login_required(views.Cambios), name="Cambios"),
    path("CrearCambios/", login_required(views.CrearCambios.as_view()), name="Crear"),
    path("CrearCambiosFooter/", login_required(views.CrearCambiosFooter.as_view()), name="CrearFooter"),
    path("Permisos/", login_required(views.listarPermisos.as_view()), name="Permisos"),
    path("Admin/<int:pk>", login_required(views.Admin.as_view()), name="Admin"),
    path("EditarRol/<int:pk>",login_required(views.EditarRolView.as_view()), name="updateRol"),
    path("CrearRol/", login_required(views.CreateRolView.as_view()), name="CreateRol"),
    path("AgregarPermisos/", login_required(views.AgregarPer), name="AgregarPer"),
    # path("EstadoRol/",views.EstadoRol, name="estado"),
    path('EliminarRol/', login_required(views.eliminarRol), name="eliminarRol"),
]
