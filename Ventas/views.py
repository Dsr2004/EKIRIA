from datetime import datetime, timedelta
import re

from sre_constants import SUCCESS
from statistics import mode
from webbrowser import get
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Usuarios.models import Usuario



from .forms import ServicioForm, Tipo_servicioForm, EditarTipoServicioForm,CatalogoForm, Servicio_PersonalizadoForm, CitaForm, pruebaxForm
from .models import *
from Ventas import models




def is_list_empty(list):
    if len(list) == 0:
        return True
    else:
        return False

"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administra el catalogo
<----------------------------------------------------------------->
"""

class Catalogo(ListView): 
    queryset = models.Catalogo.objects.filter(estado=True)
    context_object_name = "servicios"
    template_name = "Catalogo.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Catalogo, self).get_context_data(**kwargs)
        try:
           if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                return context
        except:
            return context
    

class AgregarServicioalCatalogo(View):
    model = Catalogo
    form_class =   CatalogoForm
    template_name = "Catalogo/AgregarServicio.html"
    def get(self, request, *args, **kwargs):
        servicesInCatalogo=models.Catalogo.objects.all()
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

        contexto={
            "form":self.form_class,
            "servicios":ServiciosNoEnCatalogo,
            "NoEnCatalogo":posts,
            'paginas':paginas,
            'pagina_actual':pagina_actual
        }

        return render(request, self.template_name, contexto)

    def post(self, request, *args, **kwargs):
        id = request.POST["id"]
        try:
            servicio = Servicio.objects.get(id_servicio=id)
            ServicioToCatalogo = models.Catalogo.objects.create(servicio_id=servicio)
            ServicioToCatalogo.save()
            return redirect("Ventas:adminVentas")
        except Exception as e: 
            formTipo_Servicio = EditarTipoServicioForm
            servicios=models.Catalogo.objects.all()

            paginado=Paginator(servicios, 5)
            pagina = request.GET.get("page") or 1
            posts = paginado.get_page(pagina)
            pagina_actual=int(pagina)
            paginas=range(1,posts.paginator.num_pages+1)
            #contexto
            contexto={
                'Tipo_Servicios':Tipo_servicio.objects.all(),
                'form_Tipo_Servicio':formTipo_Servicio,
                'servicios':posts,
                'paginas':paginas,
                'pagina_actual':pagina_actual,
                "errores": "No se puede realizar su solicitud, el error es: "+str(e)
            }

            return render(request, "Ventas.html", contexto)


def CambiarEstadoServicioEnCatalogo(request):
    if request.method == "POST":
        id = request.POST["estado"]
        update=models.Catalogo.objects.get(id_catalogo=id)
        estatus=update.estado
        if estatus==True:
            update.estado=False
            update.save()
        elif estatus==False:
            update.estado=True
            update.save()
        else:
            return redirect("Ventas:listarServicios")
        return HttpResponse(update)
    else:
        return redirect("Ventas:listarServicios")  


class QuitarServicioalCatalogo(DeleteView):
    pass


def Carrito(request):
    cliente=Usuario.objects.get(username=request.session['username'])
    if cliente:
        pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)
        items= pedido.pedidoitem_set.all()
        serviciosx=[]
        serviciosPerx=[]
        duracion=0
        cont=0
        for i in items:
            if not i.servicio_personalizado_id == None:
                cont+=1
        
        if cont <= 0:
            pedido.esPersonalizado = False
            pedido.save()
        cont=0
        
        for i in items:
            if not i.servicio_id ==  None:
                duracion=duracion+i.servicio_id.duracion
            if not i.servicio_personalizado_id == None:
                duracion=duracion+i.servicio_personalizado_id.duracion
        if items:
            for i in items:
                if not i.servicio_id ==  None:
                    serviciosx.append(i)
                if not i.servicio_personalizado_id == None:
                    serviciosPerx.append(i)
    
        request.session["carrito"]=pedido.get_items_carrito
        request.session["duracion"]=duracion
        
    else:
        items=[]
        pedido={"get_total_carrito":0,"get_items_carrito":0}
        request.session["carrito"]=0

    try:
        if request.session:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                if request.session['Admin'] == True:
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                else:
                    return redirect("SinPermisos")
    except:
            return redirect("UNR")

    contexto={"pedido":pedido,"User":UserSesion,"serviciosx":serviciosx,"serviciosPerx":serviciosPerx}

    return render(request, "Carrito.html",contexto)

class AgandarCita(CreateView):
    model = Cita
    form_class = CitaForm
    template_name = "TerminarPedido.html"
    success_url = reverse_lazy("Ventas:calendario")

    def get(self, request, *args,**kwargs):
        cliente=Usuario.objects.get(username=self.request.session['username'])
        if cliente:
            pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)
            items= pedido.pedidoitem_set.all()
            serviciosx=[]
            serviciosPerx=[]
            if items:
                for i in items:
                    if not i.servicio_id ==  None:
                        serviciosx.append(i)
                    if not i.servicio_personalizado_id == None:
                        serviciosPerx.append(i)  
            contexto={"items":items, "pedido":pedido,"form":self.form_class,"serviciosx":serviciosx,"serviciosPerx":serviciosPerx}
        else:
            items=[]
            pedido={"get_total_carrito":0,"get_items_carrito":0}
            contexto={"items":items, "pedido":pedido,"form":self.form_class}


        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                contexto["User"]=UserSesion

        except:
            pass

        if is_list_empty(items):
            contexto["mensaje"]=True
            return render(request, "Carrito.html",contexto)
        else:
            return render(request, "TerminarPedido.html",contexto)
    
    def post(self, request, *args, **kwargs):
        """
            esta parte de la hora de fin se debe hacer en el metodo save del modelo es mas facil en el video de los calendarios de developer.pe
            se explica muy bien 
        """
    
        # duracion = timedelta(minutes=duracion)
        # horaFin = horaInicio + duracion
        # horaFin = horaFin.strftime("%H:%M:%S")

        horaInicio = request.POST["horaInicioCita"]
        diaCita = request.POST["diaCita"]
        empleado = request.POST["empleado_id"]
        descripcion = request.POST["descripcion"]
        horaInicio=datetime.strptime(horaInicio, "%H:%M %p").strftime("%H:%M:%S")
        cliente=Usuario.objects.get(username=self.request.session['username'])
        pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)

        

        # request.POST["horaFinCita"]=horaFin
        

        datosParaGuardar = {"pedido_id":pedido,"horaInicioCita":horaInicio,"cliente_id":cliente, "empleado_id":empleado,
        "descripcion":descripcion,"diaCita":diaCita}
        form = self.form_class(datosParaGuardar)
        if form.is_valid:
            object=form.save()
            calendarioSave = models.Calendario(dia=object.diaCita, horaInicio=object.horaInicioCita, horaFin=object.horaFinCita, cita_id=object, cliente_id=object.cliente_id, empleado_id=object.empleado_id)
            calendarioSave.save()
            form.save()
            pedido.completado = True
            pedido.save()
            return redirect("Ventas:calendario")
        else:
            return render(request, self.template_name, {"form":self.form_class})
       
        
        
        return self.success_url
        # horaInicio = request.POST["horaInicioCita"]
        # horaInicio=datetime.strptime(horaInicio, "%H:%M %p").strftime("%H:%M:%S")

        # cliente=Usuario.objects.get(username=self.request.session['username'])
        # pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)

        # postViejo = request.POST._mutable
        # request.POST._mutable = True

        # request.POST["horaInicioCita"]=horaInicio
        # request.POST["cliente_id"]=cliente
        # request.POST["pedido_id"]=pedido
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     object=form.save()
        #     calendarioSave = models.Calendario(dia=object.diaCita, horaInicio=object.horaInicioCita, horaFin=object.horaFinCita, cita_id=object, cliente_id=object.cliente_id, empleado_id=object.empleado_id)
        #     calendarioSave.save()
        #     form.save()
        #     return redirect("Ventas:calendario")
        # else:
        #     cliente=Usuario.objects.get(username=self.request.session['username'])
        #     if cliente:
        #         pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)
        #         items= pedido.pedidoitem_set.all()
        #         serviciosx=[]
        #         serviciosPerx=[]
        #         if items:
        #             for i in items:
        #                 if not i.servicio_id ==  None:
        #                     serviciosx.append(i)
        #                 if not i.servicio_personalizado_id == None:
        #                     serviciosPerx.append(i)  
        #         contexto={"items":items, "pedido":pedido,"form":form,"serviciosx":serviciosx,"serviciosPerx":serviciosPerx}
        #     else:
        #         items=[]
        #         pedido={"get_total_carrito":0,"get_items_carrito":0}
        #         contexto={"items":items, "pedido":pedido,"form":form}


        #     try:
        #         if self.request.session:
        #             imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
        #             imagen = imagen.img_usuario
        #             UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen}
        #             contexto["User"]=UserSesion

        #     except:
        #         pass


        #     if is_list_empty(items):
        #         contexto["mensaje"]=True
        #         return render(request, "Carrito.html",contexto)
        #     else:
        #         return render(request, "TerminarPedido.html",contexto)
    
            
       
        
        
      
    


        # object = Servicio.objects.get(request.POST.get(""))
        # object.horafin = horaFin
        # object.save(    )
        

       
        


class BuscarDisponibilidadEmpleado(View):
    def post(self,request,*args,**kwargs):
        accion=request.POST["accion"]
        if accion == "BuscarEmpleado":
            empleado=request.POST["empleado"]
            agenda=models.Calendario.objects.filter(empleado_id=empleado)
            x= request.session["duracion"]
            return JsonResponse({"empleado":empleado})

        elif accion == "BuscarDiaDeEmpleado":
            empleado=request.POST["empleado"]
            dia=request.POST["dia"]
            dia=datetime.strptime(dia, "%d/%m/%Y")
            dia=dia.strftime("%Y-%m-%d")
            diasConsulta = models.Calendario.objects.filter(empleado_id=empleado).filter(dia=dia)
            
            horasNoDisponibles={}
            cont=1
            for i in diasConsulta:
                horaInicio=i.horaInicio
                horaInicio = horaInicio.strftime("%H:%M")
                horaFin=i.horaFin
                horaFin = horaFin.strftime("%H:%M")
                cont=str(cont)
                horasNoDisponibles[str("cita"+cont)]={"horaInicio":horaInicio,"horaFin":horaFin}
                cont=int(cont)
                cont+=1
                   
           
            horas = [
                "00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00",
                "15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00",
            ]

            if len(horasNoDisponibles)==0:
                res=horas
            else:
                for i in horasNoDisponibles:
                    res = [x for x in horas if (x < horasNoDisponibles[i]["horaInicio"] or x > horasNoDisponibles[i]["horaFin"])]

            return JsonResponse({"horasDisponibles":res})


    

class Calendario(TemplateView):
    template_name = "Calendario.html"
    def get(self, request, *args, **kwargs):
        try:
            if request.session:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                if request.session['Admin'] == True:
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                else:
                    return redirect("SinPermisos")
        except:
            return redirect("UNR")

        #contexto
        citas=models.Calendario.objects.filter(cliente_id=request.session['pk'])
        context={
            "User":UserSesion,
            "citas":citas
        }
        
        return render(request, self.template_name, context)

class ServiciosPersonalizados(CreateView):
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
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                return context
        except:
            return redirect("UNR")

    def form_valid(self, form, *args, **kwargs):
        objeto=form.save()
        cliente = Usuario.objects.get(username=self.request.session['username'])
        pedido,creado = models.Pedido.objects.get_or_create(cliente_id=cliente, completado=False)
        itemPedio = models.PedidoItem.objects.get_or_create(pedido_id=pedido,servicio_personalizado_id=objeto)
        pedido.esPersonalizado = True
        pedido.save()

        return redirect("Ventas:carrito")
        
class EditarServiciosPersonalizados(UpdateView):
    model = Servicio_Personalizado
    form_class = Servicio_PersonalizadoForm
    template_name = "Carrito/ActualizarServicioPer.html"
    success_url=reverse_lazy("Ventas:carrito")
"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administra el Admin de las ventas
<----------------------------------------------------------------->
"""

