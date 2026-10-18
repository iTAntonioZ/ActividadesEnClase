
class Pila:
    def __init__(self):
        self.elementos = []

    def apilar(self, valor):
        self.elementos.append(valor)

    def desapilar(self):
        if not self.elementos:
            raise ValueError("Faltan números en la expresión")
        return self.elementos.pop()

    def tamaño(self):
        return len(self.elementos)


OPERADORES = {"+", "-", "*", "/"}


def validar_expresion(expresion):
    if not expresion.strip():
        raise ValueError("No ingresaste una expresión")

    tokens = expresion.split()

    for token in tokens:
        if token in OPERADORES:
            continue

        try:
            numero = float(token)
        except ValueError:
            raise ValueError(
                f"El elemento '{token}' no está permitido"
            )

        import math
        if not math.isfinite(numero):
            raise ValueError("Solo se admiten números finitos")

    return tokens


def operar(a, b, operador):
    if operador == "+":
        return a + b
    elif operador == "-":
        return a - b
    elif operador == "*":
        return a * b
    elif operador == "/":
        if b == 0:
            raise ZeroDivisionError("División entre cero")
        return a / b


def evaluar(expresion, tipo):
    tokens = validar_expresion(expresion)
    pila = Pila()

    if tipo == "prefija":
        tokens = list(reversed(tokens))

    for token in tokens:
        if token in OPERADORES:
            primero = pila.desapilar()
            segundo = pila.desapilar()

            if tipo == "postfija":
                resultado = operar(segundo, primero, token)
            else:
                resultado = operar(primero, segundo, token)

            pila.apilar(resultado)
        else:
            pila.apilar(float(token))

    if pila.tamaño() != 1:
        raise ValueError("Expresión aritmética incorrecta")

    return pila.desapilar()


def menu():
    while True:
        print("\n===== EVALUADOR DE EXPRESIONES =====")
        print("1. Notación postfija")
        print("2. Notación prefija")
        print("0. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "0":
            print("Programa finalizado.")
            break

        if opcion not in ("1", "2"):
            print("Opción no válida.")
            continue

        tipo = "postfija" if opcion == "1" else "prefija"

        print("\nOperadores permitidos: + - * /")
        print("Escribe cada número y operador separado")
        print("por un espacio.")

        expresion = input("Expresión: ")

        try:
            resultado = evaluar(expresion, tipo)
            print(f"\nResultado: {resultado:g}")

        except (ValueError, ZeroDivisionError) as error:
            print("\nError:", error)


if __name__ == "__main__":
    menu()
