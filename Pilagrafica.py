
import tkinter as tk

# Configuración
BG = "#242424"
PANEL = "#303030"
INPUT = "#383838"
TEXT = "#F5F5F5"
MUTED = "#AAAAAA"
ACCENT = "#A8C7FA"

MAX_ELEMENTOS = 6
pila = []


def validar_numero(valor):
    if valor == "" or valor == "-":
        return True

    if valor.startswith("-"):
        return valor[1:].isdigit()

    return valor.isdigit()


def apilar():
    valor = entrada.get().strip()

    if valor in ("", "-"):
        estado.config(text="Ingresa un número válido")
        return

    if len(pila) >= MAX_ELEMENTOS:
        estado.config(text="La pila está llena")
        return

    numero = int(valor)
    pila.append(numero)

    entrada.delete(0, tk.END)
    estado.config(text=f"Elemento {numero} agregado")
    dibujar_pila()


def desapilar():
    if not pila:
        estado.config(text="La pila está vacía")
        return

    numero = pila.pop()
    estado.config(text=f"Elemento {numero} eliminado")
    dibujar_pila()


def ver_cima():
    if pila:
        estado.config(text=f"Cima actual: {pila[-1]}")
    else:
        estado.config(text="La pila está vacía")


def vaciar():
    pila.clear()
    estado.config(text="Pila vaciada")
    dibujar_pila()


def dibujar_pila():
    canvas.delete("all")

    ancho = 190
    alto = 42
    separacion = 8
    x = 15
    base = 285

    for i, numero in enumerate(pila):
        y2 = base - i * (alto + separacion)
        y1 = y2 - alto

        cima = i == len(pila) - 1
        color = ACCENT if cima else "#494949"
        texto = "#202C40" if cima else TEXT

        canvas.create_rectangle(
            x, y1, x + ancho, y2,
            fill=color,
            outline=""
        )

        canvas.create_text(
            x + ancho / 2,
            (y1 + y2) / 2,
            text=str(numero),
            fill=texto,
            font=("Segoe UI", 13, "bold")
        )

    canvas.create_line(
        10, 295, 210, 295,
        fill="#DDDDDD",
        width=4
    )

    contador.config(
        text=f"{len(pila)} / {MAX_ELEMENTOS} elementos"
    )


def crear_boton(parent, texto, comando, color, fg=TEXT):
    return tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=color,
        fg=fg,
        activebackground="#555555",
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 11),
        height=2
    )


# Ventana principal
ventana = tk.Tk()
ventana.title("Stack Visualizer")
ventana.geometry("650x500")
ventana.resizable(False, False)
ventana.configure(bg=BG)

# Encabezado
encabezado = tk.Frame(ventana, bg=BG)
encabezado.pack(fill="x", padx=25, pady=(20, 5))

tk.Label(
    encabezado,
    text="STACK VISUALIZER",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 18, "bold")
).pack(anchor="w")

tk.Label(
    encabezado,
    text="Simulador de pila - LIFO",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(anchor="w")


# Barra de estado
# Se crea antes del contenido para reservar espacio inferior
pie = tk.Frame(
    ventana,
    bg=PANEL,
    height=45
)

pie.pack(
    side="bottom",
    fill="x",
    padx=25,
    pady=(5, 15)
)

pie.pack_propagate(False)

estado = tk.Label(
    pie,
    text="Pila lista para operar",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 10)
)
estado.pack(side="left", padx=15)

contador = tk.Label(
    pie,
    text="0 / 6 elementos",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 10)
)
contador.pack(side="right", padx=15)


# Contenedor principal
contenido = tk.Frame(ventana, bg=BG)
contenido.pack(
    padx=25,
    pady=(10, 5),
    fill="both",
    expand=True
)

# Panel izquierdo
panel_pila = tk.Frame(
    contenido,
    bg=PANEL,
    width=240,
    height=320
)
panel_pila.pack(
    side="left",
    padx=(0, 25),
    anchor="n"
)
panel_pila.pack_propagate(False)

canvas = tk.Canvas(
    panel_pila,
    bg=PANEL,
    width=220,
    height=305,
    highlightthickness=0
)
canvas.pack(pady=5)


# Panel derecho
panel_control = tk.Frame(
    contenido,
    bg=BG,
    width=310
)
panel_control.pack(
    side="left",
    fill="y",
    anchor="n"
)

tk.Label(
    panel_control,
    text="Nuevo elemento",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(anchor="w", pady=(0, 5))

validacion = ventana.register(validar_numero)

entrada = tk.Entry(
    panel_control,
    bg=INPUT,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    font=("Segoe UI", 13),
    validate="key",
    validatecommand=(validacion, "%P")
)
entrada.pack(
    fill="x",
    ipady=8,
    pady=(0, 12)
)

crear_boton(
    panel_control,
    "+ Apilar",
    apilar,
    ACCENT,
    "#202C40"
).pack(fill="x", pady=4)

crear_boton(
    panel_control,
    "- Desapilar",
    desapilar,
    "#424242"
).pack(fill="x", pady=4)

crear_boton(
    panel_control,
    "Ver cima",
    ver_cima,
    "#424242"
).pack(fill="x", pady=4)

crear_boton(
    panel_control,
    "Vaciar pila",
    vaciar,
    "#383838"
).pack(fill="x", pady=4)


# Ejecutar programa
ventana.bind("<Return>", lambda event: apilar())

dibujar_pila()
entrada.focus_set()

ventana.mainloop()
