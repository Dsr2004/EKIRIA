import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from this import d
from django.template.loader import render_to_string

from datetime import date, datetime, timedelta, time

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.shortcuts import reverse 

from django.conf import settings
from django.contrib.auth.models import Permission,Group
from Usuarios.models import Usuario
from Notificaciones.signals import notificar

usuario = Usuario


# modelo para administrar los tipos de servicios
class Tipo_servicio(models.Model):
    id_tipo_servicio=models.AutoField("Id del Tipo de Servicio", primary_key=True, unique=True)
    nombre=models.CharField("Nombre", max_length=50, null=False,blank=False, unique=True)
    grado_id = models.ForeignKey(Permission, verbose_name="Grado", on_delete=models.CASCADE, null=False, blank=False,db_column="grado_id")
    fecha_creacion=models.DateField("Fecha de Creacion", auto_now=False, auto_now_add=True)
    fecha_actualizacion= models.DateTimeField("Fecha de Actualizacion", auto_now=True, auto_now_add=False)
    estado=models.BooleanField("Estado", default=True)

    class Meta:
        db_table = 'tipo_servicios'
        verbose_name = 'tipo de servicio'
        verbose_name_plural = 'tipo_servicios'

    def __str__(self):
        return self.nombre

# modelo para administrar los servicios
class Servicio(models.Model):
    id_servicio=models.AutoField("Id del Servicio", primary_key=True, unique=True)
    slug=models.SlugField("Slug", unique=True)
    nombre=models.CharField("Nombre", max_length=40, null=False, blank=False, unique=True)
    descripcion=models.TextField("Descripcion",null=False,blank=False)
    img_servicio=models.ImageField("Imagen del Servicio", upload_to='Ventas/servicios',null=False, blank=False)
    precio=models.IntegerField("Precio",null=False, blank=False)
    tipo_servicio_id=models.ForeignKey(Tipo_servicio, verbose_name="Tipo de Servicio", on_delete=models.CASCADE,null=True, blank=True, db_column="tipo_servicio_id")
    duracion=models.PositiveIntegerField(default=0)
    fecha_creacion=models.DateField("Fecha de Creacion", auto_now=False, auto_now_add=True)
    fecha_actualizacion= models.DateTimeField("Fecha de Actualizacion", auto_now=True, auto_now_add=False)
    estado=models.BooleanField("Estado", default=True)

    class Meta:
        db_table = 'servicios'
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("Ventas:detalleSer", kwargs={"slug": self.slug})
    
    def toJSON(self):
        servicio = {"id_servicio": self.id_servicio,"nombre": self.nombre, "precio": self.precio, 
                    "tipo_servicio_id": self.tipo_servicio_id.nombre, "duracion": self.duracion, 
                    "fecha_creacion": self.fecha_creacion, "fecha_actualizacion": self.fecha_actualizacion, 
                    "estado": self.estado}
        servicio["img_servicio"] = "{}{}".format(settings.MEDIA_URL, self.img_servicio)
        servicio["slug"] = "abrir_modal_detalleServicio('{}')".format(self.get_absolute_url())
        servicio["carrito"]="AjaxAddService({}, 'add')".format(self.id_servicio)
        return servicio
    
    
    

   
    

# modelo para administrar el catalogo
class Catalogo(models.Model):
    id_catalogo=models.AutoField("Id del Catalogo", primary_key=True, unique=True)
    servicio_id=models.ForeignKey(Servicio, verbose_name="Servicio", on_delete=models.CASCADE,null=True, blank=True,db_column="servicio_id")
    fecha_creacion=models.DateField("Fecha de Creacion", auto_now=False, auto_now_add=True)
    fecha_actualizacion= models.DateTimeField("Fecha de Actualizacion", auto_now=True, auto_now_add=False)
    estado=models.BooleanField("Estado", default=True)

    class Meta:
        db_table = 'catalogo'
        verbose_name = 'catalogo'
        ordering = ['id_catalogo','servicio_id','fecha_creacion','fecha_actualizacion','estado']

    def __str__(self):
        return str(self.servicio_id.id_servicio)

