import smtplib
from email.mime.text import MIMEText

from Proyecto_Ekiria import settings

def send_email():
    try:
        Servidor = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT )
        print(Servidor.ehlo())
        Servidor.starttls()
        print(Servidor.ehlo())
        Servidor.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("conexion establecida")

        mensaje = MIMEText("""Este es el mensaje
        de las narices""")
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = settings.EMAIL_HOST_USER
        mensaje['Subject'] = "Tienes un correo"

        Servidor.sendmail(settings.EMAIL_HOST_USER,
                            settings.EMAIL_HOST_USER,
                            mensaje.as_string())

        print("Se envio el correo")
    except Exception as e:
        print(e)

send_email()

el otro_------
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from django.conf import settings
settings.configure()

def send_email():
    try:
        Servidor = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT )
        print(Servidor.ehlo())
        Servidor.starttls()
        print(Servidor.ehlo())
        Servidor.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("conexion establecida")


        mensaje = MIMEMultipart()
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = settings.EMAIL_HOST_USER
        mensaje['Subject'] = "Tienes un correo"


        contenido = render_to_string("Correo/send_email.html")

        mensaje.attach(MIMEText(contenido, 'html'))
        Servidor.sendmail(settings.EMAIL_HOST_USER,#de donde
                            settings.EMAIL_HOST_USER,#hacia donde
                            mensaje.as_string())

        print("Se envio el correo")
    except Exception as e:
        print(e)

send_email()