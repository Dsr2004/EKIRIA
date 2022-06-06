"""
Desarolle un algoritmo que permita leer valores y almacenarlos en las variables A, B, C respectivamente. 
El algoritmo debe imprimir cual es mayor y cual es menor.
Recuerde constatar que los tres valores introducidos por el teclado sean valores distintos. 
Presente un mensaje de alerta en caso de que se detecte la introdución de valores iguales
"""

A = int(input("Ingrese el primer valor: "))
B = int(input("Ingrese el segundo valor: "))
C = int(input("Ingrese el tercer valor: "))



if  A==B or A==C or B==C or C==A:
    print("Los valores ingresados son iguales")
else:
    if A>B and A>C:
        print("El valor mayor es: ", A)
    elif B>A and B>C:
        print("El valor mayor es: ", B)
    elif C==A and B>C:
        print("El valor mayor es: ", C)
        
        