# modelo para administrar los servicios personalizados     
class Servicio_Personalizado(models.Model):
    id_servicio_personalizado=models.AutoField("Id del Servicio Personalizado", primary_key=True, unique=True)
    descripcion=models.TextField("Descripcion",null=True,blank=True)
    img_servicio=models.ImageField("Imagen del Servicio", upload_to="Ventas/servicios_personalizados",null=False, blank=False)
    precio=models.IntegerField("Precio",default=0)
    tipo_servicio_id=models.ForeignKey(Tipo_servicio, verbose_name="Tipo de Servicio", on_delete=models.CASCADE,null=False, blank=False, db_column="tipo_servicio_id")
    duracion=models.PositiveIntegerField(default=0)
    fecha_creacion=models.DateField("Fecha de Creacion", auto_now=False, auto_now_add=True)
    fecha_actualizacion= models.DateTimeField("Fecha de Actualizacion", auto_now=True, auto_now_add=False)
    estado=models.BooleanField("Estado", default=True)

    class Meta:
        db_table = 'servicios_personalizados'
        verbose_name = 'servicio personalizado'
        verbose_name_plural = 'servicios_personalizados'

    def __str__(self):
        c_servicio=f"El servicio personalizado es: {self.descripcion}"
        return c_servicio

# modelos para administrar los pedidos
class Pedido(models.Model):
    id_pedido=models.AutoField("Id del Pedido", primary_key=True, unique=True)
    cliente_id=models.ForeignKey(usuario, on_delete=models.SET_NULL, blank=True, null=True, db_column="cliente_id")
    completado=models.BooleanField(default=False, null=True, blank=False)
    total_pagar=models.IntegerField("Total a pagar", default=0)
    
    esPersonalizado=models.BooleanField("Es personalizado", default=False)
    fecha_creacion=models.DateField("Fecha de Creacion", auto_now=False, auto_now_add=True)
    fecha_actualizacion= models.DateTimeField("Fecha de Actualizacion", auto_now=True, auto_now_add=False)
    estado=models.BooleanField("Estado", default=True)

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'

    def __str__(self):
        return f"el id del pedido es: {self.id_pedido}"

    @property
    def get_total_carrito(self):
        itemspedido = self.pedidoitem_set.all()
        total = sum([item.get_total for item in itemspedido])
        return total 

    @property
    def get_items_carrito(self):
        itemspedido = self.pedidoitem_set.all()
        total = len(itemspedido)
        return total 
    
    @property
    def get_cantidad(self):
        itemspedido = self.pedidoitem_set.all()
        duracion = 0
        for i in itemspedido:
            if not i.servicio_id ==  None:
                duracion=duracion+i.servicio_id.duracion
            if not i.servicio_personalizado_id == None:
                duracion=duracion+i.servicio_personalizado_id.duracion
       
        return duracion

    
# modelos para administrar los items del pedido
class PedidoItem(models.Model):
    id_pedidoItem=models.AutoField("Id del Item del  Pedido", primary_key=True, unique=True)
    servicio_id=models.ForeignKey(Servicio, verbose_name="Id del Servicio",db_column="servicio_id", on_delete=models.SET_NULL, null=True)
    servicio_personalizado_id=models.ForeignKey(Servicio_Personalizado, verbose_name="Servicios Personalizados",on_delete=models.SET_NULL, null=True,db_column="servicio_personalizado_id")
    pedido_id=models.ForeignKey(Pedido, verbose_name="Id del Pedido",db_column="pedido_id", on_delete=models.SET_NULL, null=True)
    fecha_creacion=models.DateField("Fecha de Creacion", auto_now=False, auto_now_add=True)
    fecha_actualizacion= models.DateTimeField("Fecha de Actualizacion", auto_now=True, auto_now_add=False)
    estado=models.BooleanField("Estado", default=True)

    class Meta:
        db_table = 'pedidoItems'
        verbose_name = 'pedidoItem'
        verbose_name_plural = 'pedidoItems'

    def __str__(self):
        return f"el id del pedido es: {self.id_pedidoItem}"

    @property
    def get_total(self):
        try:
            total = self.servicio_id.precio * 1
        except Exception as e:
            total=0
        return total
   

    
    
    
