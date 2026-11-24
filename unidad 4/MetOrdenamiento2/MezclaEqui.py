from pathlib import Path


CARPETA = Path(__file__).resolve().parent

ARCHIVO = CARPETA / "numeros.txt"
RESULTADO = CARPETA / "ordenado.txt"


class MezclaEquilibrada:

    def mezclar(self, izquierda, derecha):

        resultado = []
        i = 0
        j = 0

        while i < len(izquierda) and j < len(derecha):

            if izquierda[i] <= derecha[j]:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])

        return resultado

    def ordenar_archivo(self, archivo):

        aux1 = CARPETA / "auxiliar1.txt"
        aux2 = CARPETA / "auxiliar2.txt"

        salida1 = CARPETA / "salida1.txt"
        salida2 = CARPETA / "salida2.txt"

        cantidad = 0

        with open(archivo, "r", encoding="utf-8") as entrada, \
             open(aux1, "w", encoding="utf-8") as a, \
             open(aux2, "w", encoding="utf-8") as b:

            for linea in entrada:

                if linea.strip() == "":
                    continue

                numero = int(linea.strip())

                if cantidad % 2 == 0:
                    a.write(str(numero) + "\n")
                else:
                    b.write(str(numero) + "\n")

                cantidad += 1

        if cantidad == 0:
            RESULTADO.write_text("", encoding="utf-8")
            return

        while cantidad > 1:

            nuevas_secuencias = 0

            with open(aux1, "r", encoding="utf-8") as a, \
                 open(aux2, "r", encoding="utf-8") as b, \
                 open(salida1, "w", encoding="utf-8") as s1, \
                 open(salida2, "w", encoding="utf-8") as s2:

                while True:

                    linea1 = a.readline()
                    linea2 = b.readline()

                    if not linea1 and not linea2:
                        break

                    izquierda = (
                        list(map(int, linea1.split()))
                        if linea1 else []
                    )

                    derecha = (
                        list(map(int, linea2.split()))
                        if linea2 else []
                    )

                    combinacion = self.mezclar(
                        izquierda, derecha
                    )

                    texto = " ".join(
                        map(str, combinacion)
                    ) + "\n"

                    if nuevas_secuencias % 2 == 0:
                        s1.write(texto)
                    else:
                        s2.write(texto)

                    nuevas_secuencias += 1

            cantidad = nuevas_secuencias

            aux1, salida1 = salida1, aux1
            aux2, salida2 = salida2, aux2

        archivo_final = aux1

        with open(archivo_final, "r", encoding="utf-8") as entrada:

            with open(RESULTADO, "w", encoding="utf-8") as salida:

                for linea in entrada:

                    for numero in linea.split():
                        salida.write(numero + "\n")

        for nombre in [aux1, aux2, salida1, salida2]:

            with open(nombre, "w", encoding="utf-8"):
                pass


if not ARCHIVO.exists():

    print("Error: No se encontró numeros.txt")
    print("Crea el archivo en:", CARPETA)

else:

    metodo = MezclaEquilibrada()

    metodo.ordenar_archivo(ARCHIVO)

    print("Ordenamiento finalizado.")
    print("Resultado guardado en:", RESULTADO.name)

    print("\nNúmeros ordenados:")

    with open(RESULTADO, "r", encoding="utf-8") as archivo:

        print(" ".join(linea.strip() for linea in archivo))
