"""Simulador interactivo de peaje con colas circulares."""

from collections import deque
from dataclasses import dataclass


TAMANOS = {"moto": 1, "auto": 2, "trailer": 5}


@dataclass
class Vehiculo:
    identificador: str
    tipo: str

    @property
    def espacio(self):
        return TAMANOS[self.tipo]


class ColaCircular:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.datos = [None] * capacidad
        self.frente = 0
        self.final = 0
        self.cantidad = 0
        self.ocupado = 0

    @property
    def libre(self):
        return self.capacidad - self.ocupado

    def cabe(self, vehiculo):
        return self.libre >= vehiculo.espacio and self.cantidad < len(self.datos)

    def entrar(self, vehiculo):
        if not self.cabe(vehiculo):
            return False
        self.datos[self.final] = vehiculo
        self.final = (self.final + 1) % len(self.datos)
        self.cantidad += 1
        self.ocupado += vehiculo.espacio
        return True

    def salir(self):
        if not self.cantidad:
            return None
        vehiculo = self.datos[self.frente]
        self.datos[self.frente] = None
        self.frente = (self.frente + 1) % len(self.datos)
        self.cantidad -= 1
        self.ocupado -= vehiculo.espacio
        return vehiculo

    def vehiculos(self):
        return [self.datos[(self.frente + i) % len(self.datos)]
                for i in range(self.cantidad)]


class Peaje:
    def __init__(self, numero_carriles, autos_por_carril):
        if numero_carriles <= 0 or autos_por_carril <= 0:
            raise ValueError("Las cantidades deben ser mayores que cero.")
        self.capacidad = autos_por_carril * TAMANOS["auto"]
        self.carriles = [ColaCircular(self.capacidad)
                         for _ in range(numero_carriles)]
        self.espera = deque()
        self.secuencia = 0

    def asignar(self, vehiculo):
        candidatos = [i for i, carril in enumerate(self.carriles)
                      if carril.cabe(vehiculo)]
        if not candidatos:
            return None
        # Mejor ajuste: deja el menor espacio sobrante en un carril.
        # En empate se elige el primer carril.
        indice = min(candidatos,
                     key=lambda i: (self.carriles[i].libre - vehiculo.espacio, i))
        self.carriles[indice].entrar(vehiculo)
        return indice + 1

    def atender_espera(self):
        movimientos = []
        while self.espera:
            numero = self.asignar(self.espera[0])
            if numero is None:
                break
            vehiculo = self.espera.popleft()
            movimientos.append(f"{vehiculo.identificador} ({vehiculo.tipo}) "
                               f"entró al carril {numero}.")
        return movimientos

    def llegada(self, tipo):
        if tipo not in TAMANOS:
            return ["Tipo de vehículo inválido."]
        if TAMANOS[tipo] > self.capacidad:
            return [f"No cabe un {tipo} en ningún carril: requiere "
                    f"{TAMANOS[tipo]} unidades y cada carril tiene {self.capacidad}."]
        self.secuencia += 1
        vehiculo = Vehiculo(f"V{self.secuencia}", tipo)
        self.espera.append(vehiculo)
        mensajes = self.atender_espera()
        if vehiculo in self.espera:
            mensajes.append(f"{vehiculo.identificador} ({tipo}) está en espera externa.")
        return mensajes

    def salida(self, numero):
        if not 1 <= numero <= len(self.carriles):
            return ["Número de carril inválido."]
        vehiculo = self.carriles[numero - 1].salir()
        if vehiculo is None:
            return ["El carril está vacío."]
        return [f"Salió {vehiculo.identificador} ({vehiculo.tipo}) "
                f"del carril {numero}."] + self.atender_espera()

    def mostrar(self):
        print("\nESTADO DEL PEAJE — salida ← frente de cada cola")
        for numero, carril in enumerate(self.carriles, 1):
            cola = " → ".join(f"{v.identificador}:{v.tipo}"
                              for v in carril.vehiculos()) or "vacío"
            barra = "#" * carril.ocupado + "." * carril.libre
            print(f"\nCarril {numero}: {cola}")
            print(f"[{barra}] Ocupado: {carril.ocupado}/{carril.capacidad}; "
                  f"libre: {carril.libre} unidades")
            print(f"Caben: {carril.libre // 2} autos O "
                  f"{carril.libre} motos O {carril.libre // 5} tráileres")
        espera = ", ".join(f"{v.identificador}:{v.tipo}" for v in self.espera)
        print(f"\nEspera externa: {espera or 'ninguno'}")
        print("Las cantidades que caben son alternativas, no se suman.")


def leer_entero(mensaje, minimo=1, maximo=None):
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo and (maximo is None or valor <= maximo):
                return valor
        except ValueError:
            pass
        print("Ingresa un número entero dentro del rango permitido.")


def main():
    print("SIMULADOR DE PEAJE")
    numero = leer_entero("¿Cuántos carriles hay? ")
    autos = leer_entero("¿Cuántos autos caben en cada carril? ")
    peaje = Peaje(numero, autos)
    print("\nEquivalencias: moto = 1, auto = 2, tráiler = 5 unidades.")
    print("Todos los carriles admiten cualquier tipo que quepa.")
    print("Asignación por mejor ajuste de espacio; salidas en orden FIFO.")
    if peaje.capacidad < TAMANOS["trailer"]:
        print("Con esta capacidad no caben tráileres en los carriles.")

    while True:
        print("\n1. Entrada de vehículo\n2. Salida de vehículo"
              "\n3. Ver espacios disponibles\n4. Terminar")
        opcion = leer_entero("Selecciona una opción: ", maximo=4)
        if opcion == 1:
            print("1. Moto\n2. Auto\n3. Tráiler")
            tipo = ("moto", "auto", "trailer")[
                leer_entero("Tipo: ", maximo=3) - 1]
            print("\n".join(peaje.llegada(tipo)))
        elif opcion == 2:
            peaje.mostrar()
            carril = leer_entero("¿De qué carril sale el primer vehículo? ",
                                 maximo=numero)
            print("\n".join(peaje.salida(carril)))
        elif opcion == 3:
            peaje.mostrar()
        else:
            print("Simulación finalizada.")
            break


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSimulación finalizada.")