class AdminVentas(TemplateView):
    template_name = "Ventas.html"

    def get(self,request, *args, **kwargs):
        formTipo_Servicio = EditarTipoServicioForm
        servicios=models.Catalogo.objects.all()

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
                if request.session['Admin'] == True:
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                else:
                    return redirect("SinPermisos")
        except:
            return redirect("UNR")

        #contexto
        context={
            'Tipo_Servicios':Tipo_servicio.objects.all(),
            'form_Tipo_Servicio':formTipo_Servicio,
            'servicios':posts,
            'paginas':paginas,
            'pagina_actual':pagina_actual,
            "User":UserSesion,
        }
        
        return render(request, self.template_name, context)
    

"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administran los tipos de servicios
<----------------------------------------------------------------->
"""
class AgregarTipo_Servicio(CreateView):#crear
    model = Tipo_servicio
    form_class = Tipo_servicioForm
    template_name = "Tipo_Servicio/Tipo_servicioAdd.html"

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_TipoServicio = Tipo_servicio(
                    nombre = form.cleaned_data.get('nombre'),
                    estado = form.cleaned_data.get('estado')
                )
                nuevo_TipoServicio.save()
                mensaje = f"{self.model.__name__} registrado correctamente"
                error = "No hay error!"
                response = JsonResponse({"mensaje":mensaje, "error":error})
                response.status_code = 201
                return response
            else:
                errores=form.errors
                mensaje = f"{self.model.__name__} no se ha podido actualizar!"
                response = JsonResponse({"mensaje":mensaje, 'errors': errores})
                response.status_code = 400
                return response
        else:
            return redirect("Ventas:adminVentas")
            

class EditarTipo_Servicio(UpdateView):#actualziar
    model = Tipo_servicio
    form_class = Tipo_servicioForm
    template_name = "Tipo_Servicio/Tipo_servicio.html"

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f"{self.model.__name__} actualizado correctamente"
                error = "No hay error!"
                response = JsonResponse({"mensaje":mensaje, "error":error})
                response.status_code = 201
                return response
            else:
                errores=form.errors
                mensaje = f"{self.model.__name__} no se ha podido actualizar!"
                response = JsonResponse({"mensaje":mensaje, 'errors': errores})
                response.status_code = 400
                return response
        else:
            return redirect("Ventas:adminVentas")

class ElimininarTipoServicio(DeleteView):
    model = Tipo_servicio
    template_name = "Tipo_Servicio/EliminarTipoServicio.html"
    success_url = reverse_lazy("Ventas:adminVentas")


def CambiarEstadoTipoServicio(request):
    if request.method=="POST":
        id = request.POST["estado"]
        update=Tipo_servicio.objects.get(id_tipo_servicio=id)
        estatus=update.estado
        if estatus==True:
            update.estado=False
            update.save()
        elif estatus==False:
            update.estado=True
            update.save()
        else:
            return redirect("Ventas:adminVentas")
        return HttpResponse(update)
    else:
        return redirect("Ventas:adminVentas")

class ElimininarTipoServicio(DeleteView):#eliminar
    model = Tipo_servicio
    template_name = "Tipo_Servicio/EliminarTipoServicio.html"
    success_url = reverse_lazy("Ventas:adminVentas")

"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administran los servicios
<----------------------------------------------------------------->
"""

