import time

class Factorial:
    def __init__(self, n):
        self.n = n

    def calcular(self, n=None):
        if n is None:
            n = self.n
        if n <= 1:
            return 1
        return n * self.calcular(n - 1)

    def mostrar(self):
        print(self.calcular())

a = 5
f = Factorial(a)
#f.mostrar()  