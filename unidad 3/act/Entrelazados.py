from dataclasses import dataclass


@dataclass
class Pedido:
    cliente: str
    cantidad: int


class Node:
    def __init__(self, info):
        self.info = info
        self.next = None


class LinkedQueue:
    def __init__(self):
        self.top = None
        self.tail = None
        self._size = 0

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size

    def enqueue(self, info):
        nuevo = Node(info)

        if self.is_empty():
            self.top = nuevo
        else:
            self.tail.next = nuevo

        self.tail = nuevo
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None

        info = self.top.info
        self.top = self.top.next
        self._size -= 1

        if self.top is None:
            self.tail = None

        return info

    def front(self):
        if self.is_empty():
            return None

        return self.top.info

    def getNth(self, pos):
        if not isinstance(pos, int) or pos < 1 or pos > self._size:
            return None

        actual = self.top

        for _ in range(pos - 1):
            actual = actual.next

        return actual.info

    def printInfo(self):
        print("\n********* COLA DE PEDIDOS *********")
        print(f"Tamaño: {self._size}")

        actual = self.top
        posicion = 1

        while actual is not None:
            pedido = actual.info
            print(f"Elemento {posicion}")
            print(f"  Cliente: {pedido.cliente}")
            print(f"  Cantidad: {pedido.cantidad}")

            actual = actual.next
            posicion += 1

        print("**********************************")


def main():
    cola = LinkedQueue()

    pedidos = [
        Pedido("Ana", 20),
        Pedido("Alejandra", 30),
        Pedido("Jose", 40),
        Pedido("Mario May", 50),
    ]


    for pedido in pedidos:
        print(f"\nInsertando: {pedido.cliente}, Cantidad: {pedido.cantidad}")
        cola.enqueue(pedido)
        cola.printInfo()


    pedido = cola.front()
    if pedido is not None:
        print(f"  Cliente: {pedido.cliente}, Cantidad: {pedido.cantidad}")

    pedido = cola.getNth(3)
    if pedido is not None:
        print(f"  Cliente: {pedido.cliente}, Cantidad: {pedido.cantidad}")
    pedido = cola.getNth(10)
    if pedido is not None:
        print(f"  Cliente: {pedido.cliente}, Cantidad: {pedido.cantidad}")

    while not cola.is_empty():
        pedido = cola.dequeue()
        if pedido is not None:
            print(f"Cliente: {pedido.cliente}, Cantidad: {pedido.cantidad}")
        cola.printInfo()

    print("\nExtraer de la cola vacía:", cola.dequeue())


if __name__ == "__main__":
    main()