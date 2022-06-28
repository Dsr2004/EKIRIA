#-----------------------------------------Imports---------------------------------------------------
import smtplib
import json
# prueba
from Proyecto_Ekiria import settings
# -----
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string

#-----------------------------------------Django---------------------------------------------------
from django.http import HttpResponseRedirect, request, HttpResponse, JsonResponse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission,Group
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

#-----------------------------------------Rest Framework---------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from Usuarios.authentication import ExpiringTokenAuthentication
#-----------------------------------------Serializers---------------------------------------------------
from Proyecto_Ekiria import settings
#-----------------------------------------Models---------------------------------------------------
from Usuarios.models import Usuario, VistasDiarias
from Ventas.models import Servicio
from Configuracion.models import cambiosFooter, cambios
#-----------------------------------------More---------------------------------------------------
from Usuarios.authentication_mixins import Authentication
from datetime import datetime
from Usuarios.forms import Cambiar, Regitro, Editar, CustomAuthForm, EditUser
from Usuarios.Mixins.Mixin import Asimetric_Cipher,if_admin
from Proyecto_Ekiria.settings.production import Public_Key
import cryptocode
from Proyecto_Ekiria.Mixin.Mixin import PermissionDecorator, PermissionMixin
from Notificaciones.models import Notificacion
#--------------------------------------Templates Loaders------------------------------------

@login_required()
def Loguot(request):
    logout(request)
    return redirect('Inicio')

def if_User(request):
    UserSesion=""
    if request.session:
        try:
            if request.session['pk']:
                imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                imagen = imagen.img_usuario
                UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "admin":request.session['Admin'],"imagen":imagen, "notify":request.session['notificaciones']}
                return UserSesion
        except:
            return False

def if_admin(request):
    UserSesion=""
    if request.session:
        try:
            if request.session['pk']:
                if request.user.administrador:
                    imagen = Usuario.objects.get(id_usuario=request.session['pk'])
                    imagen = imagen.img_usuario
                    UserSesion = {"username":request.session['username'], "rol":request.session['rol'], "imagen":imagen, "admin":request.session['Admin'],"notify":request.session['notificaciones']}
                    return UserSesion
                else:
                    return False
        except:
            return False

def Login(request):
    Error = ""
    if request.method == "POST":
        try:
            form = CustomAuthForm(request, data=request.POST)
            if form.is_valid():
                username= form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = Usuario.objects.get(username = username)
                if user.administrador:
                    user.rol_id = 1
                    user.save()
                try:
                    if user.rol.permissions.get(codename="Administrador"):
                        user.administrador = 1
                        user.save()
                except:
                    pass
                usuario = authenticate(username=username, password=password)
                if usuario is not None:
                    if usuario.estado:
                        notificaciones = Notificacion.objects.filter(usuario_id = usuario).filter(leido=False).count()
                        if notificaciones > 0:
                            request.session['notificaciones'] = notificaciones
                        else:
                            request.session['notificaciones'] = 0
                        login(request, usuario)
                        request.session['username'] = usuario.username
                        request.session['rol']= usuario.rol.name
                        request.session['pk'] = usuario.id_usuario
                        if usuario.administrador:
                            request.session['Admin'] = 1
                        else:
                            try:
                                if user.rol.permissions.get(codename="Empleado"):
                                    request.session['Admin'] = 2
                            except:
                                 request.session['Admin'] = 3
                        if 'next' in request.POST:
                            return redirect(request.POST.get('next'))
                        else:
                            return redirect("Inicio")
                    else:
                        Error = "Este Usuario se encuentra inhabilitado"
                else:
                    Error = "El Usuario o la contraseña no son correctos"
            else:
                Error = "Los datos ingresados no son correctos.\n si no tienes un usuario puedes registrarte."
        except Exception as e:
            print(e)
            
    form = CustomAuthForm()

    return render(request, "registration/login.html", {'form': form, 'message':Error})


