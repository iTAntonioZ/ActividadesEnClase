"""Estructura FIFO compartida por ambos ejercicios."""
from collections import deque


class Cola:
    def __init__(self, elementos=()):
        self._elementos = deque(elementos)

    def encolar(self, elemento):
        self._elementos.append(elemento)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")
        return self._elementos.popleft()

    def esta_vacia(self):
        return not self._elementos

    def __len__(self):
        return len(self._elementos)

    def __iter__(self):
        return iter(self._elementos)

    def __repr__(self):
        return f"Cola({list(self._elementos)})"
