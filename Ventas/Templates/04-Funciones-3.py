numeros = [1,2,3,5,6,8,9]

inicio,fin = 3,5

for i in numeros:
    if  inicio<=i-1<=fin:
        print("{} esta en el rango".format(i))