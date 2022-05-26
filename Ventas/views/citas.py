import smtplib
from datetime import datetime, timedelta, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from Configuracion.models import cambios, cambiosFooter
from Proyecto_Ekiria import settings
from Usuarios.models import Usuario
from .views import is_list_empty
from ..mixins import ActualiarCitaMixin, ActualiarCitaClienteMixin
from ..models import Cita, Pedido, Calendario
from ..forms import CitaForm
"""
<----------------------------------------------------------------->
Seccion de las Vistas donde se administran las citas
<----------------------------------------------------------------->
"""

class AgregarCita(TemplateView):
    template_name = "AgregarCita.html"
    def get_context_data(self, *args, **kwargs):
        context = super(AgregarCita, self).get_context_data(**kwargs)
        try:
            UserSesion=""
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                print("_______________________1")
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                    context["User"] = UserSesion
                    context['cambios']=cambiosQueryset
                    context['footer']=cambiosfQueryset
                    return context
                else:
                    return redirect("SinPermisos")
        except Exception as e:
            print("agendar cita")
            print(e)
        return context

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
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                    context["User"] = UserSesion
                    context['cambios']=cambiosQueryset
                    context['footer']=cambiosfQueryset
                    return context
                else:
                    return redirect("SinPermisos")
        except:
            return context
    
