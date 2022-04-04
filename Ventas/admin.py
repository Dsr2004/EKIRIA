from django.contrib import admin
from Ventas.models import *


admin.site.register(Servicio)
admin.site.register(Tipo_servicio)
admin.site.register(Catalogo)
admin.site.register(Pedido)
admin.site.register(PedidoItem)
admin.site.register(Cita)
admin.site.register(Calendario)
admin.site.register(Servicio_Personalizado)

# Register your models here.
