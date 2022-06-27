from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Notification, BorrarNotificacion,CambiarEstado

urlpatterns = [
    path('', login_required(Notification.as_view()), name="Notify"),
    path("borrar/<int:pk>", login_required(BorrarNotificacion), name="DeleteNotify"),
    path("cambiarEstado/", login_required(CambiarEstado), name="ChangeStatus")
]