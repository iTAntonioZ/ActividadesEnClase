"""Peaje con colas circulares y espera con equidad.
Capacidad por carril = autos_por_carril * 2 unidades.
Los tamanos 1, 2 y 5 son equivalencias didacticas, no medidas reales.
"""
from collections import deque
from dataclasses import dataclass

TAMANOS = {"moto": 1, "auto": 2, "trailer": 5}
SENTIDOS = ("ida", "vuelta")
LIMITE_ADELANTAMIENTOS = 3


def entero_positivo(valor):
    return type(valor) is int and valor > 0


@dataclass(frozen=True)
class Vehiculo:
    identificador: str
    tipo: str
    sentido: str = "ida"

    def __post_init__(self):
        if self.tipo not in TAMANOS or self.sentido not in SENTIDOS:
            raise ValueError("Tipo o sentido invalido.")

    @property
    def espacio(self):
        return TAMANOS[self.tipo]

    @property
    def grupo(self):
        return "pesados" if self.tipo == "trailer" else "ligeros"


@dataclass
class Pendiente:
    vehiculo: Vehiculo
    adelantamientos: int = 0


class ColaCircular:
    def __init__(self, capacidad):
        if not entero_positivo(capacidad):
            raise ValueError("La capacidad debe ser un entero positivo.")
        self.capacidad = capacidad
        # Una referencia por vehiculo, no por unidad de espacio.
        # El maximo de objetos ocurre cuando todos son motos.
        self.max_vehiculos = capacidad // min(TAMANOS.values())
        self.datos = [None] * self.max_vehiculos
        self.frente = self.final = self.cantidad = self.ocupado = 0

    @property
    def libre(self):
        return self.capacidad - self.ocupado

    def cabe(self, vehiculo):
        return (self.libre >= vehiculo.espacio
                and self.cantidad < self.max_vehiculos)

    def entrar(self, vehiculo):
        if not self.cabe(vehiculo):
            return False
        self.datos[self.final] = vehiculo
        self.final = (self.final + 1) % self.max_vehiculos
        self.cantidad += 1
        self.ocupado += vehiculo.espacio
        return True

    def salir(self):
        if not self.cantidad:
            return None
        vehiculo = self.datos[self.frente]
        self.datos[self.frente] = None
        self.frente = (self.frente + 1) % self.max_vehiculos
        self.cantidad -= 1
        self.ocupado -= vehiculo.espacio
        return vehiculo

    def vehiculos(self):
        return [self.datos[(self.frente + i) % self.max_vehiculos]
                for i in range(self.cantidad)]


class Carril(ColaCircular):
    def __init__(self, capacidad, funcion):
        super().__init__(capacidad)
        self.funcion = funcion
        self.abierto = True
        self.sentido = "ida"
        self.grupo_auxiliar = None

    def compatible(self, vehiculo):
        if not self.abierto or self.sentido != vehiculo.sentido:
            return False
        if self.funcion == "pesados":
            return vehiculo.grupo == "pesados"
        if self.funcion == "ligeros":
            return vehiculo.grupo == "ligeros"
        if self.funcion == "auxiliar":
            return self.grupo_auxiliar in (None, vehiculo.grupo)
        return True  # Carril mixto cuando solo existe uno.

    def entrar(self, vehiculo):
        if not self.compatible(vehiculo) or not super().entrar(vehiculo):
            return False
        if self.funcion == "auxiliar":
            self.grupo_auxiliar = vehiculo.grupo
        return True

    def salir(self):
        vehiculo = super().salir()
        if not self.cantidad:
            self.grupo_auxiliar = None
        return vehiculo