class Cita(models.Model):
    id_cita=models.AutoField("Id de la Cita", primary_key=True, unique=True)
    empleado_id=models.ForeignKey(usuario, on_delete=models.SET_NULL, blank=False, null=True, db_column="empleado_id", related_name="empleado_id")
    cliente_id=models.ForeignKey(usuario, on_delete=models.SET_NULL, blank=False, null=True, db_column="cliente_id",related_name="cliente_id")
    pedido_id=models.ForeignKey(Pedido, verbose_name="Id del Pedido",db_column="pedido_id", on_delete=models.SET_NULL, null=True)
    diaCita=models.DateField("Dia de la cita")
    horaInicioCita=models.TimeField("Fecha de Inicio de la Cita",null=False, blank=False)
    horaFinCita=models.TimeField("Fecha de Fin de la Cita",null=False, blank=False)
    descripcion=models.TextField("Descripcion",null=True ,blank=True)
    fecha_creacion=models.DateField("Fecha de Creacion", auto_now=False, auto_now_add=True)
    fecha_actualizacion= models.DateTimeField("Fecha de Actualizacion", auto_now=True, auto_now_add=False)
    cancelado = models.BooleanField(default=False, null=False, blank=False)
    estado=models.BooleanField("Estado", default=False)

    class Meta:
        db_table = 'citas'
        verbose_name = 'cita'
        verbose_name_plural = 'citas'

    def __str__(self):
        return f"el cliente de esta cita es: {self.cliente_id}"

    @property
    def titulo(self):
        title = f"{str(self.cliente_id.nombres).upper()} {str(self.cliente_id.apellidos).upper()}" 
        return title

    @property
    def inicio(self):
        start = self.diaCita.strftime("%Y-%m-%d")
        hora = self.horaInicioCita.strftime("%H:%M:%S")
        start = f"{start}T{hora}"
        return start

    @property
    def fin(self):
        end = self.diaCita.strftime("%Y-%m-%d")
        hora = self.horaFinCita.strftime("%H:%M:%S")
        end = f"{end}T{hora}"
        return end

    @property 
    def EstadoCita(self):
        hoy = datetime.today()
        horaCita = self.horaInicioCita
        fechaCita = datetime(year=self.diaCita.year, month=self.diaCita.month, day=self.diaCita.day, hour=horaCita.hour, minute=horaCita.minute)
        if hoy.date()>=fechaCita.date():
            if hoy.time()<fechaCita.time():
                estado = False
            else:
                estado = True
        else:
            estado = False
        return estado
    
    @property
    def get_url_cliente(self):
        return reverse("Ventas:detalleCita", kwargs={"pk": self.id_cita})
    
    @property
    def get_url_empleado(self):
        return reverse("Ventas:detalleEditarCita", kwargs={"pk": self.id_cita})
        

class Calendario(models.Model):
    #falta el id de este campo importante tambien organizar la parte donde se agendan citas creo
    id_calendario = models.AutoField("Id del la cita en el calendario", primary_key=True, unique=True)
    empleado_id=models.ForeignKey(usuario, on_delete=models.SET_NULL,null=True, db_column="empleado_id", related_name="empleado_calendario_id", blank=False)
    cliente_id=models.ForeignKey(usuario, on_delete=models.SET_NULL,null=True, db_column="cliente_id",related_name="cliente_calendario_id")
    cita_id=models.ForeignKey(Cita, on_delete=models.SET_NULL,null=True,db_column="cita_id")
    dia=models.DateField(null=False, blank=False)
    horaInicio=models.TimeField(null=True, blank=True)
    horaFin=models.TimeField(null=True, blank=True)

    class Meta:
        db_table = 'calendario'
        verbose_name = 'calendario'
        verbose_name_plural = 'calendario'

    def __str__(self):
        return f"el cliente de esta cita es: {self.cliente_id}"

    @property
    def titulo(self):
        title = f"{str(self.cliente_id.nombres).upper()} {str(self.cliente_id.apellidos).upper()}" 
        return title

    @property
    def inicio(self):
        start = self.dia.strftime("%Y-%m-%d")
        hora = self.horaInicio.strftime("%H:%M:%S")
        start = f"{start}T{hora}"
        return start

    @property
    def fin(self):
        end = self.dia.strftime("%Y-%m-%d")
        hora = self.horaFin.strftime("%H:%M:%S")
        end = f"{end}T{hora}"
        return end

