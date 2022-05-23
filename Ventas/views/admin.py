from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView


from Configuracion.models import cambiosFooter, cambios
from Usuarios.models import Usuario
from ..models import Catalogo, Tipo_servicio, Servicio
from ..forms import CatalogoForm, EditarTipoServicioForm

"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administra el Admin de las ventas
<----------------------------------------------------------------->
"""

class AdminVentas(TemplateView):
    template_name = "Ventas.html"

    def get(self,request, *args, **kwargs):
        formTipo_Servicio = EditarTipoServicioForm
        servicios=Catalogo.objects.all()

        paginado=Paginator(servicios, 5)
        pagina = request.GET.get("page") or 1
        posts = paginado.get_page(pagina)
        pagina_actual=int(pagina)
        paginas=range(1,posts.paginator.num_pages+1)
        #autenticacion usuario
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

        #contexto
        context={
            'Tipo_Servicios':Tipo_servicio.objects.all(),
            'form_Tipo_Servicio':formTipo_Servicio,
            'servicios':posts,
            'paginas':paginas,
            'pagina_actual':pagina_actual,
            "User":UserSesion,
            'cambios':cambiosQueryset,
            'footer':cambiosfQueryset
        }
        
        return render(request, self.template_name, context)
    
class AgregarServicioalCatalogo(View):
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
            formTipo_Servicio = EditarTipoServicioForm
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
