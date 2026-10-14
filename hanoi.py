
import time


def hanoi(n, origen, auxiliar, destino):
    if n == 0:
        return

    hanoi(n - 1, origen, destino, auxiliar)
    hanoi(n - 1, auxiliar, origen, destino)


def calcular_movimientos(n):
    return 2 ** n - 1


def medir_tiempo(n):
    inicio = time.perf_counter()

    hanoi(n, "A", "B", "C")

    fin = time.perf_counter()
    return fin - inicio


def mostrar_resultados(n):
    movimientos = calcular_movimientos(n)

    print(f"\nCantidad de discos: {n}")
    print(f"Movimientos mínimos: {movimientos:,}")

    if n <= 20:
        tiempo = medir_tiempo(n)
        print(f"Tiempo de ejecución: {tiempo:.8f} segundos")
    else:
        print("Tiempo: No ejecutado por su alto costo")


def main():
    while True:
        print("\n===== TORRE DE HANOI =====")
        print("1. Ejecutar pruebas (5, 10, 30 y 64 discos)")
        print("2. Introducir cantidad de discos")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            discos = [5, 10, 30, 64]

            for n in discos:
                mostrar_resultados(n)

        elif opcion == "2":
            try:
                n = int(input("Ingresa la cantidad de discos: "))

                if n <= 0:
                    print("La cantidad debe ser mayor que 0")
                else:
                    mostrar_resultados(n)

            except ValueError:
                print("Error: Ingresa un número entero válido")

        elif opcion == "0":
            print("Programa finalizado")
            break

        else:
            print("Opción no válida. Intenta nuevamente")


if __name__ == "__main__":
    main()
