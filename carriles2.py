"""Simulador interactivo de peaje con colas circulares.

Equivalencias de espacio:
    Moto = 1 unidad
    Auto = 2 unidades
    Tráiler = 5 unidades

Con cuatro carriles se usa una política especializada:
    Carril 1: preferente para tráileres.
    Carriles 2 y 3: preferentes para autos y motos.
    Carril 4: auxiliar para cualquier vehículo.

Si se configura otra cantidad de carriles, se utiliza Best Fit flexible.
"""

from collections import deque
from dataclasses import dataclass


TAMANOS = {"moto": 1, "auto": 2, "trailer": 5}
NOMBRES_TIPO = {"moto": "moto", "auto": "auto", "trailer": "tráiler"}


@dataclass(frozen=True)
class Vehiculo:
    identificador: str
    tipo: str

    def __post_init__(self):
        if self.tipo not in TAMANOS:
            raise ValueError(f"Tipo de vehículo inválido: {self.tipo!r}")

    @property
    def espacio(self):
        return TAMANOS[self.tipo]


class ColaCircular:
    """Cola FIFO circular con capacidad expresada en unidades de espacio."""

    def __init__(self, capacidad):
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise ValueError("La capacidad debe ser un entero mayor que cero.")

        self.capacidad = capacidad
        # Como cada vehículo ocupa al menos una unidad, caben como máximo
        # 'capacidad' vehículos. Los índices representan vehículos, no espacio.
        self.datos = [None] * capacidad
        self.frente = 0
        self.final = 0
        self.cantidad = 0
        self.ocupado = 0

    @property
    def libre(self):
        return self.capacidad - self.ocupado

    def cabe(self, vehiculo):
        return self.libre >= vehiculo.espacio

    def entrar(self, vehiculo):
        # La segunda condición protege el arreglo incluso si se alterara
        # accidentalmente el estado interno de la cola.
        if not self.cabe(vehiculo) or self.cantidad >= len(self.datos):
            return False

        self.datos[self.final] = vehiculo
        self.final = (self.final + 1) % len(self.datos)
        self.cantidad += 1
        self.ocupado += vehiculo.espacio
        return True

    def salir(self):
        if self.cantidad == 0:
            return None

        vehiculo = self.datos[self.frente]
        self.datos[self.frente] = None
        self.frente = (self.frente + 1) % len(self.datos)
        self.cantidad -= 1
        self.ocupado -= vehiculo.espacio
        return vehiculo

    def vehiculos(self):
        return [
            self.datos[(self.frente + i) % len(self.datos)]
            for i in range(self.cantidad)
        ]


