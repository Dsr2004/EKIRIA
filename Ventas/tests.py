# import smtplib
# from Proyecto_Ekiria.wsgi import *
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from django.template.loader import render_to_string
# from Proyecto_Ekiria import settings

import datetime as dt


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

        content = render_to_string("Correo/send_email.html")
        mensaje.attach(MIMEText(content, 'html'))

        Servidor.sendmail(settings.EMAIL_HOST_USER,
                            settings.EMAIL_HOST_USER,
                            mensaje.as_string())

        print("Se envio el correo")
    except Exception as e:
        print(e)






def restar():
    #lista donde estan todas las horas disponibles
    horas = hours = [(dt.time(i).strftime("%H:%M")) for i in range(24)]

    #horas que hay que quitar de la lista principal
    horasNoDisponibles = {'cita1': {'horaInicio': '04:00', 'horaFin': '06:00'}, 'cita2': {'horaInicio': '07:00', 'horaFin': '09:00'}}

    #funcion que resta
    # res=[]
    # for i in horasNoDisponibles:
    #     for x in horas:
    #         if  x not in res:
    #             if (x < horasNoDisponibles[i]["horaInicio"] or x >horasNoDisponibles[i]["horaFin"]):
    #                 res.append(x)
   
    
    res = [x 
        for x in horas
            for i in horasNoDisponibles if i not in res  
            if (x < horasNoDisponibles[i]["horaInicio"] or x >horasNoDisponibles[i]["horaFin"])
            ]
        

    print(res)

def prueba():
    horas = [(dt.time(i).strftime("%H:%M")) for i in range(24)]

    horasNoDisponibles = {'cita1': {'horaInicio': '04:00', 'horaFin': '06:00'}, 'cita2': {'horaInicio': '07:00', 'horaFin': '09:00'}}

    for i in horasNoDisponibles:
        res = [x for x in horas if (x < horasNoDisponibles[i]["horaInicio"] or x > horasNoDisponibles[i]["horaFin"])]

    print(res)

prueba()

# 12


# hours = [(dt.time(i).strftime("%H:%M")) for i in range(24)]

# for i in hours:
#     print(i, type(i))




# como convertir el numero a hora en python
# hours = [(dt.time(hour=i)) for i in range(24)]