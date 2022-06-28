import json
import os
import smtplib
from datetime import datetime, timedelta, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import final
from xhtml2pdf import pisa

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles import finders

from Proyecto_Ekiria.Mixin.Mixin import PermissionDecorator, PermissionMixin
from Configuracion.models import cambios, cambiosFooter
from django.conf import settings
from Usuarios.views import if_admin
from Usuarios.models import Usuario
from Usuarios.views import if_User, if_admin

from Notificaciones.save import saveNotify

from .views import is_list_empty
from ..mixins import ActualiarCitaMixin, ActualiarCitaClienteMixin
from ..models import Cita, Pedido, Calendario, Servicio
from ..forms import CitaForm
from ..forms import CitaForm, Servicio_PersonalizadoForm

from ..Accesso import acceso
"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administran las citas
<----------------------------------------------------------------->
"""

#las variables en MAYUSCULAS SOSTENIDAS son las constantes no deben ser cambiadas
BUEN_FORMATO_FECHA = "%d/%m/%Y"
FORMATO_DJANGO = "%Y-%m-%d"

#funcion que convierte el formato de 12 horas a 24 horas
def conversor12a24(str1):

    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2] 
    elif str1[-2:] == "AM": 
        return str1[:-2] 
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]    
    else: 
        return  str(int(str1[:1]) + 12) + str1[1:5] 


class AgregarCita(TemplateView,PermissionMixin):
    permission_required = ['add_cita']
    template_name = "AgregarCita.html"
    form_class = CitaForm
    def get_context_data(self, *args, **kwargs):
        context = super(AgregarCita, self).get_context_data(**kwargs)
        try:
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"] = UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            context["form"] = self.form_class
            context["formPer"]=Servicio_PersonalizadoForm
            return context
        except Exception as e:
            print("desde Agregar cita: ", e)
        return context
    
    def post(self, request, *args, **kwargs):
        accion = request.POST.get("accion")
        errores ={}
        
        if accion == "BuscarUsuario":
            busqueda = request.POST.get("busqueda", "")
            if busqueda == "":
               errores["BuscarUsuario"] = "Este campo no puede estar vacío."
            else:
                data = []
                consulta = Usuario.objects.filter(Q(username__icontains=busqueda) |  Q(nombres=busqueda)  | Q(email__icontains=busqueda)).filter(estado=True).distinct()
                print(consulta)

                
                for i in consulta:
                    print(i)
                    item = i.toJSON()
                    respuesta = {"imagen":item["img"],"celular":item["celular"],"direccion":item["direccion"],"email":item["email"],"nombreUser":item["username"], "rol":i.rol.name}
                    respuesta["text"] = item["nombre_completo"]
                    respuesta["id"] = item["id_usuario"]
                    data.append(respuesta)
                return  JsonResponse(data, safe=False)
        elif accion == "BuscarServicio":
            busqueda = request.POST.get("busqueda", "")
            if busqueda == "":
               errores["BuscarServicio"] = "Este campo no puede estar vacío."
            else:
                data = []
                consulta = Servicio.objects.filter(Q(nombre__icontains=busqueda)).filter(estado=True).distinct()
                for i in consulta:
                    item = i.toJSON()
                    item["value"] = i.nombre
                    data.append(item)
                return  JsonResponse(data, safe=False)
        elif accion == "AgregarCita": 
            cita = json.loads(request.POST["cita"])
            print("ARCHIVOS",request.FILES)
            
            print(request.POST)
            cliente = cita["cliente"]
            empleado = cita["empleado"]
            # print(cita) 
            # print(empleado)
            return HttpResponse("hola") 
        return super(AgregarCita, self).get(request, *args, **kwargs)
               
class ListarCita(ListView,PermissionMixin):
    permission_required = ['view_cita']
    queryset = Cita.objects.all()
    context_object_name = "citas"
    template_name = "ListarCitas.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ListarCita, self).get_context_data(**kwargs)
        try:
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"] = UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            context["form"] = self.form_class
            return context
        except Exception as e:
            print("desde Agregar cita: ", e)
        return context
    
class EditarCitaDetalle(DetailView,PermissionMixin):
    permission_required = ['change_cita']
    model = Cita
    template_name = "DetalleEditarCita.html"
    form_class = CitaForm

    def get_context_data(self, *args, **kwargs):
        context = super(EditarCitaDetalle, self).get_context_data(**kwargs)
        try:
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"] = UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            context["form"] = self.form_class
        except Exception as e:
            print("desde Agregar cita: ", e)
        citax = Cita.objects.get(id_cita=self.kwargs["pk"])
        pedido = Pedido.objects.get(id_pedido = citax.pedido_id.id_pedido)
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
        if hoy < tresDias:
            context["SePuedeModificar"] = True
        else:
            context["SePuedeModificar"] = False

        if citax.cancelado == True:
            context["Cancelado"]=True
        else:
            context["Cancelado"]=False

        return context

class EditarCita(ActualiarCitaMixin, UpdateView,PermissionMixin): 
    permission_required = ['change_cita','view_cita','add_cita']
    model = Cita
    template_name = "EditarCita.html"
    form_class = CitaForm
    success_url = reverse_lazy("Ventas:calendario")

    def get_context_data(self, *args, **kwargs):
        context = super(EditarCita, self).get_context_data(**kwargs)
        try:
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"] = UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except Exception as e:
            print("desde Agregar cita: ", e) 
        citax = Cita.objects.get(id_cita=self.kwargs["pk"])
        pedido = Pedido.objects.get(id_pedido = citax.pedido_id.id_pedido)
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
    def post(self, request, *args, **kwargs):
        empleadoOriginal = self.get_object().empleado_id.id_usuario
        empleado = request.POST["empleado_id"]
        dia = request.POST["diaCita"]
        hora = request.POST["horaInicioCita"]
        descripcion = request.POST["descripcion"]
        hoy = datetime.now()
        hoy = hoy.strftime(BUEN_FORMATO_FECHA)
        hoy = datetime.strptime(hoy, BUEN_FORMATO_FECHA)
    
    
        errores = {}
        if not hora:
            errores["horaInicioCita"] = "Debe completar la hora de la cita."
        if not dia:
            errores["diaCita"] = "Debe completar el día  de la cita."
        if dia:
            try:
                dia=datetime.strptime(dia, BUEN_FORMATO_FECHA)
                if  dia < hoy:
                    errores["diaCita"] = "El día de la cita no puede ser menor al día actual."
            except:
                errores["diaCita"] = "El día de la cita no es válido."
        if not empleado:
            errores["empleado_id"] = "Debe seleccionar un empleado que atienda su cita."
       
        if errores:
            response = JsonResponse({"errores":errores})
            response.status_code = 400
            return response
        else:
            try:
                hora = datetime.strptime(hora, "%I:%M %p")
                hora = hora.time()
            except Exception as e:
                print(e)
                errores["horaInicioCita"]="La hora de la cita no es válida. {}".format(str(e))
                response = JsonResponse({"errores":errores})
                response.status_code = 400
                return response
            
            empleado = Usuario.objects.get(id_usuario=empleado)
            cita = self.model.objects.get(id_cita=self.get_object().id_cita)
            diaCita=dia.strftime("%Y-%m-%d")
            diasConsulta = Calendario.objects.filter(empleado_id=empleado).filter(dia=diaCita)
            horas = [(time(i).strftime("%H:%M")) for i in [8,9,10,11,12,13,14,15,16,17,18]]
            
            AM8 = time(8).strftime("%H:%M")
            AM8 = datetime.strptime(AM8, "%H:%M")
            PM6 = time(18).strftime("%H:%M")
            PM6 = datetime.strptime(PM6, "%H:%M")
            
            fin = datetime(1970, 1, 1, hora.hour, hora.minute, hora.second) + timedelta(minutes=cita.pedido_id.get_cantidad)
            fin = time(fin.hour, fin.minute, fin.second)
            
    
            if  not AM8.time() <= hora <=  PM6.time():
                errores["horaInicioCita"]="La hora de inicio debe estar entre las  8:00 AM y las 6:00 PM"
            elif not AM8.time() <= fin <=  PM6.time():
                errores["horaInicioCita"]="La hora de fin debe estar entre las  8:00 AM y las 6:00 PM, la duracion estimada es de {} minutos ,la hora de fin estimamda es {}".format(cita.pedido_id.get_cantidad, fin.strftime("%I:%M %p"))
            
            else:
                horasNoDisponibles={}
                cont=1
                for i in diasConsulta:
                    horaInicioC=i.horaInicio.strftime("%H:%M")
                    horaFinC=i.horaFin
                    horaFinC = datetime.strptime(str(horaFinC), "%H:%M:%S")
                    horaFinC = horaFinC.strftime("%H:%M")
                    cont=str(cont)
                    horasNoDisponibles[str("cita"+cont)]={"horaInicio":horaInicioC,"horaFin":horaFinC}
                    cont=int(cont)
                    cont+=1
                    
                iniciox = hora.strftime("%H:%M")
                finDatetime = datetime.strptime(iniciox, "%H:%M")
                finMinuto = finDatetime-timedelta(minutes=1)
                finMinuto = finMinuto.strftime("%H:%M")
                if not len(horasNoDisponibles)==0:
                    horasQuitadas = [x for x in horas for i in horasNoDisponibles if (horasNoDisponibles[i]["horaInicio"] <= x <= horasNoDisponibles[i]["horaFin"])]
                    for i in horasQuitadas:
                        if (iniciox <= i <= finMinuto):
                            errores["horaInicioCita"]="Ya existe una cita en esa hora, por favor seleccione otra hora"
                       
            if errores:
                response = JsonResponse({"errores":errores})
                response.status_code = 400
                return response
            else:
                cita.empleado_id = empleado
                cita.diaCita = dia
                cita.horaInicioCita = hora
                cita.horaFinCita = fin
                cita.descripcion = descripcion
                cita.estado = False
                
                if empleado.id_usuario == empleadoOriginal:# si el empleado es el mismo
                    verb = "{} {} Se han modificado los datos de una cita, debe confirmarla de nuevo".format(str(cita.empleado_id.nombres.capitalize()), str(cita.empleado_id.apellidos.capitalize()))
                    saveNotify(verb=verb,direct=cita.get_url_empleado,actor=cita,usuario=cita.empleado_id)
                   
                if empleado.id_usuario != empleadoOriginal: #diferente empleado
                    verb = "{} {} Se le ha asignado una nueva cita, debe confirmarla".format(str(cita.empleado_id.nombres.capitalize()), str(cita.empleado_id.apellidos.capitalize()))
                    saveNotify(verb=verb,direct=cita.get_url_empleado,actor=cita,usuario=cita.empleado_id)
                if saveNotify:
                    cita.save()  
                else:
                    print("no se modifico la cita")
                return redirect("Ventas:listarCitas")
    
class EditarCitaCliente(ActualiarCitaClienteMixin, UpdateView, PermissionMixin): 
    permission_required = ['change_cita','view_cita','add_cita']
    model = Cita
    template_name = "EditarCitaCliente.html"
    form_class = CitaForm
    success_url = reverse_lazy("Ventas:calendario")

    def get_context_data(self, *args, **kwargs):
        context = super(EditarCitaCliente, self).get_context_data(**kwargs)
        try:
            UserSesion = if_admin(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
            cambiosQueryset = cambios.objects.all() 
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"] = UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
        except Exception as e:
            print("desde Agregar cita: ", e)
        citax = Cita.objects.get(id_cita=self.kwargs["pk"])
        pedido = Pedido.objects.get(id_pedido = citax.pedido_id.id_pedido)
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
        form = self.form_class(instance=citax)
        form["horaInicioCita"].initial = citax.horaInicioCita.strftime("%I:%M %p")
        context["form"]=form
        return context
    
    def post(self, request, *args, **kwargs):
        empleadoOriginal = self.get_object().empleado_id.id_usuario
        empleado = request.POST["empleado_id"]
        dia = request.POST["diaCita"]
        hora = request.POST["horaInicioCita"]
        descripcion = request.POST["descripcion"]
        hoy = datetime.now()
        hoy = hoy.strftime(BUEN_FORMATO_FECHA)
        hoy = datetime.strptime(hoy, BUEN_FORMATO_FECHA)
    
    
        errores = {}
        if not hora:
            errores["horaInicioCita"] = "Debe completar la hora de la cita."
        if not dia:
            errores["diaCita"] = "Debe completar el día  de la cita."
        if dia:
            try:
                dia=datetime.strptime(dia, BUEN_FORMATO_FECHA)
                if  dia < hoy:
                    errores["diaCita"] = "El día de la cita no puede ser menor al día actual."
            except:
                errores["diaCita"] = "El día de la cita no es válido."
        if not empleado:
            errores["empleado_id"] = "Debe seleccionar un empleado que atienda su cita."
       
        if errores:
            response = JsonResponse({"errores":errores})
            response.status_code = 400
            return response
        else:
            try:
                hora = datetime.strptime(hora, "%I:%M %p")
                hora = hora.time()
            except Exception as e:
                print(e)
                errores["horaInicioCita"]="La hora de la cita no es válida. {}".format(str(e))
                response = JsonResponse({"errores":errores})
                response.status_code = 400
                return response
            
            empleado = Usuario.objects.get(id_usuario=empleado)
            cita = self.model.objects.get(id_cita=self.get_object().id_cita)
            diaCita=dia.strftime("%Y-%m-%d")
            diasConsulta = Calendario.objects.filter(empleado_id=empleado).filter(dia=diaCita)
            horas = [(time(i).strftime("%H:%M")) for i in [8,9,10,11,12,13,14,15,16,17,18]]
            
            AM8 = time(8).strftime("%H:%M")
            AM8 = datetime.strptime(AM8, "%H:%M")
            PM6 = time(18).strftime("%H:%M")
            PM6 = datetime.strptime(PM6, "%H:%M")
            
            fin = datetime(1970, 1, 1, hora.hour, hora.minute, hora.second) + timedelta(minutes=cita.pedido_id.get_cantidad)
            fin = time(fin.hour, fin.minute, fin.second)
            
    
            if  not AM8.time() <= hora <=  PM6.time():
                errores["horaInicioCita"]="La hora de inicio debe estar entre las  8:00 AM y las 6:00 PM"
            elif not AM8.time() <= fin <=  PM6.time():
                errores["horaInicioCita"]="La hora de fin debe estar entre las  8:00 AM y las 6:00 PM, la duracion estimada es de {} minutos ,la hora de fin estimamda es {}".format(cita.pedido_id.get_cantidad, fin.strftime("%I:%M %p"))
            
            else:
                horasNoDisponibles={}
                cont=1
                for i in diasConsulta:
                    horaInicioC=i.horaInicio.strftime("%H:%M")
                    horaFinC=i.horaFin
                    horaFinC = datetime.strptime(str(horaFinC), "%H:%M:%S")
                    horaFinC = horaFinC.strftime("%H:%M")
                    cont=str(cont)
                    horasNoDisponibles[str("cita"+cont)]={"horaInicio":horaInicioC,"horaFin":horaFinC}
                    cont=int(cont)
                    cont+=1
                    
                iniciox = hora.strftime("%H:%M")
                finDatetime = datetime.strptime(iniciox, "%H:%M")
                finMinuto = finDatetime-timedelta(minutes=1)
                finMinuto = finMinuto.strftime("%H:%M")
                if not len(horasNoDisponibles)==0:
                    horasQuitadas = [x for x in horas for i in horasNoDisponibles if (horasNoDisponibles[i]["horaInicio"] <= x <= horasNoDisponibles[i]["horaFin"])]
                    for i in horasQuitadas:
                        if (iniciox <= i <= finMinuto):
                            errores["horaInicioCita"]="Ya existe una cita en esa hora, por favor seleccione otra hora"
                       
            if errores:
                response = JsonResponse({"errores":errores})
                response.status_code = 400
                return response
            else:
                cita.empleado_id = empleado
                cita.diaCita = dia
                cita.horaInicioCita = hora
                cita.horaFinCita = fin
                cita.descripcion = descripcion
                cita.estado = False
                
                if empleado.id_usuario == empleadoOriginal:# si el empleado es el mismo
                    verb = "{} {} Se han modificado los datos de una cita, debe confirmarla de nuevo".format(str(cita.empleado_id.nombres.capitalize()), str(cita.empleado_id.apellidos.capitalize()))
                    saveNotify(verb=verb,direct=cita.get_url_empleado,actor=cita,usuario=cita.empleado_id)
                   
                if empleado.id_usuario != empleadoOriginal: #diferente empleado
                    verb = "{} {} Se le ha asignado una nueva cita, debe confirmarla".format(str(cita.empleado_id.nombres.capitalize()), str(cita.empleado_id.apellidos.capitalize()))
                    saveNotify(verb=verb,direct=cita.get_url_empleado,actor=cita,usuario=cita.empleado_id)
                if saveNotify:
                    cita.save()  
                else:
                    print("no se modifico la cita")
                return redirect("Ventas:calendario")
      
class DetalleCitaCliente(DetailView,PermissionMixin):
    permission_required = ['change_cita','view_cita','add_cita']
    model = Cita
    template_name = "DetalleCitaCliente.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DetalleCitaCliente, self).get_context_data(**kwargs)
        try:
            UserSesion = if_User(self.request)
            if UserSesion == False:
                return redirect("IniciarSesion")
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
        except:
            return redirect("IniciarSesion")

        citax = Cita.objects.get(id_cita=self.kwargs["pk"])
        pedido = Pedido.objects.get(id_pedido = citax.pedido_id.id_pedido)
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
        if hoy < tresDias:
            context["SePuedeModificar"] = True
        else:
            context["SePuedeModificar"] = False

        if citax.cancelado == True:
            context["Cancelado"]=True
        else:
            context["Cancelado"]=False

        return context
    
class DetalleCitaCalendario(DetailView):
    model = Cita
    template_name = "Calendario/DetalleCitaCalendario.html"

class CambiarEstadoDeCita(TemplateView,PermissionMixin):
    permission_required = ['delete_cita']
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
            verb = "{} {} Su cita se ha confirmado, vea los detalles en el botón verde".format(str(update.cliente_id.nombres.capitalize()), str(update.cliente_id.apellidos.capitalize()))
            saveNotify(verb=verb,direct=update.get_url_cliente, actor=update,usuario=update.cliente_id)
            if saveNotify:
                update.save()
            else:
                print("no se confirmo la cita")
                
        else:
            return redirect("Ventas:listarCitas")
        return HttpResponse(update)

class CancelarCita(View,PermissionMixin):
    permission_required = ['delete_cita']
    model = Cita
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            cita = self.model.objects.get(id_cita=request.POST["cita"])
            cita.cancelado = True
            cita.estado=False
            cita.save()
            try:
                Servidor = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                Servidor.starttls()
                Servidor.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                print("conexion establecida")

                mensaje = MIMEMultipart()
                mensaje['From'] = settings.EMAIL_HOST_USER
                mensaje['To'] = cita.cliente_id.email
                mensaje['Subject'] = "Su cita se ha cancelado"

                cliente = f"{str(cita.cliente_id.nombres).capitalize()} {str(cita.cliente_id.apellidos).capitalize()}"

                content = render_to_string("Correo/CancelarCitaCorreo.html", {"cliente":cliente, "dia":cita.diaCita, "hora":cita.horaInicioCita,"url":cita.id_cita})
                mensaje.attach(MIMEText(content, 'html'))

                Servidor.sendmail(settings.EMAIL_HOST_USER,
                                  cita.cliente_id.email,
                                  mensaje.as_string())

                print("Se envio el correo")
            except Exception as e:
                print("DESDE CANCELAR CITA: ", e)
        return HttpResponse("Se ha cancelado la cita")

class AgandarCita(CreateView,PermissionMixin):
    permission_required = ['add_cita']
    model = Cita
    form_class = CitaForm
    template_name = "TerminarPedido.html"
    success_url = reverse_lazy("Ventas:calendario")

    def get(self, request, *args,**kwargs):
        try: 
            username = self.request.session['username']
            cliente=Usuario.objects.get(username=username)
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
        except: 
            return redirect("IniciarSesion")

        try:
            UserSesion = if_User(request)
            if UserSesion == False:
                return redirect("IniciarSesion")
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            contexto["User"]=UserSesion
            contexto["User"]=UserSesion
            contexto['cambios']=cambiosQueryset
            contexto['footer']=cambiosfQueryset

        except:
            pass

        if is_list_empty(items):
            contexto["mensaje"]=True
            return render(request, "Carrito.html",contexto)
        else:
            return render(request, "TerminarPedido.html",contexto)
    
    def post(self, request, *args, **kwargs):
        horaInicio = request.POST["horaInicioCita"]
        diaCita = request.POST["diaCita"]
        empleado = request.POST["empleado_id"]
        descripcion = request.POST["descripcion"]
        hoy = datetime.now()
        hoy = hoy.strftime(BUEN_FORMATO_FECHA)
        hoy = datetime.strptime(hoy, BUEN_FORMATO_FECHA)
        
       
        
        errores = {}
        if not horaInicio:
            errores["horaInicioCita"] = "Debe completar la hora de la cita."
        if not diaCita:
            errores["diaCita"] = "Debe completar el día  de la cita."
        if diaCita:
            try:
                diaCita=datetime.strptime(diaCita, BUEN_FORMATO_FECHA)
                if  diaCita < hoy:
                    errores["diaCita"] = "El día de la cita no puede ser menor al día actual."
            except:
                errores["diaCita"] = "El día de la cita no es válido."
        if not empleado:
            errores["empleado_id"] = "Debe seleccionar un empleado que atienda su cita."
  
        if errores:
            response = JsonResponse({"errores":errores})
            response.status_code = 400
            return response
        else:
            empleado = Usuario.objects.get(id_usuario=empleado)
            try:
                horaInicio = conversor12a24(horaInicio)
            except:
                errores["horaInicioCita"]="La hora de la cita no es válida."
                response = JsonResponse({"errores":errores})
                response.status_code = 400
                return response
            cliente=Usuario.objects.get(username=self.request.session['username'])
            pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)

            datosParaGuardar = {"pedido_id":pedido,"horaInicioCita":horaInicio,"cliente_id":cliente, "empleado_id":empleado.pk,
            "descripcion":descripcion,"diaCita":diaCita}
            form = self.form_class(datosParaGuardar)
            try:
                if form.is_valid():
                    object=form.save()
                    calendarioSave = Calendario(dia=object.diaCita, horaInicio=object.horaInicioCita, horaFin=object.horaFinCita, cita_id=object, cliente_id=object.cliente_id, empleado_id=object.empleado_id)
                    calendarioSave.save()
                    form.save()
                    pedido.completado = True
                    pedido.save()
                    return redirect("Ventas:calendario")

            except Exception as e:
                errores["horaInicioCita"]=str(e)
                response = JsonResponse({"errores":errores})
                response.status_code = 400
                return response

class BuscarDisponibilidadEmpleado(View):
    permission_required = ['view_calendario']
    def post(self,request,*args,**kwargs):
        accion=request.POST["accion"]
        if accion == "BuscarEmpleado":
            empleado=request.POST["empleado"]
            return JsonResponse({"empleado":empleado})

        elif accion == "BuscarDiaDeEmpleado":
            empleado=request.POST["empleado"]
            dia=request.POST["dia"]
            dia=datetime.strptime(dia, BUEN_FORMATO_FECHA)
            dia=dia.strftime(FORMATO_DJANGO )
            diasConsulta = Calendario.objects.filter(empleado_id=empleado).filter(dia=dia)
            
            horasNoDisponibles={}
            cont=1
            if diasConsulta:
                for i in diasConsulta:
                    cita = i.cita_id
                    if cita.cancelado == False:
                        horaInicio=i.horaInicio
                        horaInicio = horaInicio.strftime("%H:%M")
                        horaFin=i.horaFin
                        minuto = horaFin.minute
                        if minuto == 0:
                            horaFin = horaFin.strftime("%H:%M")
                            horaFin = datetime.strptime(horaFin, "%H:%M") - datetime.strptime("01:00", "%H:%M")
                        elif minuto >=20:
                            minuto = 60-minuto
                            horaFin = datetime(1970, 1, 1, horaFin.hour, horaFin.minute, horaFin.second) + timedelta(minutes=minuto)           
                            horaFin = time(horaFin.hour, horaFin.minute, horaFin.second)
                        elif minuto>0 and minuto<20:
                            horaFin = datetime(1970, 1, 1, horaFin.hour, horaFin.minute, horaFin.second) - timedelta(minutes=minuto)           
                            horaFin = time(horaFin.hour, horaFin.minute, horaFin.second)
                            
                        horaFin = datetime.strptime(str(horaFin), "%H:%M:%S")
                        horaFin = horaFin.strftime("%H:%M")
                        cont=str(cont)
                        horasNoDisponibles[str("cita"+cont)]={"horaInicio":horaInicio,"horaFin":horaFin}
                        cont=int(cont)
                        cont+=1
            horas = [(time(i).strftime("%H:%M")) for i in [8,9,10,11,12,13,14,15,16,17,18]]
            if len(horasNoDisponibles)==0:
                res=horas
            else:
                res = [x for x in horas if x not in [x for x in horas for i in horasNoDisponibles if (horasNoDisponibles[i]["horaInicio"] <= x <= horasNoDisponibles[i]["horaFin"])]]
                
            return JsonResponse({"horasDisponibles":res})

class BuscarDisponibilidadEmpleadoEditarCita(View):
    permission_required = ['view_calendario']
    def post(self,request,*args,**kwargs):
        accion=request.POST["accion"]
        if accion == "BuscarEmpleado":
            empleado=request.POST["empleado"]
            return JsonResponse({"empleado":empleado})

        elif accion == "BuscarDiaDeEmpleado":
            empleado=request.POST["empleado"]
            dia=request.POST["dia"]
            id_cita = request.POST["id_cita"]
            dia=datetime.strptime(dia, BUEN_FORMATO_FECHA)
            dia=dia.strftime(FORMATO_DJANGO )
            diasConsulta = Calendario.objects.filter(empleado_id=empleado).filter(dia=dia)
            
            horasNoDisponibles={}
            cont=1
            if diasConsulta:
                for i in diasConsulta:
                    cita = i.cita_id
                    if cita.cancelado == False and cita.pk != int(id_cita):
                        horaInicio=i.horaInicio
                        horaInicio = horaInicio.strftime("%H:%M")
                        horaFin=i.horaFin
                        minuto = horaFin.minute
                        if minuto == 0:
                            horaFin = horaFin.strftime("%H:%M")
                            horaFin = datetime.strptime(horaFin, "%H:%M") - datetime.strptime("01:00", "%H:%M")
                        elif minuto >=20:
                            minuto = 60-minuto
                            horaFin = datetime(1970, 1, 1, horaFin.hour, horaFin.minute, horaFin.second) + timedelta(minutes=minuto)           
                            horaFin = time(horaFin.hour, horaFin.minute, horaFin.second)
                        elif minuto>0 and minuto<20:
                            horaFin = datetime(1970, 1, 1, horaFin.hour, horaFin.minute, horaFin.second) - timedelta(minutes=minuto)           
                            horaFin = time(horaFin.hour, horaFin.minute, horaFin.second)
                            
                        horaFin = datetime.strptime(str(horaFin), "%H:%M:%S")
                        horaFin = horaFin.strftime("%H:%M")
                        cont=str(cont)
                        horasNoDisponibles[str("cita"+cont)]={"horaInicio":horaInicio,"horaFin":horaFin}
                        cont=int(cont)
                        cont+=1

            horas = [(time(i).strftime("%H:%M")) for i in [8,9,10,11,12,13,14,15,16,17,18]]

            if len(horasNoDisponibles)==0:
                res=horas
            else:
                res = [x for x in horas if x not in [x for x in horas for i in horasNoDisponibles if (horasNoDisponibles[i]["horaInicio"] <= x <= horasNoDisponibles[i]["horaFin"])]]
                
            return JsonResponse({"horasDisponibles":res})

class CitasReportePDF(View):
    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL 
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
                return uri

        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path
    
    def get(self,request,*args,**kwargs):
        citas=Cita.objects.filter(empleado_id=request.session['pk']).filter(diaCita=datetime.now().date()).filter(estado=1)
        empleado=Usuario.objects.get(pk=request.session['pk'])
        try:
            template = get_template('Reportes/citas_hoy.html')
            context = {"citas":citas, "hoy":datetime.now(), "empleado":empleado}
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response["Content-Disposition"] = 'attachment; filename="citas_hoy.pdf"'
            pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        messages.add_message(request, messages.INFO, 'Ocurrió un error al generar el PDF.')
        return HttpResponseRedirect(reverse_lazy("Ventas:calendarioEmpleado"))
    
    def post(self,request,*args,**kwargs):
        accion = request.POST.get("accion", "")

        if accion == "":
            print("si hay accion")
        else:
            messages.add_message(request, messages.INFO, 'Ocurrió un error al generar el PDF.')
            return HttpResponseRedirect(reverse_lazy("Ventas:calendarioEmpleado"))
        return HttpResponse("sfdsdsds")
        # if accion != "":
        #     if accion == "GenerarReporte":
        #         inicio = request.POST.get("fechaInicio", "")
        #         fin= request.POST.get("fechaFin", "")
                
        #         citas = Cita.objects.all()
        #         empleado=Usuario.objects.get(pk=request.session['pk'])
        #         if len(inicio) and len(fin):
        #             citas = citas.filter(diaCita__range=[inicio, fin])
        #             try:
        #                 template = get_template('Reportes/empleadoPersonalizado.html')
        #                 context = {"citas":citas, "hoy":datetime.now(), "empleado":empleado}
        #                 html = template.render(context)
        #                 response = HttpResponse(content_type='application/pdf')
        #                 response["Content-Disposition"] = 'attachment; filename="Reporte_Personalizado.pdf"'
        #                 pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
        #                 return response
        #             except:
        #                 pass
        #             respone = JsonResponse({"error":"Sin herror creado correctamente"})
        #             respone.status_code = 200
        #             return respone
        #     else:
        #         return HttpResponse(request.POST["fechaInicio"])
        # else:
        #     response = JsonResponse({"error":"No se ha recibido ninguna acción"})
        #     response.status_code = 400
        #     return response