class EditarCitaDetalle(DetailView):
    model = Cita
    template_name = "DetalleEditarCita.html"
    form_class = CitaForm

    def get_context_data(self, *args, **kwargs):
        UserSesion = ""
        context = super(EditarCitaDetalle, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                
                UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                context["User"]=UserSesion
                context['cambios']=cambiosQueryset
                context['footer']=cambiosfQueryset
            else:
                return redirect("SinPermisos")
        except:
            return context


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

class EditarCita(ActualiarCitaMixin, UpdateView): 
    model = Cita
    template_name = "EditarCita.html"
    form_class = CitaForm
    success_url = reverse_lazy("Ventas:calendario")

    def get_context_data(self, *args, **kwargs):
        context = super(EditarCita, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                    context["User"]=UserSesion
                    context['cambios']=cambiosQueryset
                    context['footer']=cambiosfQueryset
                else:
                    return redirect("SinPermisos")  
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
      
        return context

    def post(self, request, *args, **kwargs):
        pass

class EditarCitaCliente(ActualiarCitaClienteMixin, UpdateView): 
    model = Cita
    template_name = "EditarCitaCliente.html"
    form_class = CitaForm
    success_url = reverse_lazy("Ventas:calendario")

    def get_context_data(self, *args, **kwargs):
        context = super(EditarCitaCliente, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                if self.request.session['Admin'] == True:
                    UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
                    context["User"]=UserSesion
                    context['cambios']=cambiosQueryset
                    context['footer']=cambiosfQueryset
                else:
                    return redirect("SinPermisos")  
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
      
        return context
    
class DetalleCitaCliente(DetailView):
    model = Cita
    template_name = "DetalleCitaCliente.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DetalleCitaCliente, self).get_context_data(**kwargs)
        try:
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
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
            try:
                update.estado=True
                update.save() 
                Servidor = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                Servidor.starttls()
                Servidor.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                print("conexion establecida")

                mensaje = MIMEMultipart()
                mensaje['From'] = settings.EMAIL_HOST_USER
                mensaje['To'] = update.cliente_id.email
                mensaje['Subject'] = "Correo de confirmación de cita"

                cliente = f"{str(update.cliente_id.nombres).capitalize()} {str(update.cliente_id.apellidos).capitalize()}"

                content = render_to_string("Correo/ConfirmarCitaCorreo.html", {"cliente":cliente, "dia":update.diaCita, "hora":update.horaInicioCita,"url":update.id_cita})
                mensaje.attach(MIMEText(content, 'html'))

                Servidor.sendmail(settings.EMAIL_HOST_USER,
                                  update.cliente_id.email,
                                  mensaje.as_string())

                print("Se envio el correo")
            except Exception as e:
                print(e)
        else:
            return redirect("Ventas:listarCitas")
        return HttpResponse(update)

class CancelarCita(View):
    model = Cita
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            cita = self.model.objects.get(id_cita=request.POST["cita"])
            cita.cancelado = True
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
                print(e)
        return HttpResponse("Se ha cancelado la cita")

class AgandarCita(CreateView):
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
            if self.request.session:
                imagen = Usuario.objects.get(id_usuario=self.request.session['pk'])
                imagen = imagen.img_usuario
                cambiosQueryset = cambios.objects.all()
                cambiosfQueryset = cambiosFooter.objects.all()
                UserSesion = {"username":self.request.session['username'], "rol":self.request.session['rol'], "imagen":imagen, "admin":self.request.session['Admin']}
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

        if horaInicio[-2:] == "PM":
            horaTipo = horaInicio[0:4].replace(":",",")
            print('desde :', horaTipo)
        elif horaInicio[-2:] == "AM":
            horaTipo = horaInicio[0:4].replace(":", ",")
            print('desde :', horaTipo)






        diaCita = request.POST["diaCita"]
        empleado = request.POST["empleado_id"]
        descripcion = request.POST["descripcion"]
        errores = {}
        if not horaInicio:
            errores["horaInicioCita"] = "Debe completar la hora de la cita."
        if not diaCita:
            errores["diaCita"] = "Debe completar el dia  de la cita."
        if not empleado:
            errores["empleado_id"] = "Debe seleccionar un empleado que atienda su cita."
    
        empleado = Usuario.objects.get(id_usuario=empleado)
        diaCita=datetime.strptime(diaCita, "%d/%m/%Y")
        diaCita=diaCita.strftime("%Y-%m-%d")
        diasConsulta = Calendario.objects.filter(empleado_id=empleado).filter(dia=diaCita)



        horasNoDisponibles={}
        cont=1

        for i in diasConsulta:
            horaIniciox = i.horaInicio.strftime("%H:%M")
            horaFinx = i.horaFin.strftime("%H:%M")
            cont=str(cont)
            horasNoDisponibles[str("cita"+cont)]={"horaInicio":horaIniciox,"horaFin":horaFinx}
            cont=int(cont)+1

        horas = [(time(i).strftime("%H:%M")) for i in range(24)]

       

        res = [x for x in horas if x  in [x for x in horas for i in horasNoDisponibles if (horasNoDisponibles[i]["horaInicio"] <= x <= horasNoDisponibles[i]["horaFin"])]]

        # for i in horas:
        #     if i 
        print(res)

        if errores:
            response = JsonResponse({"errores":errores})
            response.status_code = 400
            return response
        else:
            horaInicio=datetime.strptime(horaInicio, "%H:%M %p").strftime("%H:%M:%S")
            cliente=Usuario.objects.get(username=self.request.session['username'])
            pedido,creado = Pedido.objects.get_or_create(cliente_id=cliente, completado=False)
            datosParaGuardar = {"pedido_id":pedido,"horaInicioCita":horaInicio,"cliente_id":cliente, "empleado_id":empleado.pk,
            "descripcion":descripcion,"diaCita":diaCita}
            form = self.form_class(datosParaGuardar)
            if form.is_valid:
                object=form.save()
                calendarioSave = Calendario(dia=object.diaCita, horaInicio=object.horaInicioCita, horaFin=object.horaFinCita, cita_id=object, cliente_id=object.cliente_id, empleado_id=object.empleado_id)
                calendarioSave.save()
                form.save()
                pedido.completado = True
                pedido.save()
                datos = {}

                return redirect("Ventas:calendario")

            else:
                return render(request, self.template_name, {"form":self.form_class})

class BuscarDisponibilidadEmpleado(View):
    def post(self,request,*args,**kwargs):
        accion=request.POST["accion"]
        if accion == "BuscarEmpleado":
            empleado=request.POST["empleado"]
            agenda=Calendario.objects.filter(empleado_id=empleado)
            return JsonResponse({"empleado":empleado})

        elif accion == "BuscarDiaDeEmpleado":
            empleado=request.POST["empleado"]
            dia=request.POST["dia"]
            dia=datetime.strptime(dia, "%d/%m/%Y")
            dia=dia.strftime("%Y-%m-%d")
            diasConsulta = Calendario.objects.filter(empleado_id=empleado).filter(dia=dia)
            
            horasNoDisponibles={}
            cont=1
            for i in diasConsulta:
                horaInicio=i.horaInicio
                horaInicio = horaInicio.strftime("%H:%M")
                horaFin=i.horaFin
                horaFin = horaFin.strftime("%H:%M")
                horaFin = datetime.strptime(horaFin, "%H:%M") - datetime.strptime("01:00", "%H:%M")
                horaFin = datetime.strptime(str(horaFin), "%H:%M:%S")
                horaFin = horaFin.strftime("%H:%M")
                cont=str(cont)
                horasNoDisponibles[str("cita"+cont)]={"horaInicio":horaInicio,"horaFin":horaFin}
                cont=int(cont)
                cont+=1
           
            horas = hours = [(time(i).strftime("%H:%M")) for i in range(24)]

            if len(horasNoDisponibles)==0:
                res=horas
            else:
                res = [x for x in horas if x not in [x for x in horas for i in horasNoDisponibles if (horasNoDisponibles[i]["horaInicio"] <= x <= horasNoDisponibles[i]["horaFin"])]]

            print(res)

            return JsonResponse({"horasDisponibles":res})