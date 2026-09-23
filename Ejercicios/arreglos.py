import random
import time

# 1. Ingreso de dimensiones
num_alumnos = int(input("Ingrese la cantidad de alumnos: "))
num_materias = int(input("Ingrese la cantidad de materias: ")) 

matriz_materias_alumnos = [
    [random.randint(50, 100) for _ in range(num_alumnos)]
    for _ in range(num_materias)
]


matriz_alumnos_materias = [
    [matriz_materias_alumnos[m][a] for m in range(num_materias)]
    for a in range(num_alumnos)
]


print("\n" + "=" * 65)
print("TABLA 1: Filas = Materias | Columnas = Alumnos")
print("=" * 65)

if num_alumnos > 6:
    header = f"{'Materia':<10} Alum_1    Alum_2    Alum_3    ...    " \
             f"Alum_{num_alumnos-2:<4} Alum_{num_alumnos-1:<4} Alum_{num_alumnos:<4}"
    print(header)
    print("-" * len(header))
    
    for m in range(num_materias):
        p1 = f"{matriz_materias_alumnos[m][0]:<9} {matriz_materias_alumnos[m][1]:<9} {matriz_materias_alumnos[m][2]:<9}"
        p2 = f"{matriz_materias_alumnos[m][-3]:<10} {matriz_materias_alumnos[m][-2]:<10} {matriz_materias_alumnos[m][-1]:<10}"
        print(f"Mat_{m+1:<6} {p1} ...    {p2}")
else:
    header = f"{'Materia':<10}" + "".join([f"Alum_{i+1:<5} " for i in range(num_alumnos)])
    print(header)
    print("-" * len(header))
    for m in range(num_materias):
        fila = f"Mat_{m+1:<6}" + "".join([f"{matriz_materias_alumnos[m][a]:<9} " for a in range(num_alumnos)])
        print(fila)


print("\n" + "=" * 65)
print("TABLA 2: Filas = Alumnos | Columnas = Materias")
print("=" * 65)

header_m = f"{'Alumno':<10}" + "".join([f"Mat_{j+1:<6}" for j in range(num_materias)])
print(header_m)
print("-" * len(header_m))

def imprimir_fila_alumno(idx):
    califs = "".join([f"{matriz_alumnos_materias[idx][m]:<10}" for m in range(num_materias)])
    print(f"Alum_{idx+1:<5}{califs}")

if num_alumnos > 8:
    for a in range(3):
        imprimir_fila_alumno(a)
    print(f"{'......':<10}" + "......    " * num_materias)
    for a in range(num_alumnos - 3, num_alumnos):
        imprimir_fila_alumno(a)
else:
    for a in range(num_alumnos):
        imprimir_fila_alumno(a)

print("\n" + "=" * 65)
alumno_consultar = int(input(f"Ingrese el número de alumno a consultar (1 a {num_alumnos}): "))
materia_consultar = int(input(f"Ingrese el número de materia a consultar (1 a {num_materias}): "))

if 1 <= alumno_consultar <= num_alumnos and 1 <= materia_consultar <= num_materias:
    idx_alumno = alumno_consultar - 1
    idx_materia = materia_consultar - 1

    inicio_f1 = time.perf_counter()
    calif_f1 = matriz_materias_alumnos[idx_materia][idx_alumno]
    fin_f1 = time.perf_counter()
    tiempo_f1 = fin_f1 - inicio_f1

    inicio_f2 = time.perf_counter()
    calif_f2 = matriz_alumnos_materias[idx_alumno][idx_materia]
    fin_f2 = time.perf_counter()
    tiempo_f2 = fin_f2 - inicio_f2

    print(f"\n--- Resultados de la Consulta ---")
    print(f"Forma 1 (Filas = Materias, Cols = Alumnos):")
    print(f"  Calificación: {calif_f1} | Tiempo de acceso: {tiempo_f1:.8f} s")

    print(f"Forma 2 (Filas = Alumnos, Cols = Materias):")
    print(f"  Calificación: {calif_f2} | Tiempo de acceso: {tiempo_f2:.8f} s")
else:
    print("Error: Los valores ingresados están fuera del rango permitido.")