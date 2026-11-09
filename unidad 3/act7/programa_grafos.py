"""ADA7: grafo ponderado de siete estados mexicanos. Python 3.9 o superior.

Ejecutar: python programa_grafos.py
Opcional: python programa_grafos.py --dibujar
Los costos son supuestos académicos en MXN, no tarifas reales.
"""

import argparse
import heapq
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser


ESTADOS = ["Jalisco", "Guanajuato", "Michoacán", "Querétaro",
           "Hidalgo", "Estado de México", "Puebla"]
# Conexiones seleccionadas entre estados vecinos. Grafo no dirigido:
# cada traslado cuesta lo mismo en ambos sentidos.
CONEXIONES = [
    (0, 1, 350), (0, 2, 300), (1, 2, 250), (1, 3, 200),
    (2, 3, 320), (2, 5, 400), (3, 4, 220), (3, 5, 280),
    (4, 5, 180), (4, 6, 300), (5, 6, 250),
]


def construir_grafo():
    grafo = {estado: {} for estado in ESTADOS}
    for a, b, costo in CONEXIONES:
        grafo[ESTADOS[a]][ESTADOS[b]] = costo
        grafo[ESTADOS[b]][ESTADOS[a]] = costo
    return grafo


def sin_repetir(grafo, inicio):
    """Backtracking: compara todos los caminos hamiltonianos desde inicio."""
    mejor_ruta, mejor_costo = None, float("inf")

    def explorar(ruta, visitados, costo):
        nonlocal mejor_ruta, mejor_costo
        if costo >= mejor_costo:
            return
        if len(visitados) == len(grafo):
            mejor_ruta, mejor_costo = ruta[:], costo
            return
        for vecino, peso in grafo[ruta[-1]].items():
            if vecino not in visitados:
                explorar(ruta + [vecino], visitados | {vecino}, costo + peso)

    explorar([inicio], {inicio}, 0)
    return mejor_ruta, mejor_costo


def con_repeticion(grafo, inicio):
    """Dijkstra sobre (estado actual, máscara de visitados, hubo repetición).

    Se permite volver a cualquier estado y reutilizar conexiones. La meta
    exige visitar los siete estados y repetir al menos uno. Los pesos positivos
    permiten hallar el mínimo, incluso cuando hay ciclos en el grafo original.
    """
    indice = {estado: i for i, estado in enumerate(grafo)}
    todos = (1 << len(grafo)) - 1
    origen = (inicio, 1 << indice[inicio], False)
    distancias = {origen: 0}
    anteriores = {}
    pendientes = [(0, origen)]
    while pendientes:
        costo, actual = heapq.heappop(pendientes)
        if costo != distancias[actual]:
            continue
        estado, mascara, repetido = actual
        if mascara == todos and repetido:
            ruta = []
            while True:
                ruta.append(actual[0])
                if actual == origen:
                    break
                actual = anteriores[actual]
            return ruta[::-1], costo
        for vecino, peso in grafo[estado].items():
            bit = 1 << indice[vecino]
            siguiente = (vecino, mascara | bit, repetido or bool(mascara & bit))
            nuevo_costo = costo + peso
            if nuevo_costo < distancias.get(siguiente, float("inf")):
                distancias[siguiente] = nuevo_costo
                anteriores[siguiente] = actual
                heapq.heappush(pendientes, (nuevo_costo, siguiente))
    return None, float("inf")


def describir(ruta, costo, grafo):
    if ruta is None:
        return "No existe un recorrido que cumpla las condiciones."
    tramos = [f"{a} -> {b}: ${grafo[a][b]:,} MXN"
              for a, b in zip(ruta, ruta[1:])]
    return " -> ".join(ruta) + "\n" + "\n".join(tramos) + f"\nCosto total: ${costo:,} MXN"


def guardar_grafico(grafo, resultados=None):
    """Python calcula todas las rutas; la interfaz permite explorarlas."""
    rutas = {}
    for inicio in ESTADOS:
        rutas[inicio] = {}
        for clave, resolver in [("a", sin_repetir), ("b", con_repeticion)]:
            ruta, costo = resolver(grafo, inicio)
            rutas[inicio][clave] = {"ruta": ruta, "costo": costo if ruta else None}
    datos = {"estados": ESTADOS, "conexiones": CONEXIONES, "rutas": rutas}
    carpeta = Path(__file__).resolve().parent
    plantilla = (carpeta / "interfaz.html").read_text(encoding="utf-8")
    contenido = plantilla.replace("__DATOS_PYTHON__", json.dumps(datos, ensure_ascii=False))
    archivo = carpeta / "grafo_estados.html"
    archivo.write_text(contenido, encoding="utf-8")
    return archivo


def abrir_interfaz(archivo):
    """Sirve solo la interfaz en localhost; no expone carpetas del equipo."""
    contenido = archivo.read_bytes()

    class InterfazHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path not in ("/", "/grafo_estados.html"):
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(contenido)))
            self.end_headers()
            self.wfile.write(contenido)

        def log_message(self, *args):
            pass

    with ThreadingHTTPServer(("127.0.0.1", 0), InterfazHandler) as servidor:
        url = f"http://127.0.0.1:{servidor.server_port}/"
        print(f"Interfaz: {url}\nMantén esta terminal abierta. Ctrl+C para cerrar.")
        webbrowser.open(url)
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\nInterfaz cerrada.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dibujar", action="store_true", help="Abrir la interfaz (comportamiento predeterminado)")
    parser.add_argument("--solo-html", action="store_true", help="Generar HTML sin abrir el navegador ni iniciar el servidor")
    args = parser.parse_args()
    grafo = construir_grafo()
    for titulo, resolver in [("A) Sin repetir", sin_repetir), ("B) Con repetición", con_repeticion)]:
        ruta, costo = resolver(grafo, "Jalisco")
        print(f"\n{titulo}\n{describir(ruta, costo, grafo)}")
    archivo = guardar_grafico(grafo)
    print(f"\nInterfaz generada: {archivo}")
    if not args.solo_html:
        abrir_interfaz(archivo)


if __name__ == "__main__":
    main()
