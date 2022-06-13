
from multiprocessing.sharedctypes import Value
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
from Proyecto_Ekiria.Mixin.Mixin import PermissionDecorator, PermissionMixin
from heapq import nlargest

from Configuracion.models import cambiosFooter, cambios
from Usuarios.models import Usuario
from ..models import Catalogo, Tipo_servicio, Servicio, PedidoItem
from ..forms import CatalogoForm, Tipo_servicioForm


"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administra el Admin de las ventas
<----------------------------------------------------------------->
"""

class AdminVentas(TemplateView):
    permission_required = ['view_catalogo']
    template_name = "Ventas.html"
    
    def get_grafico_serviciosMasSolicitados(self):
        pedidos = PedidoItem.objects.all()
        servicios = Servicio.objects.filter(estado=True)
        serviciosEnPedido = {}
        
        for i in servicios:
            CantServiciosEnPedido = PedidoItem.objects.filter(servicio_id=i).count()
            serviciosEnPedido[i.nombre] = CantServiciosEnPedido
        servicios_mas_solicitados =nlargest(10, serviciosEnPedido, key=serviciosEnPedido.get)
        datosDeServicos_mas_solcitados = []
        
        for i in servicios_mas_solicitados:
            servicio = serviciosEnPedido[i] 
            datosDeServicos_mas_solcitados.append(servicio)
            
        return {"servicio":servicios_mas_solicitados, "cantidad":datosDeServicos_mas_solcitados}
            

    def get(self,request, *args, **kwargs):
        formTipo_Servicio = Tipo_servicioForm
        servicios=Catalogo.objects.all()
        try:
            if request.session:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                if request.session['Admin'] == True:
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                else:
                    return redirect("SinPermisos")
        except:
            return redirect("IniciarSesion")
        
        servicios_mas_solicitados = self.get_grafico_serviciosMasSolicitados()

        datosServicios=servicios_mas_solicitados["servicio"]
        datosCantidadServicio = servicios_mas_solicitados["cantidad"]
        
        print(datosServicios)
        print("sdsdsdsdsdsd")
        print(datosCantidadServicio)
        
        #contexto
        context={
            'Tipo_Servicios':Tipo_servicio.objects.all(),
            'form_Tipo_Servicio':formTipo_Servicio,
            'servicios':servicios,
            "User":UserSesion,
            'cambios':cambiosQueryset,
            'footer':cambiosfQueryset,
            'datosServicios':datosServicios,
            'datosCantidadServicio':datosCantidadServicio,
        }
        
        return render(request, self.template_name, context)
    
class AgregarServicioalCatalogo(View):
    permission_required = ['change_catalogo', 'add_servicio']
    model = Catalogo
    form_class =   CatalogoForm
    template_name = "Catalogo/AgregarServicio.html"
    def get(self, request, *args, **kwargs):
        servicesInCatalogo=Catalogo.objects.all()
        servicesInCatalogoList=[]
        for i in servicesInCatalogo:
            id=i.servicio_id.id_servicio
            servicesInCatalogoList.append(id)
        ServiciosNoEnCatalogo=Servicio.objects.exclude(id_servicio__in=servicesInCatalogoList).filter(estado=True)

        paginado=Paginator(ServiciosNoEnCatalogo, 3)
        pagina = request.GET.get("page") or 1
        posts = paginado.get_page(pagina)
        pagina_actual=int(pagina)
        paginas=range(1,posts.paginator.num_pages+1)
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        contexto={
            "form":self.form_class,
            "servicios":ServiciosNoEnCatalogo,
            "NoEnCatalogo":posts,
            'paginas':paginas,
            'pagina_actual':pagina_actual,
            'cambios':cambiosQueryset,
            'footer':cambiosfQueryset,
        }

        return render(request, self.template_name, contexto)

    def post(self, request, *args, **kwargs):
        id = request.POST["id"]
        try:
            servicio = Servicio.objects.get(id_servicio=id)
            ServicioToCatalogo = Catalogo.objects.create(servicio_id=servicio)
            ServicioToCatalogo.save()
            return redirect("Ventas:adminVentas")
        except Exception as e: 
            formTipo_Servicio = Tipo_servicioForm
            servicios=Catalogo.objects.all()

            paginado=Paginator(servicios, 5)
            pagina = request.GET.get("page") or 1
            posts = paginado.get_page(pagina)
            pagina_actual=int(pagina)
            paginas=range(1,posts.paginator.num_pages+1)
            #contexto
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            contexto={
                'Tipo_Servicios':Tipo_servicio.objects.all(),
                'form_Tipo_Servicio':formTipo_Servicio,
                'servicios':posts,
                'paginas':paginas,
                'pagina_actual':pagina_actual,
                "errores": "No se puede realizar su solicitud, el error es: "+str(e),
                'cambios':cambiosQueryset,
                'footer':cambiosfQueryset,
            }

            return render(request, "Ventas.html", contexto)

@PermissionDecorator(['change_catalogo', 'delete_catalogo', 'delete_servicio','change_servicio'])    
def CambiarEstadoServicioEnCatalogo(request):
    if request.method == "POST":
        id = request.POST["estado"]
        update=Catalogo.objects.get(id_catalogo=id)
        estatus=update.estado
        if estatus==True:
            update.estado=False
            update.save()
        elif estatus==False:
            update.estado=True
            update.save()
        else:
            return redirect("Ventas:listarServiceditarcitaios")
        return HttpResponse(update)
    else:
        return redirect("Ventas:listarServicios")  