class Peaje:
    def __init__(self, numero_carriles, autos_por_carril):
        if not all(entero_positivo(v) for v in (numero_carriles, autos_por_carril)):
            raise ValueError("Las cantidades deben ser enteros positivos.")
        self.capacidad = autos_por_carril * TAMANOS["auto"]
        if numero_carriles == 1:
            funciones = ["mixto"]
        else:
            # Evitar un principal inutilizable cuando no caben trailers.
            primero = "pesados" if self.capacidad >= TAMANOS["trailer"] else "ligeros"
            funciones = [primero, "ligeros"] + ["auxiliar"] * (numero_carriles - 2)
        self.carriles = [Carril(self.capacidad, f) for f in funciones]
        self.espera = deque()
        self.secuencia = 0

    @property
    def hay_vehiculos(self):
        return any(c.cantidad for c in self.carriles)

    def asignar(self, vehiculo):
        candidatos = (i for i, c in enumerate(self.carriles)
                      if c.compatible(vehiculo) and c.cabe(vehiculo))
        # Sin tiempos medidos, equilibrar por cantidad de vehiculos.
        # Desempates: mejor ajuste, preferencia por principal y primer indice.
        indice = min(candidatos, default=None, key=lambda i: (
            self.carriles[i].cantidad,
            self.carriles[i].libre - vehiculo.espacio,
            self.carriles[i].funcion == "auxiliar", i))
        if indice is None:
            return None
        self.carriles[indice].entrar(vehiculo)
        return indice + 1

    def atender_espera(self, objetivo=None):
        """Hasta tres adelantamientos al primero que no puede ingresar.

        Al alcanzar el limite se suspenden TODOS los adelantamientos hasta
        admitirlo. Puede quedar espacio ocioso a cambio de proteger su turno.
        Se reconstruye el deque sin eliminar posiciones intermedias.
        """
        mensajes = []
        pendientes = deque()
        bloqueado = None
        carril_objetivo = None
        while self.espera:
            if bloqueado and bloqueado.adelantamientos >= LIMITE_ADELANTAMIENTOS:
                pendientes.extend(self.espera)
                self.espera.clear()
                break
            pendiente = self.espera.popleft()
            vehiculo = pendiente.vehiculo
            numero = self.asignar(vehiculo)
            if numero is None:
                pendientes.append(pendiente)
                if bloqueado is None:
                    bloqueado = pendiente
            else:
                if bloqueado:
                    bloqueado.adelantamientos += 1
                if vehiculo.identificador == objetivo:
                    carril_objetivo = numero
                mensajes.append(f"{vehiculo.identificador} ({vehiculo.tipo}, "
                                f"{vehiculo.sentido}) entro al carril {numero}.")
        self.espera = pendientes
        return mensajes, carril_objetivo

    def llegada(self, tipo, sentido="ida"):
        if tipo not in TAMANOS or sentido not in SENTIDOS:
            return ["Tipo o sentido invalido."]
        if TAMANOS[tipo] > self.capacidad:
            return [f"No cabe un {tipo}: requiere {TAMANOS[tipo]} unidades "
                    f"y cada carril tiene {self.capacidad}."]
        self.secuencia += 1
        vehiculo = Vehiculo(f"V{self.secuencia}", tipo, sentido)
        self.espera.append(Pendiente(vehiculo))
        mensajes, numero = self.atender_espera(vehiculo.identificador)
        # Estado directo: evita una segunda busqueda con 'in'.
        if numero is None:
            mensajes.append(f"{vehiculo.identificador} ({tipo}, {sentido}) "
                            "esta en espera externa.")
        return mensajes

    def salida(self, numero):
        if type(numero) is not int or not 1 <= numero <= len(self.carriles):
            return ["Numero de carril invalido."]
        vehiculo = self.carriles[numero - 1].salir()
        if vehiculo is None:
            return ["El carril esta vacio."]
        movimientos, _ = self.atender_espera()
        return [f"Salio {vehiculo.identificador} ({vehiculo.tipo}) "
                f"del carril {numero}."] + movimientos

    def configurar_carril(self, numero, abierto, sentido):
        if (type(numero) is not int or not 1 <= numero <= len(self.carriles)
                or type(abierto) is not bool or sentido not in SENTIDOS):
            return ["Configuracion invalida."]
        carril = self.carriles[numero - 1]
        if carril.cantidad and sentido != carril.sentido:
            return ["Para cambiar el sentido, cierra el carril y vacialo primero."]
        carril.abierto = abierto
        carril.sentido = sentido
        mensajes = [f"Carril {numero}: {'abierto' if abierto else 'cerrado'}, {sentido}."]
        movimientos, _ = self.atender_espera()
        return mensajes + movimientos

    def mostrar(self):
        lineas = ["\nESTADO DEL PEAJE - el primero de la lista es el proximo en salir."]
        for numero, c in enumerate(self.carriles, 1):
            cola = " -> ".join(f"{v.identificador}:{v.tipo}" for v in c.vehiculos()) or "vacio"
            funcion = c.funcion
            if funcion == "auxiliar":
                funcion += f" ({c.grupo_auxiliar or 'disponible'})"
            llenos = c.ocupado * 20 // c.capacidad
            barra = "#" * llenos + "." * (20 - llenos)
            lineas.extend([
                f"\nCarril {numero}: {funcion}; {c.sentido}; "
                f"{'abierto' if c.abierto else 'cerrado para entradas'}",
                cola,
                f"[{barra}] Ocupado: {c.ocupado}/{c.capacidad}; libre: {c.libre} unidades."
            ])
            disponibles = ", ".join(
                f"{c.libre // espacio} {tipo}(s)"
                for tipo, espacio in TAMANOS.items()
                if c.compatible(Vehiculo('consulta', tipo, c.sentido)))
            lineas.append("Capacidad compatible (alternativas): " + (disponibles or "ninguna"))
        espera = ", ".join(
            f"{p.vehiculo.identificador}:{p.vehiculo.tipo}/{p.vehiculo.sentido} "
            f"(adelantamientos: {p.adelantamientos}/{LIMITE_ADELANTAMIENTOS})"
            for p in self.espera)
        lineas.append(f"\nEspera externa: {espera or 'ninguno'}")
        lineas.append("Las capacidades por tipo son alternativas, no se suman. "
                      "La espera protegida puede impedir entradas aunque haya espacio.")
        return "\n".join(lineas)


