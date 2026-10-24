from cola import Cola


def sumar_colas(cola_a, cola_b):
    if len(cola_a) != len(cola_b):
        raise ValueError("Las dos colas deben tener la misma cantidad de elementos.")
    if any(type(n) is not int for n in cola_a) or any(
        type(n) is not int for n in cola_b
    ):
        raise ValueError("Las colas solo pueden contener números enteros.")
    copia_a, copia_b = Cola(cola_a), Cola(cola_b)
    resultado = Cola()
    while not copia_a.esta_vacia():
        resultado.encolar(copia_a.desencolar() + copia_b.desencolar())
    return resultado


def leer_cola(nombre):
    while True:
        try:
            entrada = input(f"Cola {nombre} (enteros separados por espacios): ")
            return Cola(int(valor) for valor in entrada.split())
        except ValueError:
            print("Entrada inválida. Escribe únicamente números enteros.")


def main():
    print("SUMA DE DOS COLAS")
    print("Ejemplo: A = 3 4 2 8 12; B = 6 2 9 11 3")
    cola_a = leer_cola("A")
    cola_b = leer_cola("B")
    try:
        resultado = sumar_colas(cola_a, cola_b)
    except ValueError as error:
        print(error)
        return
    print(f"{'Cola A':>10} {'Cola B':>10} {'Resultado':>10}")
    for a, b, suma in zip(cola_a, cola_b, resultado):
        print(f"{a:>10} {b:>10} {suma:>10}")
    print("Cola resultado:", list(resultado))


if __name__ == "__main__":
    main()