class AgregarServicio(CreateView):#crear
    model = Servicio
    form_class = ServicioForm
    template_name = "AgregarServicio.html"
    success_url = reverse_lazy('Ventas:listarServicios')
    def get(self, request, *args, **kwargs):
        try:
            if request.session:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                if request.session['Admin'] == True:
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                else:
                    return redirect("SinPermisos")
        except:
            return redirect("UNR")
    def form_valid(self, form, **kwargs):
        objeto=form.save()
        if objeto.estado == True:
            pk=int(objeto.id_servicio)
            ServicioToCatalogo = models.Catalogo.objects.create(servicio_id=objeto)
            ServicioToCatalogo.save()
        objeto.save()
        return redirect("Ventas:listarServicios")

class EditarServicio(UpdateView):#actualizar
    model = Servicio
    form_class = ServicioForm
    template_name = "EditarServicio.html" 
    success_url = reverse_lazy('Ventas:listarServicios')
    
    def get_context_data(self, *args, **kwargs):
        context = super(EditarServicio, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                return context
        except:
            return context
       
    def form_valid(self, form, **kwargs):
        objeto=form.save()
        if objeto.estado == False:
            QuitarServicioToCatalogo = models.Catalogo.objects.filter(servicio_id=objeto).delete()
        elif objeto.estado == True:
            ServicioToCatalogo = models.Catalogo.objects.create(servicio_id=objeto)
            ServicioToCatalogo.save()
        objeto.save()
        return redirect("Ventas:listarServicios")

class ListarServicio(ListView):#listar
    queryset = Servicio.objects.all()
    context_object_name = "servicios"
    template_name = "ListarServicios.html"
  
    def get_context_data(self, *args, **kwargs):
        context = super(ListarServicio, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
                context["User"]=UserSesion
                return context
        except:
            return context

class ServicioDetalle(DetailView):#detalle
    queryset = Servicio.objects.all()
    context_object_name = "DetailSs"
    template_name = "Catalogo/Detalle_Servicio.html"

def CambiarEstadoServicio(request):
    if request.method == "POST":
        id = request.POST["estado"]
        update=Servicio.objects.get(id_servicio=id)
        estatus=update.estado
        if estatus==True:
            update.estado=False
            QuitarServicioToCatalogo = models.Catalogo.objects.filter(servicio_id=update).delete()
            update.save()
        elif estatus==False:
            update.estado=True
            update.save()
            ServicioToCatalogo = models.Catalogo.objects.create(servicio_id=update)
            ServicioToCatalogo.save()
        else:
            return redirect("Ventas:listarServicios")
        return HttpResponse(update)
    else:
        return redirect("Ventas:listarServicios")

"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administran las citas
<----------------------------------------------------------------->
"""

class AgregarCita(TemplateView):
    template_name = "AgregarCita.html"
    def get(self, request, *args, **kwargs):
        try:
            if request.session:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                if request.session['Admin'] == True:
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                else:
                    return redirect("SinPermisos")
        except:
            return redirect("UNR")

class ListarCita(ListView):
    queryset = Cita.objects.all()
    context_object_name = "citas"
    template_name = "ListarCitas.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ListarCita, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
        except:
            return context
    
   
    
class EditarCitaDetalle(DetailView):
    model = Cita
    template_name = "DetalleEditarCita.html"
    form_class = CitaForm

    def get_context_data(self, *args, **kwargs):
        context = super(EditarCitaDetalle, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen}
                context["User"]=UserSesion
        
        except:
            pass
        citax = models.Cita.objects.get(id_cita=self.kwargs["pk"])
        pedido = models.Pedido.objects.get(id_pedido = citax.pedido_id.id_pedido)
        items = pedido.pedidoitem_set.all()
        serviciosx=[]
        serviciosPerx=[]
        if items:
            for i in items:
                if not i.servicio_id ==  None:
                    serviciosx.append(i)
                    context["servicios"]=serviciosx
                if not i.servicio_personalizado_id == None:
                    serviciosPerx.append(i)
                    context["serviciosPer"]=serviciosPerx
        hoy = datetime.today()
        diaCita = citax.diaCita
        tresDias =  datetime(diaCita.year, diaCita.month, diaCita.day) - timedelta(days=3)
        print(tresDias)
        print(diaCita)
        if hoy < tresDias:
            context["SePuedeModificar"] = True
        else:
            context["SePuedeModificar"] = False
        return context
class EditarCita(UpdateView):
    model = Cita
    template_name = "EditarCita.html"
    form_class = CitaForm

    def get_context_data(self, *args, **kwargs):
        context = super(EditarCita, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                else:
                    return redirect("SinPermisos")
        
        except:
            return redirect("UNR")
        citax = models.Cita.objects.get(id_cita=self.kwargs["pk"])
        pedido = models.Pedido.objects.get(id_pedido = citax.pedido_id.id_pedido)
        items = pedido.pedidoitem_set.all()
        serviciosx=[]
        serviciosPerx=[]
        if items:
            for i in items:
                if not i.servicio_id ==  None:
                    serviciosx.append(i)
                    context["servicios"]=serviciosx
                if not i.servicio_personalizado_id == None:
                    serviciosPerx.append(i)
                    context["serviciosPer"]=serviciosPerx
        return context
   

class DetalleCita(DetailView):
   template_name = "DetalleCita.html"
   def get(self, request, *args, **kwargs):
        try:
            if request.session:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                if request.session['Admin'] == True:
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
                else:
                    return redirect("SinPermisos")
        except:
            return redirect("UNR")

class CambiarEstadoDeCita(TemplateView):
   template_name = "DetalleCita.html"
   def post(self, request, *args, **kwargs):
        id = request.POST["estado"]
        update=Cita.objects.get(id_cita=id) 
        estatus=update.estado
        if estatus==True:
            update.estado=False
            update.save()
        elif estatus==False:
            update.estado=True
            update.save()
        else:
            return redirect("Ventas:listarCitas")
        return HttpResponse(update)

"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se realizan las pruebas
<----------------------------------------------------------------->
"""

def ejemplo(request, id):
    consuta=Servicio.objects.filter(id_servicio=id)

def pruebas(request):
    servicios=Servicio.objects.all()
    form=pruebaxForm
    try:
        if request.session:
            imagen = Usuario.objects.get(id_usuario=request.session['pk'])
            imagen = imagen.img_usuario
            if request.session['Admin'] == True:
                UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin']}
            else:
                return redirect("SinPermisos")
    except:
            return redirect("UNR")
    cont={
        "servicios":servicios,
        "form":form,
        "User":UserSesion
    }
    return render(request, 'prueba.html',cont)