class Peaje:
    def __init__(self, numero_carriles, autos_por_carril):
        for valor, nombre in (
            (numero_carriles, "El número de carriles"),
            (autos_por_carril, "La cantidad de autos por carril"),
        ):
            if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
                raise ValueError(f"{nombre} debe ser un entero mayor que cero.")

        # Etotal = número de autos configurado × 2 unidades por auto.
        self.capacidad = autos_por_carril * TAMANOS["auto"]
        self.carriles = [
            ColaCircular(self.capacidad) for _ in range(numero_carriles)
        ]
        self.espera = deque()
        self.secuencia = 0
        self.politica_especializada = numero_carriles == 4

    def _carriles_preferentes(self, vehiculo):
        """Devuelve los carriles preferentes y, al final, el auxiliar."""
        if not self.politica_especializada:
            return list(range(len(self.carriles)))

        # Índices internos: 0 = carril 1, ..., 3 = carril 4.
        if vehiculo.tipo == "trailer":
            return [0, 3]  # Carril 1 preferente; carril 4 auxiliar.
        return [1, 2, 3]  # Carriles 2 y 3 preferentes; carril 4 auxiliar.

    def asignar(self, vehiculo):
        orden = self._carriles_preferentes(vehiculo)
        preferentes = orden[:-1] if self.politica_especializada else orden
        auxiliar = orden[-1] if self.politica_especializada else None

        candidatos = [i for i in preferentes if self.carriles[i].cabe(vehiculo)]

        # El carril auxiliar solo se utiliza si no hay espacio en los preferentes.
        if not candidatos and auxiliar is not None:
            if self.carriles[auxiliar].cabe(vehiculo):
                candidatos = [auxiliar]

        if not candidatos:
            return None

        # Best Fit: elegir el carril que deje menos espacio libre tras la entrada.
        indice = min(
            candidatos,
            key=lambda i: (self.carriles[i].libre - vehiculo.espacio, i),
        )

        if not self.carriles[indice].entrar(vehiculo):
            return None
        return indice + 1

    def atender_espera(self):
        """Ingresa los vehículos que quepan, sin bloquear toda la espera.

        Se conserva el orden relativo de los vehículos que siguen esperando.
        Un vehículo posterior puede entrar antes si el que está delante no cabe.
        """
        movimientos = []
        ingresados = set()
        pendientes = deque()

        while self.espera:
            vehiculo = self.espera.popleft()
            numero = self.asignar(vehiculo)

            if numero is None:
                pendientes.append(vehiculo)
            else:
                ingresados.add(vehiculo.identificador)
                movimientos.append(
                    f"{vehiculo.identificador} ({NOMBRES_TIPO[vehiculo.tipo]}) "
                    f"entró al carril {numero}."
                )

        self.espera = pendientes
        return movimientos, ingresados

    def llegada(self, tipo):
        if tipo not in TAMANOS:
            return ["Tipo de vehículo inválido."]

        if TAMANOS[tipo] > self.capacidad:
            return [
                f"No cabe un {NOMBRES_TIPO[tipo]} en ningún carril: requiere "
                f"{TAMANOS[tipo]} unidades y cada carril tiene {self.capacidad}."
            ]

        self.secuencia += 1
        vehiculo = Vehiculo(f"V{self.secuencia}", tipo)

        # Se agrega al final para no saltarse a los vehículos que ya esperaban.
        self.espera.append(vehiculo)
        mensajes, ingresados = self.atender_espera()

        # El set permite saber en tiempo promedio O(1) si entró esta llegada.
        if vehiculo.identificador not in ingresados:
            mensajes.append(
                f"{vehiculo.identificador} ({NOMBRES_TIPO[tipo]}) "
                "está en espera externa."
            )
        return mensajes

    def hay_vehiculos(self):
        return any(carril.cantidad > 0 for carril in self.carriles)

    def salida(self, numero):
        if not isinstance(numero, int) or isinstance(numero, bool):
            return ["El número de carril debe ser un entero."]
        if not 1 <= numero <= len(self.carriles):
            return ["Número de carril inválido."]

        vehiculo = self.carriles[numero - 1].salir()
        if vehiculo is None:
            return ["El carril está vacío."]

        mensajes = [
            f"Salió {vehiculo.identificador} ({NOMBRES_TIPO[vehiculo.tipo]}) "
            f"del carril {numero}."
        ]
        movimientos, _ = self.atender_espera()
        mensajes.extend(movimientos)
        return mensajes

    def mostrar(self):
        """Devuelve el estado del peaje como texto, sin imprimirlo."""
        lineas = [
            "\nESTADO DEL PEAJE — salida ← frente de cada cola",
            f"Capacidad por carril: {self.capacidad} unidades "
            f"(autos configurados × 2).",
        ]

        for numero, carril in enumerate(self.carriles, 1):
            cola = " → ".join(
                f"{v.identificador}:{NOMBRES_TIPO[v.tipo]}"
                for v in carril.vehiculos()
            ) or "vacío"

            barra = "#" * carril.ocupado + "." * carril.libre
            lineas.extend([
                f"\nCarril {numero}: {cola}",
                f"[{barra}] Ocupado: {carril.ocupado}/{carril.capacidad}; "
                f"libre: {carril.libre} unidades",
                f"Caben: {carril.libre // 2} autos O "
                f"{carril.libre} motos O {carril.libre // 5} tráileres",
            ])

        espera = ", ".join(
            f"{v.identificador}:{NOMBRES_TIPO[v.tipo]}" for v in self.espera
        )
        lineas.extend([
            f"\nEspera externa: {espera or 'ninguno'}",
            "Las cantidades que caben son alternativas, no se suman.",
        ])
        return "\n".join(lineas)


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
    print(f"Capacidad por carril: {autos} × 2 = {peaje.capacidad} unidades.")

    if peaje.politica_especializada:
        print(
            "Política de cuatro carriles: carril 1 preferente para tráileres; "
            "carriles 2 y 3 para autos y motos; carril 4 auxiliar."
        )
    else:
        print(
            "Política flexible: todos los carriles admiten vehículos que quepan. "
            "La asignación utiliza Best Fit."
        )
    print("Las salidas de cada carril se procesan en orden FIFO.")

    if peaje.capacidad < TAMANOS["trailer"]:
        print("Con esta capacidad no caben tráileres en los carriles.")

    while True:
        print(
            "\n1. Entrada de vehículo"
            "\n2. Salida de vehículo"
            "\n3. Ver espacios disponibles"
            "\n4. Terminar"
        )
        opcion = leer_entero("Selecciona una opción: ", maximo=4)

        if opcion == 1:
            print("1. Moto\n2. Auto\n3. Tráiler")
            tipo = ("moto", "auto", "trailer")[
                leer_entero("Tipo: ", maximo=3) - 1
            ]
            print("\n".join(peaje.llegada(tipo)))

        elif opcion == 2:
            if not peaje.hay_vehiculos():
                print("No hay vehículos dentro del peaje para dar salida.")
                continue

            print(peaje.mostrar())
            carril = leer_entero(
                "¿De qué carril sale el primer vehículo? ",
                maximo=numero,
            )
            print("\n".join(peaje.salida(carril)))

        elif opcion == 3:
            print(peaje.mostrar())

        else:
            print("Simulación finalizada.")
            break


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSimulación finalizada.")