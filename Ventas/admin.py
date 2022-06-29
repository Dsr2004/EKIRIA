from django.contrib import admin
from .models import Cita, Calendario, Pedido, PedidoItem

admin.site.register(Cita)
admin.site.register(Calendario)
admin.site.register(Pedido)
admin.site.register(PedidoItem)

# Register your models here.