class Register(CreateView):
    model = Usuario
    form_class = Regitro
    template_name = 'registration/Registration.html'
    success_url = reverse_lazy("IniciarSesion")
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        context = {
            'form':form,
        }
        if form.is_valid():
            try:
                form.estado = 0
                form.save()
                user = Usuario.objects.get(username = request.POST['username'])
                try:
                    token = Token.objects.get(user=user)
                    token.delete()
                    token = Token.objects.create(user=user)
                except:
                    Token.objects.create(user=user)
                    token = Token.objects.get(user=user)
                Servidor = smtplib.SMTP(settings.production.EMAIL_HOST, settings.production.EMAIL_PORT)
                Servidor.starttls()
                Servidor.login(settings.production.EMAIL_HOST_USER, settings.production.EMAIL_HOST_PASSWORD)
                print("conexion establecida")
                mensaje = MIMEMultipart()
                mensaje['From'] = settings.production.EMAIL_HOST_USER
                mensaje['To'] = user.email
                mensaje['Subject'] = "Confirme su correo"
                cliente = f"{str(user.nombres).capitalize()} {str(user.apellidos).capitalize()}"
                key = token.key
                value = cryptocode.encrypt(str(key),Public_Key)
                content = render_to_string("Correo/ConfirmarCuenta.html",
                                            {"cliente": cliente, "token":value, 'dominio':settings.production.Domain, 'footer':cambiosFooter.objects.all()})
                mensaje.attach(MIMEText(content, 'html'))

                Servidor.sendmail(settings.production.EMAIL_HOST_USER,
                                  user.email,
                                  mensaje.as_string())

                print("Se envio el correo")
                success = "Se ha enviado el correo correctamente al email "+user.email
                return redirect('IniciarSesion')
            except:
                nombre = request.POST.getlist("nombres","")[0]
                username = request.POST.getlist('username',"")[0]
                apellidos = request.POST.getlist('apellidos',"")[0]
                telefono = request.POST.getlist('telefono',"")[0]
                celular = request.POST.getlist('celular',"")[0]
                email = request.POST.getlist('email',"")[0]
                num_documento = request.POST.getlist('num_documento',"")[0]
                direccion = request.POST.getlist('direccion',"")[0]
                cod_postal = request.POST.getlist('cod_postal',"")[0]
                municipio = request.POST.getlist('municipio',"")[0]
                tipo_documento = request.POST.getlist('tipo_documento',"")[0]
                fec_nac = request.POST.getlist('fec_nac', "")[0]

                context['nombre']=nombre
                context['username']=username
                context['apellidos']=apellidos
                context['telefono']=telefono
                context['celular']=celular
                context['email']=email
                context['num_documento']=num_documento
                context['direccion']=direccion
                context['cod_postal']=cod_postal
                context['municipio']=municipio
                context['tipo_documento']=tipo_documento
                context["fec_nac"]= fec_nac

                context['errors'] = form.errors
                context['Error'] = 'No se pudo enviar el correo'
                return render(request, self.template_name, context)
        else:
            nombre = request.POST.getlist("nombres","")[0]
            username = request.POST.getlist('username',"")[0]
            apellidos = request.POST.getlist('apellidos',"")[0]
            telefono = request.POST.getlist('telefono',"")[0]
            celular = request.POST.getlist('celular',"")[0]
            email = request.POST.getlist('email',"")[0]
            num_documento = request.POST.getlist('num_documento',"")[0]
            direccion = request.POST.getlist('direccion',"")[0]
            cod_postal = request.POST.getlist('cod_postal',"")[0]
            municipio = request.POST.getlist('municipio',"")[0]
            tipo_documento = request.POST.getlist('tipo_documento',"")[0]
            fec_nac = request.POST.getlist('fec_nac', "")[0]

            context['nombre']=nombre
            context['username']=username
            context['apellidos']=apellidos
            context['telefono']=telefono
            context['celular']=celular
            context['email']=email
            context['num_documento']=num_documento
            context['direccion']=direccion
            context['cod_postal']=cod_postal
            context['municipio']=municipio
            context['tipo_documento']=tipo_documento
            context["fec_nac"]= fec_nac

            context['errors'] =  form.errors
            context['Error']= 'Los datos ingresados son incorrectos'
        return render(request, self.template_name, context)

  
class ConfirmarCuenta(TemplateView):
    template_name = "registration/ConfirmarCuenta.html"
    def get(self, request, *args, **kwargs):
        if request.user.pk is not None:
            return redirect('Inicio')
        user = ""
        context={}
        user_token_expired = None
        if request.GET['Slug']:
            slug = request.GET['Slug'].replace(" ", "+")
            key = cryptocode.decrypt(slug, Public_Key)
            token_expired = ExpiringTokenAuthentication()
            user,token,message, self.user_token_expired = token_expired.authenticate_credentials(key)
            if user != None and token != None:
                    token = Token.objects.get(key = token)
                    token.delete()
                    context={'User':user}
            else:
                context={
                    'message':'Esté link no se puede usar'
                }
            return render(request, self.template_name, context)
        else: 
            return redirect('IniciarSesion')

    def post(self,request,*args,**kwargs):
        if request.POST['user'] != '':
            user = Usuario.objects.get(pk=request.POST['user'])
            try:
                user.estado=True
                user.save()
                return redirect('IniciarSesion')
            except:
                data = json.dumps({'error': 'No se pudo cambiar el estado de tu usuario. Intentalo nuevamente'})
                return HttpResponse(data, content_type="application/json", status=400)
        else:
            data = json.dumps({'error': 'No se pudo identificar al usuario'})
            return HttpResponse(data, content_type="application/json", status=400)

