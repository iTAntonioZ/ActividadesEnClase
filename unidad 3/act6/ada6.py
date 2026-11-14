class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None


class Arbol:
    def __init__(self):
        self.raiz = None

    def esta_vacio(self):
        return self.raiz is None

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)

        if valor < nodo.valor:
            nodo.izq = self._insertar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._insertar(nodo.der, valor)

        return nodo

    def buscar(self, valor):
        nodo = self.raiz

        while nodo is not None:
            if valor == nodo.valor:
                return True
            if valor < nodo.valor:
                nodo = nodo.izq
            else:
                nodo = nodo.der

        return False

    def eliminar(self, valor):
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return None

        if valor < nodo.valor:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            # Nodo sin hijo izquierdo.
            if nodo.izq is None:
                return nodo.der

            # Nodo sin hijo derecho.
            if nodo.der is None:
                return nodo.izq

            # Nodo con dos hijos: usar el menor del subárbol derecho.
            sucesor = nodo.der
            while sucesor.izq is not None:
                sucesor = sucesor.izq

            nodo.valor = sucesor.valor
            nodo.der = self._eliminar(nodo.der, sucesor.valor)

        return nodo

    def inorden(self):
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                recorrer(nodo.izq)
                resultado.append(nodo.valor)
                recorrer(nodo.der)

        recorrer(self.raiz)
        return resultado

    def preorden(self):
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                resultado.append(nodo.valor)
                recorrer(nodo.izq)
                recorrer(nodo.der)

        recorrer(self.raiz)
        return resultado

    def postorden(self):
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                recorrer(nodo.izq)
                recorrer(nodo.der)
                resultado.append(nodo.valor)

        recorrer(self.raiz)
        return resultado

    def altura(self):
        def calcular(nodo):
            if nodo is None:
                return 0
            return 1 + max(calcular(nodo.izq), calcular(nodo.der))

        return calcular(self.raiz)

    def contar_nodos(self):
        def contar(nodo):
            if nodo is None:
                return 0
            return 1 + contar(nodo.izq) + contar(nodo.der)

        return contar(self.raiz)


def main():
    arbol = Arbol()

    while True:
        print("\n--- ÁRBOL BINARIO DE BÚSQUEDA ---")
        print("1. Insertar")
        print("2. Buscar")
        print("3. Eliminar")
        print("4. Mostrar recorridos")
        print("5. Mostrar altura y cantidad de nodos")
        print("0. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "0":
            break

        if opcion in ("1", "2", "3"):
            try:
                valor = int(input("Ingresa un número entero: "))
            except ValueError:
                print("Debes ingresar un número entero.")
                continue

            if opcion == "1":
                if arbol.buscar(valor):
                    print("El valor ya existe.")
                else:
                    arbol.insertar(valor)
                    print("Valor insertado.")

            elif opcion == "2":
                print(
                    "Valor encontrado."
                    if arbol.buscar(valor)
                    else "El valor no existe."
                )

            elif opcion == "3":
                if arbol.buscar(valor):
                    arbol.eliminar(valor)
                    print("Valor eliminado.")
                else:
                    print("El valor no existe.")

        elif opcion == "4":
            print("Inorden:", arbol.inorden())
            print("Preorden:", arbol.preorden())
            print("Postorden:", arbol.postorden())

        elif opcion == "5":
            print("Altura en niveles:", arbol.altura())
            print("Cantidad de nodos:", arbol.contar_nodos())
            print("Está vacío:", arbol.esta_vacio())

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()