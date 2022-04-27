import smtplib
from Proyecto_Ekiria.wsgi import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from Proyecto_Ekiria import settings

# def conexion():
#     try:
#         Servidor = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
#         print(Servidor.ehlo())
#         Servidor.starttls()
#         print(Servidor.ehlo())
#         Servidor.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
#         print("conexion establecida")
#     except Exception as e:
#         print(e)


def AgendarCitaCorreo(datos):
    print("llego a la funcion")
    for dato in datos:
        print(datos[dato])
    try:
        Servidor = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        Servidor.starttls()
        Servidor.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("conexion establecida")

        mensaje = MIMEMultipart()
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = datos.cliente
        mensaje['Subject'] = "Correo de Agendamiento de cita"

        content = render_to_string("Correo/send_email.html")
        mensaje.attach(MIMEText(content, 'html'))

        Servidor.sendmail(settings.EMAIL_HOST_USER,
                            datos.cliente,
                            mensaje.as_string())

        print("Se envio el correo")
    except Exception as e:
        print(e)




