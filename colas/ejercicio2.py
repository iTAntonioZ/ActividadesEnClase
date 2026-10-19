"""Simulación de atención por servicio en una compañía de seguros."""
from cola import Cola


class SistemaSeguros:
    def __init__(self, servicios):
        if servicios < 1:
            raise ValueError("Debe existir al menos un servicio.")
        self.colas = {numero: Cola() for numero in range(1, servicios + 1)}
        self.siguientes = {numero: 1 for numero in self.colas}

    def validar_servicio(self, servicio):
        if servicio not in self.colas:
            raise ValueError(f"Servicio inexistente. Elige entre 1 y {len(self.colas)}.")

    def llegada(self, servicio):
        self.validar_servicio(servicio)
        turno = self.siguientes[servicio]
        self.colas[servicio].encolar(turno)
        self.siguientes[servicio] += 1
        return turno

    def atender(self, servicio):
        self.validar_servicio(servicio)
        if self.colas[servicio].esta_vacia():
            return None
        return self.colas[servicio].desencolar()


def main():
    print("ATENCIÓN DE SERVICIOS — COMPAÑÍA DE SEGUROS")
    while True:
        try:
            sistema = SistemaSeguros(int(input("Cantidad de servicios: ")))
            break
        except ValueError:
            print("Escribe un entero mayor que cero.")
    print("C n: llegada al servicio n | A n: atender servicio n | S: salir")
    print("También puedes escribir C1 o A1. Los turnos son independientes por servicio.")
    while True:
        comando = input("> ").strip().upper()
        if comando == "S":
            print("Simulación finalizada.")
            break
        try:
            if not comando or comando[0] not in ("C", "A"):
                raise ValueError("Usa C seguido del servicio, A seguido del servicio o S.")
            servicio = int(comando[1:].strip())
            if comando[0] == "C":
                turno = sistema.llegada(servicio)
                print(f"Servicio {servicio}: número de atención {turno}.")
            else:
                turno = sistema.atender(servicio)
                if turno is None:
                    print(f"Servicio {servicio}: no hay clientes en espera.")
                else:
                    print(f"Llamando al número {turno} del servicio {servicio}.")
        except ValueError as error:
            print(f"Entrada inválida: {error}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSimulación finalizada.")
