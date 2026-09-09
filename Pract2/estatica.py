calificaciones = [0] * 5

print(calificaciones)

for i in range(5):
    calificaciones[i] = int(input("Ingrese la calificación del estudiante {}: ".format(i + 1)))

print("Calificaciones ingresadas:", calificaciones)