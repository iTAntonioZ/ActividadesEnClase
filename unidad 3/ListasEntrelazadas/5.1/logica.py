class Nodo:
    def __init__(self, dato, liga=None):
        self.info, self.liga = dato, liga


class ListaLigada:
    def __init__(self):
        self.inicio = None
        self.nodos = []

    def valores(self):
        datos, actual = [], self.inicio
        while actual is not None:
            datos.append(actual.info)
            actual = actual.liga
        return datos

    def insertar(self, dato, modo, referencia=None, posicion=None):
        """Devuelve el índice nuevo. Posición comienza en 1.
        Medio: inserta después de n // 2 nodos.
        Antes/después: usa la primera coincidencia de X.
        """
        if dato is None or not str(dato).strip():
            raise ValueError('El dato del nodo no puede estar vacío.')
        datos = self.valores()
        if modo == 'inicio':
            i = 0
        elif modo == 'final':
            i = len(datos)
        elif modo == 'medio':
            i = len(datos) // 2
        elif modo == 'posicion':
            if type(posicion) is not int or not 1 <= posicion <= len(datos) + 1:
                raise ValueError(f'Posición inválida: {posicion}.\nPara insertar con {len(datos)} nodos, elige una posición entre 1 y {len(datos) + 1}.\nLas posiciones comienzan en 1; no pueden ser negativas ni cero.')
            i = posicion - 1
        elif modo in ('antes', 'despues'):
            if referencia not in datos:
                raise ValueError(f'No existe un nodo con el dato {referencia!r}. Revisa el dato X de referencia.')
            i = datos.index(referencia) + (modo == 'despues')
        else:
            raise ValueError('Opción inválida.')
        nuevo = Nodo(dato)
        self.nodos.append(nuevo)
        if i == 0:
            nuevo.liga = self.inicio
            self.inicio = nuevo
        else:
            anterior = self.inicio
            for _ in range(i - 1):
                anterior = anterior.liga
            nuevo.liga = anterior.liga
            anterior.liga = nuevo
        return i

    def eliminar(self, modo, referencia=None, posicion=None):
        datos = self.valores()
        if not datos:
            raise ValueError('La lista está vacía. Inserta un nodo antes de eliminar.')
        if modo == 'inicio':
            i = 0
        elif modo == 'final':
            i = len(datos) - 1
        elif modo == 'medio':
            i = (len(datos) - 1) // 2
        elif modo == 'posicion':
            if type(posicion) is not int or not 1 <= posicion <= len(datos):
                raise ValueError(f'Posición inválida: {posicion}.\nPara eliminar, elige una posición entre 1 y {len(datos)}.')
            i = posicion - 1
        elif modo in ('valor', 'antes', 'despues'):
            if referencia not in datos:
                raise ValueError(f'No existe un nodo con el dato {referencia!r}. Revisa el dato X de referencia.')
            i = datos.index(referencia) + {'valor': 0, 'antes': -1, 'despues': 1}[modo]
            if not 0 <= i < len(datos):
                raise ValueError('No se puede eliminar el anterior al primer nodo.' if i < 0 else 'No se puede eliminar el posterior al último nodo.')
        else:
            raise ValueError('Opción inválida.')
        anterior = None
        actual = self.inicio
        for _ in range(i):
            anterior, actual = actual, actual.liga
        if anterior is None:
            self.inicio = actual.liga
        else:
            anterior.liga = actual.liga
        actual.liga = None
        for nodo in self.nodos:
            if nodo.liga is actual:
                nodo.liga = None
        self.nodos.remove(actual)
        return i, actual.info

    @staticmethod
    def clave(valor):
        # Orden numérico si es un número finito; los textos van después.
        from decimal import Decimal, InvalidOperation
        try:
            numero = Decimal(str(valor))
            if numero.is_finite():
                return (0, numero)
        except InvalidOperation:
            pass
        return (1, str(valor))

    def esta_ordenada(self):
        actual = self.inicio
        while actual is not None and actual.liga is not None:
            if self.clave(actual.info) > self.clave(actual.liga.info):
                return False
            actual = actual.liga
        return True

    def ordenar(self):
        nodos = []
        actual = self.inicio
        while actual is not None:
            nodos.append(actual)
            actual = actual.liga
        nodos.sort(key=lambda nodo: self.clave(nodo.info))
        for i, nodo in enumerate(nodos):
            nodo.liga = nodos[i + 1] if i + 1 < len(nodos) else None
        self.inicio = nodos[0] if nodos else None

    def buscar(self, dato, modo='desordenada'):
        """Devuelve (índice encontrado o None, índices visitados).
        La igualdad es exacta; la ordenada requiere orden ascendente.
        """
        if modo not in ('desordenada', 'ordenada', 'recursiva'):
            raise ValueError('Búsqueda desconocida.')
        if modo == 'ordenada' and not self.esta_ordenada():
            raise ValueError('La lista no está ordenada. Usa Ordenar ascendente primero.')
        visitados = []
        def visitar(nodo, i):
            if nodo is None:
                return None
            visitados.append(i)
            if nodo.info == dato:
                return i
            return visitar(nodo.liga, i + 1)
        if modo == 'recursiva':
            return visitar(self.inicio, 0), visitados
        actual, i = self.inicio, 0
        while actual is not None:
            visitados.append(i)
            if actual.info == dato:
                return i, visitados
            if modo == 'ordenada' and self.clave(actual.info) > self.clave(dato):
                break
            actual, i = actual.liga, i + 1
        return None, visitados

    def recorrer(self, modo='iterativo'):
        """Devuelve pares (índice, dato) en orden de visita/salida."""
        salida = []
        if modo == 'iterativo':
            actual, i = self.inicio, 0
            while actual is not None:
                salida.append((i, actual.info))
                actual, i = actual.liga, i + 1
        elif modo in ('recursivo', 'inverso'):
            def visitar(nodo, i):
                if nodo is None:
                    return
                if modo == 'recursivo':
                    salida.append((i, nodo.info))
                visitar(nodo.liga, i + 1)
                if modo == 'inverso':
                    salida.append((i, nodo.info))
            visitar(self.inicio, 0)
        else:
            raise ValueError('Recorrido desconocido.')
        return salida

    def vaciar(self):
        self.inicio = None
        self.nodos.clear()

    def omitir_siguiente(self, referencia):
        """Reconecta X con el sucesor de su siguiente y retira el omitido.

        Equivale a eliminar el posterior a la primera coincidencia de X.
        Si el omitido es el último, X queda enlazado a None (NIL).
        """
        return self.eliminar('despues', referencia=referencia)

    def conectar(self, origen, destino=None):
        """Conecta objetos del registro, conservando los nodos desconectados.
        No permite ciclos. Un nodo que pierde su última entrada queda en NULL.
        """
        if origen not in self.nodos or (destino is not None and destino not in self.nodos):
            raise ValueError('Selecciona nodos existentes.')
        actual = destino
        visitados = set()
        while actual is not None:
            if actual is origen or actual in visitados:
                raise ValueError('Esta conexión crearía un ciclo. Elige otro destino o NULL.')
            visitados.add(actual)
            actual = actual.liga
        anterior = origen.liga
        origen.liga = destino
        # Al perder su última entrada, un nodo suelto apunta a NULL.
        while (anterior is not None and anterior is not self.inicio
               and not any(n.liga is anterior for n in self.nodos)):
            siguiente = anterior.liga
            anterior.liga = None
            anterior = siguiente

    def agregar_suelto(self, dato):
        if not str(dato).strip():
            raise ValueError('Escribe un dato para el nuevo nodo.')
        nodo = Nodo(str(dato).strip())
        self.nodos.append(nodo)
        if self.inicio is None:
            self.inicio = nodo
        return nodo
