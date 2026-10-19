from collections import deque
from dataclasses import dataclass


ESPACIO = {"moto": 1, "auto": 2, "trailer": 5}


@dataclass
class Vehiculo:
    identificador: str
    tipo: str

    @property
    def espacio(self):
        return ESPACIO[self.tipo]

    @property
    def grupo(self):
        return "pesados" if self.tipo == "trailer" else "ligeros"


class ColaCircular:
    def __init__(self, nombre, capacidad=10):
        self.nombre = nombre
        self.capacidad = capacidad

        # Como mínimo un vehículo ocupa una unidad:
        # nunca habrá más vehículos que posiciones.
        self.datos = [None] * capacidad
        self.frente = 0
        self.final = 0
        self.cantidad = 0
        self.ocupado = 0

    def cabe(self, vehiculo):
        return (
            self.cantidad < len(self.datos)
            and self.ocupado + vehiculo.espacio <= self.capacidad
        )

    def entrar(self, vehiculo):
        if not self.cabe(vehiculo):
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

    def contenido(self):
        return [
            self.datos[(self.frente + i) % len(self.datos)]
            for i in range(self.cantidad)
        ]


class Peaje:
    def __init__(self):
        self.carriles = [
            ColaCircular("Carril 1: tráileres"),
            ColaCircular("Carril 2: ligeros"),
            ColaCircular("Carril 3: ligeros"),
            ColaCircular("Carril 4: auxiliar"),
        ]
        self.espera = deque()
        self.funcion_auxiliar = None

    def asignar(self, vehiculo):
        indices = [0] if vehiculo.grupo == "pesados" else [1, 2]

        disponibles = [
            i for i in indices if self.carriles[i].cabe(vehiculo)
        ]

        if disponibles:
            # Menos vehículos; en empate, primer carril.
            elegido = min(
                disponibles,
                key=lambda i: (self.carriles[i].cantidad, i)
            )
            self.carriles[elegido].entrar(vehiculo)
            return True

        auxiliar = self.carriles[3]
        compatible = self.funcion_auxiliar in (None, vehiculo.grupo)

        if compatible and auxiliar.cabe(vehiculo):
            auxiliar.entrar(vehiculo)
            self.funcion_auxiliar = vehiculo.grupo
            return True

        return False

    def llegada(self, identificador, tipo):
        if tipo not in ESPACIO:
            raise ValueError("Tipo válido: moto, auto o trailer")

        vehiculo = Vehiculo(identificador, tipo)
        self.espera.append(vehiculo)
        self.atender_espera()

    def atender_espera(self):
        # Respeta el orden de llegada de la espera externa.
        while self.espera:
            if not self.asignar(self.espera[0]):
                break
            self.espera.popleft()

    def salida(self, numero_carril):
        if numero_carril not in range(1, 5):
            raise ValueError("El carril debe estar entre 1 y 4")

        vehiculo = self.carriles[numero_carril - 1].salir()

        if self.carriles[3].cantidad == 0:
            self.funcion_auxiliar = None

        self.atender_espera()
        return vehiculo

    def mostrar(self, instante):
        print(f"\n--- Instante {instante} ---")

        for carril in self.carriles:
            contenido = ", ".join(
                f"{v.identificador}({v.tipo})"
                for v in carril.contenido()
            )
            print(
                f"{carril.nombre}: [{contenido}] "
                f"| Espacio: {carril.ocupado}/{carril.capacidad}"
            )

        pendientes = ", ".join(v.identificador for v in self.espera)
        print(f"Espera externa: [{pendientes}]")
        print(f"Función auxiliar: {self.funcion_auxiliar or 'disponible'}")


# Simulación: cada evento representa un instante.
peaje = Peaje()

eventos = [
    ("entrada", "T1", "trailer"),
    ("entrada", "T2", "trailer"),
    ("entrada", "T3", "trailer"),
    ("entrada", "A1", "auto"),
    ("entrada", "M1", "moto"),
    ("entrada", "T4", "trailer"),
    ("entrada", "T5", "trailer"),
    ("salida", 1),
]

for instante, evento in enumerate(eventos, start=1):
    if evento[0] == "entrada":
        peaje.llegada(evento[1], evento[2])
    else:
        peaje.salida(evento[1])

    peaje.mostrar(instante)