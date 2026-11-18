class Ordenador:
    def __init__(self, datos):
        self.datos = list(datos)

    # ------------------------------------------------------------------
    # 1. SHELLSORT (Secuencia de Knuth / Mitades)
    # ------------------------------------------------------------------
    def shell_sort(self):
        arr = self.datos.copy()
        n = len(arr)
        gap = 1
        # Generamos la brecha inicial usando la secuencia de Knuth (3k + 1)
        while gap < n // 3:
            gap = gap * 3 + 1

        while gap >= 1:
            for i in range(gap, n):
                actual = arr[i]
                j = i
                while j >= gap and arr[j - gap] > actual:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = actual
            gap //= 3
        return arr

    # ------------------------------------------------------------------
    # 2. QUICKSORT (Partición de Lomuto in-place)
    # ------------------------------------------------------------------
    def quick_sort(self):
        arr = self.datos.copy()
        self._quicksort_recursivo(arr, 0, len(arr) - 1)
        return arr

    def _quicksort_recursivo(self, arr, inicio, fin):
        if inicio < fin:
            indice_pivote = self._particionar(arr, inicio, fin)
            self._quicksort_recursivo(arr, inicio, indice_pivote - 1)
            self._quicksort_recursivo(arr, indice_pivote + 1, fin)

    def _particionar(self, arr, inicio, fin):
        pivote = arr[fin]
        i = inicio - 1
        for j in range(inicio, fin):
            if arr[j] <= pivote:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[fin] = arr[fin], arr[i + 1]
        return i + 1

    # ------------------------------------------------------------------
    # 3. HEAPSORT (Montículo máximo)
    # ------------------------------------------------------------------
    def heap_sort(self):
        arr = self.datos.copy()
        n = len(arr)

        for idx in range(n // 2 - 1, -1, -1):
            self._hundir(arr, n, idx)

        for fin in range(n - 1, 0, -1):
            arr[0], arr[fin] = arr[fin], arr[0]
            self._hundir(arr, fin, 0)

        return arr

    def _hundir(self, arr, tamano, raiz):
        while True:
            mayor = raiz
            izq = 2 * raiz + 1
            der = 2 * raiz + 2

            if izq < tamano and arr[izq] > arr[mayor]:
                mayor = izq
            if der < tamano and arr[der] > arr[mayor]:
                mayor = der

            if mayor == raiz:
                break

            arr[raiz], arr[mayor] = arr[mayor], arr[raiz]
            raiz = mayor

    # ------------------------------------------------------------------
    # 4. RADIX SORT (Por cubetas / Buckets base 10)
    # ------------------------------------------------------------------
    def radix_sort(self):
        if not self.datos:
            return []

        negativos = [-num for num in self.datos if num < 0]
        positivos = [num for num in self.datos if num >= 0]

        neg_ordenados = [-num for num in reversed(self._radix_buckets(negativos))]
        pos_ordenados = self._radix_buckets(positivos)
        return neg_ordenados + pos_ordenados

    def _radix_buckets(self, lista):
        if not lista:
            return []
        arr = lista.copy()
        max_val = max(arr)
        posicion = 1

        while max_val // posicion > 0:
            cubetas = [[] for _ in range(10)]
            for num in arr:
                digito = (num // posicion) % 10
                cubetas[digito].append(num)
            arr = [num for cubeta in cubetas for num in cubeta]
            posicion *= 10
        return arr


# ======================================================================
# INTERFAZ DE CONSOLA
# ======================================================================
def leer_lista_usuario():
    while True:
        try:
            total = int(input("\nCantidad de números a ordenar: "))
            if total > 0:
                break
            print("Debe ser un entero positivo.")
        except ValueError:
            print("Valor no válido. Intenta de nuevo.")

    valores = []
    for idx in range(1, total + 1):
        while True:
            try:
                dato = int(input(f"  [{idx}/{total}] Número: "))
                valores.append(dato)
                break
            except ValueError:
                print("  Error: ingresa solo números enteros.")
    return valores


def ejecutar_programa():
    opciones = {
        "1": ("ShellSort (Secuencia de Knuth)", lambda obj: obj.shell_sort()),
        "2": ("Quicksort (Partición Lomuto)", lambda obj: obj.quick_sort()),
        "3": ("Heapsort (Montículo iterativo)", lambda obj: obj.heap_sort()),
        "4": ("Radix Sort (Cubetas base 10)", lambda obj: obj.radix_sort()),
    }

    while True:
        print("\n+------------------------------------------+")
        print("|    ALGORITMOS DE ORDENAMIENTO - ADA 2    |")
        print("+------------------------------------------+")
        print("| 1. ShellSort                             |")
        print("| 2. Quicksort                             |")
        print("| 3. Heapsort                              |")
        print("| 4. Radix                                 |")
        print("| 0. Salir                                 |")
        print("+------------------------------------------+")

        eleccion = input("Elige una opción: ").strip()

        if eleccion == "0":
            print("\nPrograma finalizado.")
            break

        if eleccion in opciones:
            nombre, funcion = opciones[eleccion]
            numeros = leer_lista_usuario()
            ordenador = Ordenador(numeros)
            resultado = funcion(ordenador)

            print(f"\n--- Resultado con {nombre} ---")
            print(f"Entrada : {numeros}")
            print(f"Ordenado: {resultado}")
        else:
            print("\nOpción incorrecta, selecciona del 0 al 4.")


if __name__ == "__main__":
    ejecutar_programa()