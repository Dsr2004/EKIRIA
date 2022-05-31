  
def conversor12a24(str1):
    print("Desde funcion")
    print(type(str1))
    print(str1)
    if str1[-2:] == "AM" and str1[:2] == "12": 
        return "00" + str1[2:-2] 
    elif str1[-2:] == "AM": 
        return str1[:-2] 
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2]    
    else: 
        return str(int(str1[:2]) + 12) + str1[2:6] 
  
# print(convert24("01:05 AM")) 


import datetime as dt

horas = [(dt.time(i).strftime("%H:%M")) for i in range(24)]

horasNoDisponibles = {'cita1': {'horaInicio': '04:00', 'horaFin': '06:00'}, 'cita2': {'horaInicio': '19:00', 'horaFin': '21:00'}}

res = [x for x in horas if x not in [x for x in horas for i in horasNoDisponibles if (horasNoDisponibles[i]["horaInicio"] <= x <= horasNoDisponibles[i]["horaFin"])]]


