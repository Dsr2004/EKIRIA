from operator import truediv
import smtplib
from Proyecto_Ekiria.wsgi import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from Proyecto_Ekiria import settings


def AgendarCitaCorreo(datos):
    try:
         #Estableciendo conexion con el servidor
        Servidor = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT )
        #establecindo protocolo tls 
        Servidor.starttls()
        #logeandose con los datos de los settings
        Servidor.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        #construyendo mensaje para quien de donde y el asunto
        mensaje = MIMEMultipart()
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = settings.EMAIL_HOST_USER
        mensaje['Subject'] = "Tienes un correo"

        cliente = f"{datos.cliente_id.nombres} {datos.cliente_id.apellidos}"
        contexto={"cliente": cliente, "dia":datos.diaCita, "hora":datos.horaInicioCita, "url":"sdfdf"}

        #cuerpo del correo
        content = render_to_string("Correo/AgendarCitaCorreo.html",)
        #renderizando la plantilla
        mensaje.attach(MIMEText(content, 'html'))

        #enviando el correo con la configuracion de los setings y de el mensaje contruido anteriormente
        Servidor.sendmail(settings.EMAIL_HOST_USER,
                            settings.EMAIL_HOST_USER,
                            mensaje.as_string())
        
        return 

        print("Se envio el correo")
    except Exception as e:
        return str(e)