def pre_save_servicio_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.nombre)

def pre_save_servicio_personalizado_receiver(sender, instance, *args, **kwargs):
    if instance:
        if instance.tipo_servicio_id.nombre == "Manicure" or instance.tipo_servicio_id.nombre == "manicure" or instance.tipo_servicio_id.nombre == "MANICURE":
            instance.duracion = 120
        elif instance.tipo_servicio_id.nombre == "Pedicure" or instance.tipo_servicio_id.nombre == "pedicure" or instance.tipo_servicio_id.nombre == "PEDICURE":
            instance.duracion = 120
        else:
            instance.duracion = 0
        
def pre_save_cita_receiver(sender, instance, *args, **kwargs):
    if not instance.horaFinCita: 
        # creacion de varibales para la hora de inicio y fin de la cita
        inicio = instance.horaInicioCita
        fin = datetime(1970, 1, 1, inicio.hour, inicio.minute, inicio.second) + timedelta(minutes=instance.pedido_id.get_cantidad)
        fin = time(fin.hour, fin.minute, fin.second)
        #guradar hora fin de la cita
        instance.horaFinCita = fin
        # convertit los numeros 8 y 18 en formato de 24 horas
        AM8 = time(8).strftime("%H:%M")
        AM8 = datetime.strptime(AM8, "%H:%M")
        PM6 = time(18).strftime("%H:%M")
        PM6 = datetime.strptime(PM6, "%H:%M")
        
        if  not AM8.time() <= inicio <=  PM6.time():
            raise Exception("La hora de inicio debe estar entre las  8:00 AM y las 6:00 PM")
        elif not AM8.time() <= fin <=  PM6.time():
            raise Exception("La hora de fin debe estar entre las  8:00 AM y las 6:00 PM, la duracion estimada es de {} minutos ,la hora de fin estimamda es {}".format(instance.pedido_id.get_cantidad, fin.strftime("%I:%M %p")))
        else:
            empleado = instance.empleado_id
            diaCita=instance.diaCita.strftime("%Y-%m-%d")
            diasConsulta = Calendario.objects.filter(empleado_id=empleado).filter(dia=diaCita)
            horas = [(time(i).strftime("%H:%M")) for i in [8,9,10,11,12,13,14,15,16,17,18]]
            
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
                
            iniciox = inicio.strftime("%H:%M")
            finx = fin.strftime("%H:%M")
            finDatetime = datetime.strptime(iniciox, "%H:%M")
            finMinuto = finDatetime-timedelta(minutes=1)
            finMinuto = finMinuto.strftime("%H:%M")
            if not len(horasNoDisponibles)==0:
                horasQuitadas = [x for x in horas for i in horasNoDisponibles if (horasNoDisponibles[i]["horaInicio"] <= x <= horasNoDisponibles[i]["horaFin"])]
                for i in horasQuitadas:
                    if not (iniciox <= i <= finMinuto):
                        raise Exception("Ya existe una cita en esa hora, por favor seleccione otra hora")

def post_save_cita(sender, instance, created, *args, **kwargs):
    if created:
        verb = "{} {} Ha agendado una cita, recuerde que esta cita primero tiene que ser confirmada por el empleado.".format(str(instance.cliente_id.nombres.capitalize()), str(instance.cliente_id.apellidos.capitalize()))
        notificar.send(instance, usuario_id=instance.cliente_id, verbo=verb, direct= instance.get_url_cliente)
       
    else:
        print("desdemodelo")
        print(type(instance.horaInicioCita))
        print(type(instance.horaFinCita))
        citaCalendario = Calendario.objects.get(cita_id=instance.id_cita)
        citaCalendario.dia = instance.diaCita
        citaCalendario.horaInicio = instance.horaInicioCita
        citaCalendario.horaFin = instance.horaFinCita
        citaCalendario.empleado_id = instance.empleado_id
        citaCalendario.save()
            

      

pre_save.connect(pre_save_servicio_receiver,sender=Servicio)
pre_save.connect(pre_save_servicio_personalizado_receiver,sender=Servicio_Personalizado)
pre_save.connect(pre_save_cita_receiver,sender=Cita)
post_save.connect(post_save_cita,sender=Cita)
