import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Proyecto_Ekiria.Mixin.Mixin import PermissionDecorator, PermissionMixin
from Usuarios.models import Usuario
from .models import *


@login_required()
# @PermissionDecorator([' delete_pedidoItem', 'change_pedidoItem'])
def actualizarItem(request):
    if request.method == 'POST':
        data = request.POST
        if data["servicioId"]:
            servicioid = data["servicioId"]
        accion = data["accion"]
        
        cliente = Usuario.objects.get(pk=request.user.pk)
        
        pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)

        if accion== "remove":
            servicio= Servicio.objects.get(id_servicio=servicioid)
            itemPedio, creado = PedidoItem.objects.get_or_create(pedido_id=pedido,servicio_id=servicio)
            itemPedio.delete()
            pedido.total_pagar = pedido.get_total_carrito
            pedido.save()
        elif accion == "removePer":
            servicio= Servicio_Personalizado.objects.get(id_servicio_personalizado=servicioid)
            itemPedio, creado = PedidoItem.objects.get_or_create(pedido_id=pedido,servicio_personalizado_id=servicio)
            itemPedio.delete()
            servicio.delete()
            items = PedidoItem.objects.filter(pedido_id=pedido)
            cont = 0
            for i in items:
                if not i.servicio_personalizado_id == None:
                    cont+=1
            
            if cont <= 0:
                pedido.esPersonalizado = False
                pedido.save()


        elif accion == "updatePer":
            pass
        else:
            servicio= Servicio.objects.get(id_servicio=servicioid)
            itemPedio, creado = PedidoItem.objects.get_or_create(pedido_id=pedido,servicio_id=servicio)
            pedido.total_pagar = pedido.get_total_carrito
            pedido.save()
        
        return JsonResponse('Item fue anadido', safe=False)
    


def buscarPedido(request):
    cliente = Usuario.objects.get(username=request.session['username'])
    pedido, = Pedido.objects.get(cliente_id=cliente, completado=False)

    if pedido:
        return True
    else:
        return False