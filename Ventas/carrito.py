import json
from django.http import JsonResponse

from Usuarios.models import Usuario
from .models import *


def actualizarItem(request):
    data = request.POST
    servicioid = data["servicioId"]
    accion = data["accion"]
    
    cliente = Usuario.objects.get(username=request.session['username'])
    
    pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)


    if accion== "remove":
        servicio= Servicio.objects.get(id_servicio=servicioid)
        itemPedio, creado = PedidoItem.objects.get_or_create(pedido_id=pedido,servicio_id=servicio)
        itemPedio.delete()
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
    
    return JsonResponse('Item fue anadido', safe=False)