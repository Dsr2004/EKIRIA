numeros = [20, 51, 23, 20]

numerosSinRepetir = [x for x in numeros if x != min(numeros)]

print(numerosSinRepetir)