@login_required()
def Perfil(request):
    UserSesion = if_User(request)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    usuario = Usuario.objects.get(id_usuario=request.session['pk'])
    return render(request, "UserInformation/Perfil.html", {"Usuario":usuario, "User":UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})



@login_required()
def EditarPerfil(request):  
    template_name = "UserInformation/EditarPerfil.html"
    UserSesion = if_User(request)
    if UserSesion == False:
        return redirect("IniciarSesion")
    get_object = Usuario.objects.get(id_usuario=request.session['pk'])
    form = Editar(instance=get_object)
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    if request.method=="POST":
        form = Editar(request.POST or None, request.FILES or None, instance=get_object)
        if form.is_valid():
            form.save()
            return redirect("Perfil")
        else:
            e=form.errors
            return JsonResponse({"x":e})
    return render(request, template_name, {"form":form, "User":UserSesion, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
    
@login_required()
@PermissionDecorator(['add_usuario','change_usuario', 'delete_usuario', 'view_usuario'])
def Change(request):
    UserSesion = if_User(request)
    if UserSesion == False:
        return redirect("IniciarSesion")
    get_object = Usuario.objects.get(id_usuario=request.session['pk'])
    form = Cambiar(instance=get_object)
    imagen = Usuario.objects.get(id_usuario=request.session['pk'])
    imagen = imagen.img_usuario
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all
    Error = ""
    if request.method == "POST":
        try:
            oldPass = request.POST.get('passwordA')
            Pass1 = request.POST.get('password1')
            Pass2 = request.POST.get('password2')
            username= request.session['username']
            user = authenticate(username=username, password=oldPass)
            if user is not None:
                user = Usuario.objects.get(username = request.session['username'])
                if Pass1 == Pass2:
                    if Pass1 == oldPass:
                        Error = "Esta contraseña ya está en uso"
                    else:
                        if len(Pass1) >= 8:
                            if any(chr.isdigit() for chr in Pass1):
                                if any(chr.isupper() for chr in Pass1):
                                    user.set_password(Pass1)
                                    user.save()
                                    logout(request)
                                    return redirect('IniciarSesion')
                                else:
                                    Error = "La contraseña debe tener al menos una letra Mayúscula"
                            else:
                                Error = "la contraseña debe contener al menos un número"
                        else: 
                            Error = "La contraseña debe contener más de 8 digitos"
                else:
                    Error = "Las contraseñan no coinciden"
            else: 
                Error ='Contraseña incorrecta'
        except Exception as e:
            print(e)
    return render(request, 'UserInformation/ChangePassword.html', {"form":form, "User":UserSesion,'message':Error, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})


@login_required()
@PermissionDecorator(['add_usuario','change_usuario', 'delete_usuario', 'view_usuario'])
def Admin(request):
    UserSesion = if_User(request)
    if UserSesion == False:
        return redirect("Inicio")
    cambiosQueryset = cambios.objects.all()
    cambiosfQueryset = cambiosFooter.objects.all()
    template_name = "UsersConfiguration/UsersAdministration.html"
    if request.method=="GET":
        queryset=""
        if request.user.administrador:
            queryset = Usuario.objects.filter().exclude(pk = request.user.pk)
        else:
            queryset = Usuario.objects.filter(administrador = 0).exclude(pk = request.user.pk)
        Servicios = Servicio.objects.all()
        try:
            Vistas = VistasDiarias.objects.get(id_dia=datetime.today().strftime('%Y-%m-%d'))
        except:
            Vistas=0
    return render(request, template_name, {"Usuario":queryset,"contexto":Servicios, "User":UserSesion, "Vistas":Vistas, 'cambios':cambiosQueryset, 'footer':cambiosfQueryset})
  
  
class CreateUser(CreateView, PermissionMixin):
    permission_required = ['add_usuario']
    model = Usuario
    form_class = Regitro
    template_name = 'UsersConfiguration/CreateUsers.html'
    success_url = reverse_lazy("Administracion")
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        context = {
            'form':form,
        }
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        if form.is_valid():
            try:
                form.save()
                update = Usuario.objects.get(username = form.cleaned_data.get('username')) 
                update.estado = 1
                update.save()
                return redirect('Administracion')
            except:
                context['errors'] = form.errors
                context['Error'] = 'No se pudo enviar el correo'
                context['cambios']=cambiosQueryset
                context['footer']=cambiosfQueryset
                return render(request, self.template_name, context)
        else:
            context['errors'] =  form.errors
            context['Error']= 'Los datos ingresados son incorrectos'
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
        UserSesion = if_User(request)
        if UserSesion == False:
            return redirect("Inicio")
        context['User']=UserSesion
        return render(request, self.template_name, context)
                
    def get_context_data(self, *args, **kwargs):
        context = super(CreateUser, self).get_context_data(**kwargs)
        try:
            UserSesion = if_User(self.request)
            if UserSesion == False:
                return redirect("Inicio")
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except:
            return context

class UpdateUser(UpdateView,PermissionMixin):
    permission_required = ['change_usuario']
    model = Usuario    
    template_name = 'UsersConfiguration/CreateUsers.html'
    form_class = EditUser 
    success_url=reverse_lazy("Administracion")  
    def get(self, request, *args,**kwargs):
        try:
            get_object = Usuario.objects.get(id_usuario=kwargs['pk'])
            if kwargs['pk']==request.user.pk:  
                return redirect('Administracion')
        except:
            return redirect('Administracion')
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        form = self.form_class(instance=get_object)
        context= {
            'form':form
        }
        if request.user.administrador == False:
            if get_object.administrador:
                return redirect("Administracion")
        UserSesion = if_User(request)
        if UserSesion == False:
            return redirect("Inicio")
        context['titulo']="Editar Usuario "+get_object.username
        context['User']=UserSesion
        context['UsuarioE']=get_object
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        context['fecha']=str(get_object.fec_nac)
        roles=[]
        if request.user.administrador:
            roles = Group.objects.all()
        else:
            for rol in Group.objects.all():
                try:
                    rol.permissions.get(codename="Empleado")
                except:
                    roles.append(rol)
        context['roles']=roles
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            get_object = Usuario.objects.get(id_usuario=kwargs['pk'])
            if kwargs['pk']==request.user.pk:  
                return redirect('Administracion')
        except:
            return redirect('Administracion')
        form = self.form_class(request.POST or None, instance=get_object)
        context = {
            'form':form,
        }
        cambiosQueryset = cambios.objects.all()
        cambiosfQueryset = cambiosFooter.objects.all()
        if form.is_valid():
            try:
                rol=form.cleaned_data.get('rol')
                if request.user.administrador:
                    form.save()
                    update=Usuario.objects.get(username=form.cleaned_data.get('username'))
                    try:
                        if rol.permissions.get(codename="Administrador"):
                            update.administrador = 1
                            update.save()
                    except:
                        update.administrador = 0
                        update.save()
                    return redirect('Administracion')
                else:
                    try:
                        rol.permissions.get(codename="Empleado")
                        context['Error']= 'El rol '+rol.name+' no puede ser asignado por el usuario '+request.user.nombres+" "+request.user.apellidos
                    except:
                        form.save()
                        update=Usuario.objects.get(username=form.cleaned_data.get('username'))
                        update.administrador = 0
                        update.save()
                        return redirect('Administracion')
            except Exception as e:
                context['errors'] = form.errors
                print(e)
        else:
            context['errors'] =  form.errors
            context['Error']= 'Los datos ingresados son incorrectos'
        roles=[]
        if request.user.administrador:
            roles = Group.objects.all()
        else:
            for rol in Group.objects.all():
                try:
                    rol.permissions.get(codename="Empleado")
                except:
                    roles.append(rol)
        context['roles']=roles
        context['cambios']=cambiosQueryset
        context['footer']=cambiosfQueryset
        context['UsuarioE']=get_object
        UserSesion = if_User(request)
        if UserSesion == False:
            return redirect("Inicio")
        context['User']=UserSesion
        context['titulo']="Editar Usuario "+UserSesion['username']
        return render(request, self.template_name, context)
                
    def get_context_data(self, *args, **kwargs):
        context = super(CreateUser, self).get_context_data(**kwargs)
        try:
            UserSesion = if_User(self.request)
            if UserSesion == False:
                return redirect("Inicio")
            cambiosQueryset = cambios.objects.all()
            cambiosfQueryset = cambiosFooter.objects.all()
            context['titulo']="Editar Usuario "+UserSesion['username']
            context["User"]=UserSesion
            context['cambios']=cambiosQueryset
            context['footer']=cambiosfQueryset
            return context
        except:
            return context

@PermissionDecorator(['change_usuario'])
def CambiarEstadoUsuario(request):
    if request.method=="POST":
        id = request.POST["estado"]
        update=Usuario.objects.get(id_usuario=id)
        estado=update.estado
        if estado==True:
            update.estado=False
            update.save()
        elif estado==False:
            update.estado=True
            update.save()
        else:
            return redirect("Administracion")
        return HttpResponse(update)
    else:
        return JsonResponse({"x":"no"})

class PassR(TemplateView):
    template_name="UserInformation/PasswordRecovery.html"
    def get(self, request, *args,**kwargs):
        if request.user.pk is not None:
            return redirect('Inicio')
        user = ""
        context={}
        user_token_expired = None
        if request.GET['Slug']:
            slug = request.GET['Slug'].replace(" ", "+")
            key = cryptocode.decrypt(slug, Public_Key)
            token_expired = ExpiringTokenAuthentication()
            user,token,message, self.user_token_expired = token_expired.authenticate_credentials(key)
            if user != None and token != None:
                if self.user_token_expired == True:
                    context={'message':'El tiempo de uso de esté link se ha vencido'}
                else:
                    token = Token.objects.get(key = token)
                    token.delete()
                    context={'User':user}
            else:
                context={
                    'message':'Esté link no se puede usar'
                }
        else: 
            return redirect('IniciarSesion')
        
        

        return render(request, self.template_name, context)

    @csrf_exempt
    def post(self,request,*args,**kwargs):
        if request.POST['user'] != '':
            user = Usuario.objects.get(pk=request.POST['user'])
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']
            if pass1 and pass2:
                if pass1 == pass2:
                    if any(chr.isdigit() for chr in pass1):
                        if any(chr.isupper() for chr in pass1):
                            user.set_password(pass1)
                            user.save()
                            return redirect('IniciarSesion')
                        else:
                            messages = "La contraseña debe tener al menos una letra Mayúscula"
                    else:
                        messages ="La contraseña debe tener al menos un número"
                else:
                    messages = "Las contraseñas no coinciden"
            else:
                messages = "Los campos son obligatorios"
            context ={
                'message':messages
            }
        else:
            context={
                'message':'Por favor solicita nuevamente la restauración de contraseña'
            }
        return render(request, self.template_name, context)
    
def PassRec(request):
    messages = []
    success = []
    if request.user.pk is not None:
        return redirect('Inicio')
    if request.method == "POST":
        if request.POST['email']:
            email = request.POST['email']
            if email is not None:
                try:
                    user = Usuario.objects.get(email = email)
                    if user.is_active:
                        try:
                            token = Token.objects.get(user=user)
                            token.delete()
                            token = Token.objects.create(user=user)

                        except:
                            Token.objects.create(user=user)
                            token = Token.objects.get(user=user)
                    try:
                        Servidor = smtplib.SMTP(settings.production.EMAIL_HOST, settings.production.EMAIL_PORT)
                        Servidor.starttls()
                        Servidor.login(settings.production.EMAIL_HOST_USER, settings.production.EMAIL_HOST_PASSWORD)
                        print("conexion establecida")
                        mensaje = MIMEMultipart()
                        mensaje['From'] = settings.production.EMAIL_HOST_USER
                        mensaje['To'] = user.email
                        mensaje['Subject'] = "Cambio de contraseña"
                        cliente = f"{str(user.nombres).capitalize()} {str(user.apellidos).capitalize()}"
                        key = token.key
                        value = cryptocode.encrypt(str(key),Public_Key)
                        content = render_to_string("Correo/CambioContraseñaCorreo.html",
                                                   {"cliente": cliente, "token":value, 'dominio':settings.production.Domain, 'footer':cambiosFooter.objects.all()})
                        mensaje.attach(MIMEText(content, 'html'))

                        Servidor.sendmail(settings.production.EMAIL_HOST_USER,
                                          user.email,
                                          mensaje.as_string())

                        print("Se envio el correo")
                        success = "Se ha enviado el correo correctamente al email "+user.email
                    except Exception as e:
                        messages = e
                except:
                    messages = "Este email no está rgistrado a ningún usuario"
            else:
                messages = "El email es requerido"

    return render(request, 'UserInformation/PasswordRecoveryEmail.html', {'message':messages, 'success':success})
