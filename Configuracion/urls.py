from unicodedata import name
from django.urls import  path
from . import views

urlpatterns=[
    path("Roles/", views.ListarRol, name="Roles"),
    path("Cambios/", views.Cambios, name="Cambios"),
    path("CrearCambios/", views.CrearCambios.as_view(), name="Crear"),
    path("CrearCambiosFooter/", views.CrearCambiosFooter.as_view(), name="CrearFooter"),
    path("Permisos/", views.listarPermisos.as_view(), name="Permisos"),
    path("Admin/<int:pk>", views.Admin.as_view(), name="Admin"),
    path("EditarRol/<int:pk>",views.EditarRolView.as_view(), name="updateRol"),
    path("CrearRol/", views.CreateRolView.as_view(), name="CreateRol"),
    path("AgregarPermisos/", views.AgregarPer, name="AgregarPer"),
    # path("EstadoRol/",views.EstadoRol, name="estado"),
    path('EliminarRol/', views.eliminarRol, name="eliminarRol"),
]
