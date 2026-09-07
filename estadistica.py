import random 
import statistics

datos = [random.randint(1, 100) for _ in range(50)]

media = statistics.mean(datos)
mediana = statistics.median(datos)
moda = statistics.multimode(datos)
varianza = statistics.variance(datos)
desviacion = statistics.stdev(datos)

print(f"Datos: {datos}")
print(f"Media: {media}")
print(f"Mediana: {mediana}")
print(f"Moda: {moda}")
print(f"Varianza: {varianza}")
print(f"Desviación estándar: {desviacion}")

