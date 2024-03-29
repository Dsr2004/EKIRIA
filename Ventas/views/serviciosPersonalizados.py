from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from Proyecto_Ekiria.Mixin.Mixin import PermissionDecorator, PermissionMixin
from Configuracion.models import cambios, cambiosFooter
from Usuarios.models import Usuario
from Ventas.forms import Servicio_PersonalizadoForm
from Ventas.models import Servicio_Personalizado, Pedido, PedidoItem


class ServiciosPersonalizados(CreateView,PermissionMixin):
    # permission_required = ['add_servicio_personalizado']
    model = Servicio_Personalizado
    form_class = Servicio_PersonalizadoForm
    template_name = "AddservicioPer.html"
    success_url=reverse_lazy("Ventas:catalogo")

    def get_context_data(self, *args, **kwargs):
        context = super(ServiciosPersonalizados, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                    context["User"]=UserSesion
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                context['cambios']=cambiosQueryset
                context['footer']=cambiosfQueryset
                return context
        except:
            return redirect("IniciarSesion")

    def form_valid(self, form, *args, **kwargs):
        objeto=form.save()
        cliente = Usuario.objects.get(username=self.request.session['username'])
        pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)
        itemPedio = PedidoItem.objects.get_or_create(pedido_id=pedido,servicio_personalizado_id=objeto)
        pedido.esPersonalizado = True
        pedido.save()

        return redirect("Ventas:carrito")
    




@method_decorator(csrf_exempt, name='dispatch')
class EditarServiciosPersonalizados(UpdateView, PermissionMixin):
    permission_required = ['change_servicio_personalizado']
    model = Servicio_Personalizado
    form_class = Servicio_PersonalizadoForm
    template_name = "Carrito/ActualizarServicioPer.html"
    success_url=reverse_lazy("Ventas:carrito")
    
    def post(self, request, *args, **kwargs):
        print(request.FILES)
        form = self.form_class(request.POST,request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect("Ventas:carrito")
        else:
            respuesta = JsonResponse({"errores":form.errors})
            respuesta.status_code = 400
            return respuesta
      

