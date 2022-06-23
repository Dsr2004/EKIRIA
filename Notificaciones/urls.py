from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Notification

urlpatterns = [
path('', login_required(Notification.as_view()), name="Notify"),
]