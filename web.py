import json
import os
from datetime import datetime


class Pila:
    def __init__(self):
        self.elementos = []

    def apilar(self, elemento):
        self.elementos.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop()

    def esta_vacia(self):
        return len(self.elementos) == 0

    def limpiar(self):
        self.elementos.clear()

    def mostrar(self):
        return self.elementos.copy()


class Navegador:
    def __init__(self):
        self.atras = Pila()
        self.adelante = Pila()
        self.historial = Pila()
        self.actual = None

        self.archivo = "historial.json"
        self.cargar_datos()

    def guardar_datos(self):
        datos = {
            "actual": self.actual,
            "atras": self.atras.mostrar(),
            "adelante": self.adelante.mostrar(),
            "historial": self.historial.mostrar()
        }

        temporal = self.archivo + ".tmp"

        try:
            with open(temporal, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

            os.replace(temporal, self.archivo)

        except OSError as error:
            print("Error al guardar:", error)

    def cargar_datos(self):
        if not os.path.exists(self.archivo):
            return

        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            self.actual = datos.get("actual")

            for pagina in datos.get("atras", []):
                self.atras.apilar(pagina)

            for pagina in datos.get("adelante", []):
                self.adelante.apilar(pagina)

            for visita in datos.get("historial", []):
                self.historial.apilar(visita)

            print("Historial recuperado correctamente.")

        except (OSError, ValueError, TypeError, AttributeError):
            print("No se pudo recuperar el historial.")
            self.actual = None
            self.atras.limpiar()
            self.adelante.limpiar()
            self.historial.limpiar()

    def visitar(self, pagina):
        pagina = pagina.strip()

        if not pagina:
            print("Ingresa una dirección válida.")
            return

        if " " in pagina:
            print("La dirección no debe contener espacios.")
            return

        if not pagina.startswith(("http://", "https://")):
            pagina = "https://" + pagina

        if self.actual is not None:
            self.atras.apilar(self.actual)

        self.actual = pagina
        self.adelante.limpiar()

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

        self.historial.apilar({
            "pagina": pagina,
            "fecha": fecha
        })

        self.guardar_datos()
        print("\nVisitando:", pagina)

    def retroceder(self):
        if self.atras.esta_vacia():
            print("No hay páginas anteriores.")
            return

        self.adelante.apilar(self.actual)
        self.actual = self.atras.desapilar()

        self.guardar_datos()
        print("Página actual:", self.actual)

    def avanzar(self):
        if self.adelante.esta_vacia():
            print("No hay páginas para avanzar.")
            return

        self.atras.apilar(self.actual)
        self.actual = self.adelante.desapilar()

        self.guardar_datos()
        print("Página actual:", self.actual)

    def mostrar_actual(self):
        if self.actual is None:
            print("No hay ninguna página abierta.")
        else:
            print("\nPágina actual:", self.actual)

    def mostrar_historial(self):
        visitas = self.historial.mostrar()

        if not visitas:
            print("El historial está vacío.")
            return

        print("\n========= HISTORIAL =========")

        for i, visita in enumerate(reversed(visitas), 1):
            print(f"{i}. {visita['pagina']}")
            print(f"   Fecha: {visita['fecha']}")

    def limpiar_historial(self):
        self.historial.limpiar()
        self.guardar_datos()
        print("Historial de visitas eliminado.")


def menu():
    navegador = Navegador()

    while True:
        print("\n========== NAVEGADOR ==========")
        print("1. Visitar página")
        print("2. Retroceder")
        print("3. Avanzar")
        print("4. Página actual")
        print("5. Mostrar historial")
        print("6. Limpiar historial")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            pagina = input("URL: ")
            navegador.visitar(pagina)

        elif opcion == "2":
            navegador.retroceder()

        elif opcion == "3":
            navegador.avanzar()

        elif opcion == "4":
            navegador.mostrar_actual()

        elif opcion == "5":
            navegador.mostrar_historial()

        elif opcion == "6":
            confirmar = input(
                "¿Eliminar historial? (s/n): "
            ).lower()

            if confirmar == "s":
                navegador.limpiar_historial()

        elif opcion == "0":
            navegador.guardar_datos()
            print("Datos guardados. Hasta pronto.")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