def leer_entero(mensaje, minimo=1, maximo=None):
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo and (maximo is None or valor <= maximo):
                return valor
        except ValueError:
            pass
        print("Ingresa un numero entero dentro del rango permitido.")


def pedir_sentido():
    print("1. Ida\n2. Vuelta")
    return SENTIDOS[leer_entero("Sentido: ", maximo=2) - 1]


def main():
    print("SIMULADOR DE PEAJE")
    numero = leer_entero("Cuantos carriles hay? ")
    autos = leer_entero("Cuantos autos caben en cada carril? ")
    peaje = Peaje(numero, autos)
    print("\nCapacidad = autos por carril x 2 unidades.")
    print("Moto = 1, auto = 2, trailer = 5. Valores didacticos.")
    print("Con un carril: mixto. Con dos o mas: principal de trailers, "
          "principal de ligeros y el resto auxiliares.")
    if peaje.capacidad < TAMANOS["trailer"]:
        print("No caben trailers: los principales se destinan a vehiculos ligeros.")
    print("Todos comienzan abiertos y de ida; puedes configurar desvios.")
    print("Se equilibra por cantidad; en empate, mejor ajuste de espacio. "
          "Cada auxiliar conserva su grupo hasta vaciarse.")
    print(f"Maximo {LIMITE_ADELANTAMIENTOS} adelantamientos al primero bloqueado.")

    while True:
        print("\n1. Entrada de vehiculo\n2. Salida de vehiculo"
              "\n3. Ver espacios disponibles\n4. Terminar\n5. Abrir, cerrar o cambiar sentido")
        opcion = leer_entero("Selecciona una opcion: ", maximo=5)
        if opcion == 1:
            print("1. Moto\n2. Auto\n3. Trailer")
            tipo = ("moto", "auto", "trailer")[leer_entero("Tipo: ", maximo=3) - 1]
            print("\n".join(peaje.llegada(tipo, pedir_sentido())))
        elif opcion == 2:
            if not peaje.hay_vehiculos:
                print("No hay vehiculos dentro del peaje.")
                continue
            print(peaje.mostrar())
            carril = leer_entero("De que carril sale el primer vehiculo? ", maximo=numero)
            print("\n".join(peaje.salida(carril)))
        elif opcion == 3:
            print(peaje.mostrar())
        elif opcion == 5:
            print(peaje.mostrar())
            carril = leer_entero("Carril que deseas configurar: ", maximo=numero)
            print("1. Abierto\n2. Cerrado para nuevas entradas")
            abierto = leer_entero("Estado: ", maximo=2) == 1
            print("\n".join(peaje.configurar_carril(carril, abierto, pedir_sentido())))
        else:
            print("Simulacion finalizada.")
            break


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSimulacion finalizada.")
