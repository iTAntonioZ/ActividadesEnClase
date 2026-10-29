import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

# ========================================================
# 1. Estructuras de Datos Lineales: Listas Simplemente Enlazadas
# ========================================================

class NodoTexto:
    def __init__(self, dato):
        self.dato = dato.strip()
        self.siguiente = None


class ListaEnlazadaTexto:
    """Lista simplemente enlazada que autogestiona la prevención de duplicados."""
    def __init__(self):
        self.cabeza = None

    def contiene(self, dato):
        actual = self.cabeza
        norm = dato.strip().lower()
        while actual:
            if actual.dato.strip().lower() == norm:
                return True
            actual = actual.siguiente
        return False

    def insertar(self, dato):
        texto = dato.strip()
        if not texto:
            return False, "El texto no puede estar vacío."
        if self.contiene(texto):
            return False, f"'{texto}' ya existe (se omitió duplicado)."

        nuevo = NodoTexto(texto)
        if not self.cabeza:
            self.cabeza = nuevo
            return True, f"'{texto}' agregado con éxito."

        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo
        return True, f"'{texto}' agregado con éxito."

    def eliminar(self, dato):
        if not self.cabeza:
            return False, "La lista está vacía."

        norm = dato.strip().lower()
        if self.cabeza.dato.strip().lower() == norm:
            self.cabeza = self.cabeza.siguiente
            return True, f"'{dato}' eliminado."

        actual = self.cabeza
        while actual.siguiente and actual.siguiente.dato.strip().lower() != norm:
            actual = actual.siguiente

        if actual.siguiente:
            actual.siguiente = actual.siguiente.siguiente
            return True, f"'{dato}' eliminado."

        return False, f"'{dato}' no existe en la lista."

    def modificar(self, dato_viejo, dato_nuevo):
        nuevo_limpio = dato_nuevo.strip()
        if not nuevo_limpio:
            return False, "El nuevo texto no puede estar vacío."

        if dato_viejo.strip().lower() != nuevo_limpio.lower() and self.contiene(nuevo_limpio):
            return False, f"Ya existe '{nuevo_limpio}' en la lista (duplicado)."

        actual = self.cabeza
        norm_viejo = dato_viejo.strip().lower()
        while actual:
            if actual.dato.strip().lower() == norm_viejo:
                actual.dato = nuevo_limpio
                return True, "Actualizado correctamente."
            actual = actual.siguiente
        return False, "Elemento no encontrado."

    def obtener_todos(self):
        items = []
        actual = self.cabeza
        while actual:
            items.append(actual.dato)
            actual = actual.siguiente
        return items

    def cantidad(self):
        conteo = 0
        actual = self.cabeza
        while actual:
            conteo += 1
            actual = actual.siguiente
        return conteo


class Postre:
    def __init__(self, nombre):
        self.nombre = nombre.strip()
        self.ingredientes = ListaEnlazadaTexto()
        self.pasos = ListaEnlazadaTexto()


# ========================================================
# 2. Arreglo POSTRES con Persistencia Automática (JSON)
# ========================================================

ARCHIVO_DATOS = "recetario_postres.json"

class SistemaRecetario:
    def __init__(self):
        self.postres = []
        self.cargar_desde_disco()

    def guardar_en_disco(self):
        """Serializa la estructura enlazada a un archivo JSON local."""
        datos = []
        for p in self.postres:
            datos.append({
                "nombre": p.nombre,
                "ingredientes": p.ingredientes.obtener_todos(),
                "pasos": p.pasos.obtener_todos()
            })
        try:
            with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    def cargar_desde_disco(self):
        """Carga los postres guardados reconstruyendo las listas enlazadas."""
        if not os.path.exists(ARCHIVO_DATOS):
            self._cargar_datos_demo()
            self.guardar_en_disco()
            return

        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                datos = json.load(f)

            self.postres = []
            for item in datos:
                postre = Postre(item["nombre"])
                for ing in item.get("ingredientes", []):
                    postre.ingredientes.insertar(ing)
                for paso in item.get("pasos", []):
                    postre.pasos.insertar(paso)
                self.postres.append(postre)

            # Garantizar que el arreglo permanezca ordenado alfabéticamente
            self.postres.sort(key=lambda x: x.nombre.lower())
        except Exception as e:
            print(f"Error al leer {ARCHIVO_DATOS}, cargando demos: {e}")
            self._cargar_datos_demo()

    def _cargar_datos_demo(self):
        self.postres = []
        self.dar_de_alta_postre(
            "Flan Napolitano",
            ["Leche condensada", "Leche evaporada", "Queso crema", "Huevos", "Vainilla", "Azúcar para caramelo"],
            ["Derretir el azúcar en la flanera a fuego bajo", "Licuar lácteos, huevos y vainilla", "Hornear a baño maría por 50 min", "Enfriar y desmoldar"],
            persistir=False
        )
        self.dar_de_alta_postre(
            "Tiramisú Clásico",
            ["Bizcochos de soletilla", "Café expreso", "Queso mascarpone", "Huevos", "Cacao en polvo"],
            ["Preparar café expreso y dejar enfriar", "Batir yemas con mascarpone", "Remojar bizcochos en el café", "Alternar capas y espolvorear cacao", "Refrigerar 4 horas"],
            persistir=False
        )
        self.dar_de_alta_postre(
            "Carlota de Limón",
            ["Galletas María", "Leche condensada", "Leche evaporada", "Jugo de limón natural"],
            ["Licuar las leches junto al jugo de limón", "Formar una base de galletas en el molde", "Alternar crema de limón con galletas", "Refrigerar mínimo 2 horas"],
            persistir=False
        )

    def buscar_indice(self, nombre):
        ini, fin = 0, len(self.postres) - 1
        buscado = nombre.strip().lower()
        while ini <= fin:
            med = (ini + fin) // 2
            act = self.postres[med].nombre.strip().lower()
            if act == buscado:
                return med
            elif act < buscado:
                ini = med + 1
            else:
                fin = med - 1
        return -1

    def dar_de_alta_postre(self, nombre, lista_ing=None, lista_pasos=None, persistir=True):
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            return False, "El nombre del postre no puede estar vacío."

        idx = self.buscar_indice(nombre_limpio)
        if idx != -1:
            postre_existente = self.postres[idx]
            nuevos_ing = 0
            nuevos_pasos = 0
            if lista_ing:
                for ing in lista_ing:
                    if postre_existente.ingredientes.insertar(ing)[0]:
                        nuevos_ing += 1
            if lista_pasos:
                for paso in lista_pasos:
                    if postre_existente.pasos.insertar(paso)[0]:
                        nuevos_pasos += 1
            if persistir:
                self.guardar_en_disco()
            return True, f"'{nombre_limpio}' ya existía: Se fusionaron {nuevos_ing} ingrediente(s) y {nuevos_pasos} paso(s) sin duplicar."

        nuevo = Postre(nombre_limpio)
        if lista_ing:
            for item in lista_ing:
                nuevo.ingredientes.insertar(item)
        if lista_pasos:
            for item in lista_pasos:
                nuevo.pasos.insertar(item)

        pos = 0
        while pos < len(self.postres) and self.postres[pos].nombre.lower() < nuevo.nombre.lower():
            pos += 1
        self.postres.insert(pos, nuevo)

        if persistir:
            self.guardar_en_disco()
        return True, f"Postre '{nombre_limpio}' registrado en posición {pos}."

    def dar_de_baja_postre(self, nombre):
        idx = self.buscar_indice(nombre)
        if idx == -1:
            return False, f"El postre '{nombre}' no existe."
        eliminado = self.postres.pop(idx)
        eliminado.ingredientes.cabeza = None
        eliminado.pasos.cabeza = None
        self.guardar_en_disco()
        return True, f"Postre '{nombre}' eliminado correctamente."

    def renombrar_postre(self, nombre_actual, nombre_nuevo):
        nombre_nuevo = nombre_nuevo.strip()
        if not nombre_nuevo:
            return False, "El nuevo nombre no puede estar vacío."
        if nombre_actual.lower() == nombre_nuevo.lower():
            return True, "No hubo cambios."

        if self.buscar_indice(nombre_nuevo) != -1:
            return False, f"Ya existe un postre llamado '{nombre_nuevo}'."

        idx = self.buscar_indice(nombre_actual)
        if idx == -1:
            return False, "Postre no encontrado."

        postre = self.postres.pop(idx)
        postre.nombre = nombre_nuevo

        pos = 0
        while pos < len(self.postres) and self.postres[pos].nombre.lower() < postre.nombre.lower():
            pos += 1
        self.postres.insert(pos, postre)
        self.guardar_en_disco()
        return True, f"Renombrado a '{nombre_nuevo}' con éxito."


# ========================================================
# 3. Interfaz Gráfica
# ========================================================

BG_MAIN = "#F8FAFC"
BG_CARD = "#FFFFFF"
BG_HEADER = "#0F172A"
PRIMARY = "#2563EB"
SUCCESS = "#059669"
DANGER = "#DC2626"
TEXT_MAIN = "#1E293B"
TEXT_MUTED = "#64748B"
BORDER = "#CBD5E1"


class BotonPlano(tk.Button):
    def __init__(self, master, text="", command=None, bg=PRIMARY, fg="#FFFFFF", **kwargs):
        self.default_bg = bg
        self.hover_bg = self._calcular_hover(bg)
        super().__init__(
            master,
            text=text,
            command=command,
            font=("Segoe UI", 9, "bold"),
            bg=self.default_bg,
            fg=fg,
            activebackground=self.hover_bg,
            activeforeground=fg,
            relief="flat",
            bd=0,
            padx=12,
            pady=7,
            cursor="hand2",
            **kwargs
        )
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self.default_bg))

    @staticmethod
    def _calcular_hover(hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"#{int(r*0.85):02x}{int(g*0.85):02x}{int(b*0.85):02x}"


class AppPostresFinal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control de Postres")
        self.geometry("1040x680")
        self.minsize(960, 600)
        self.configure(bg=BG_MAIN)

        self.sistema = SistemaRecetario()
        self._configurar_estilos()
        self._crear_interfaz()
        self._refrescar_lista_postres()

    def _centrar_ventana(self, modal, ancho, alto):
        self.update_idletasks()
        modal.update_idletasks()
        x_padre = self.winfo_x()
        y_padre = self.winfo_y()
        w_padre = self.winfo_width()
        h_padre = self.winfo_height()

        x = x_padre + (w_padre // 2) - (ancho // 2)
        y = y_padre + (h_padre // 2) - (alto // 2)
        modal.geometry(f"{ancho}x{alto}+{max(10, x)}+{max(10, y)}")

    def _configurar_estilos(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=BG_CARD, borderwidth=0)
        style.configure("TNotebook.Tab",
                        font=("Segoe UI", 10, "bold"),
                        padding=[16, 7],
                        background=BG_MAIN,
                        foreground=TEXT_MUTED,
                        borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", BG_CARD)],
                  foreground=[("selected", PRIMARY)])

    def _crear_logo_circular(self, parent):
        canvas = tk.Canvas(parent, width=44, height=44, bg=BG_HEADER, highlightthickness=0, bd=0)
        canvas.create_oval(3, 3, 41, 41, fill="#EC4899", outline="#F472B6", width=2)
        canvas.create_text(22, 22, text="🧁", font=("Segoe UI Emoji", 18))
        return canvas

    def _crear_interfaz(self):
        header = tk.Frame(self, bg=BG_HEADER, height=65)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        brand_frame = tk.Frame(header, bg=BG_HEADER)
        brand_frame.pack(side=tk.LEFT, padx=18, pady=10)

        logo_canvas = self._crear_logo_circular(brand_frame)
        logo_canvas.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(brand_frame, text="Control de Postres",
                 font=("Segoe UI", 15, "bold"), bg=BG_HEADER, fg="#FFFFFF").pack(side=tk.LEFT)

        BotonPlano(header, text="➕ Dar de Alta Postre", bg=SUCCESS, command=self._modal_alta_postre).pack(side=tk.RIGHT, padx=15)
        BotonPlano(header, text="📄 Exportar Receta (.txt)", bg="#475569", command=self._exportar_receta).pack(side=tk.RIGHT, padx=5)

        area_central = tk.Frame(self, bg=BG_MAIN, padx=18, pady=15)
        area_central.pack(fill=tk.BOTH, expand=True)

        # Panel Izquierdo: POSTRES
        panel_izq = tk.Frame(area_central, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER, padx=14, pady=14)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, ipadx=5)

        tk.Label(panel_izq, text="POSTRES (Arreglo Ordenado)", font=("Segoe UI", 11, "bold"), bg=BG_CARD, fg=TEXT_MAIN).pack(anchor=tk.W)
        tk.Label(panel_izq, text="🔍 Búsqueda rápida:", font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_MUTED).pack(anchor=tk.W, pady=(5, 2))

        self.txt_filtro = tk.Entry(panel_izq, font=("Segoe UI", 10), bg=BG_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER)
        self.txt_filtro.pack(fill=tk.X, ipady=4, pady=(0, 10))
        self.txt_filtro.bind("<KeyRelease>", self._filtrar_postres)

        frame_list_postres = tk.Frame(panel_izq, bg=BG_CARD)
        frame_list_postres.pack(fill=tk.BOTH, expand=True)

        scroll_postres = tk.Scrollbar(frame_list_postres)
        scroll_postres.pack(side=tk.RIGHT, fill=tk.Y)

        self.list_postres = tk.Listbox(
            frame_list_postres,
            font=("Segoe UI", 10),
            bg=BG_MAIN,
            fg=TEXT_MAIN,
            selectbackground=PRIMARY,
            selectforeground="#FFFFFF",
            relief="flat",
            bd=0,
            activestyle="none",
            highlightthickness=1,
            highlightbackground=BORDER,
            yscrollcommand=scroll_postres.set,
            exportselection=False,
            width=26
        )
        self.list_postres.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_postres.config(command=self.list_postres.yview)
        self.list_postres.bind("<<ListboxSelect>>", self._al_seleccionar_postre)

        frame_acciones_postre = tk.Frame(panel_izq, bg=BG_CARD)
        frame_acciones_postre.pack(fill=tk.X, pady=(10, 0))

        BotonPlano(frame_acciones_postre, text="✏ Renombrar", bg="#64748B", command=self._renombrar_postre_dialog).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        BotonPlano(frame_acciones_postre, text="🗑 Dar de Baja", bg=DANGER, command=self._baja_postre).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        # Panel Derecho: Listas Enlazadas
        panel_der = tk.Frame(area_central, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER, padx=18, pady=14)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))

        frame_encabezado = tk.Frame(panel_der, bg=BG_CARD)
        frame_encabezado.pack(fill=tk.X, pady=(0, 8))

        self.lbl_titulo_postre = tk.Label(frame_encabezado, text="Selecciona un postre", font=("Segoe UI", 13, "bold"), bg=BG_CARD, fg=TEXT_MAIN)
        self.lbl_titulo_postre.pack(side=tk.LEFT)

        self.lbl_metricas = tk.Label(frame_encabezado, text="", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=PRIMARY)
        self.lbl_metricas.pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(panel_der)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_ingredientes = tk.Frame(self.notebook, bg=BG_CARD, padx=10, pady=10)
        self.notebook.add(self.tab_ingredientes, text="  Ingredientes (Lista Enlazada)  ")
        self._construir_panel_pestana(self.tab_ingredientes, "ingrediente")

        self.tab_pasos = tk.Frame(self.notebook, bg=BG_CARD, padx=10, pady=10)
        self.notebook.add(self.tab_pasos, text="  Pasos de Preparación (Lista Enlazada)  ")
        self._construir_panel_pestana(self.tab_pasos, "paso")

        self.barra_estado = tk.Label(self, text="Sistema listo. Guardado automático activo en recetario_postres.json",
                                     font=("Segoe UI", 9), bg="#E2E8F0", fg=TEXT_MUTED, anchor=tk.W, padx=15, pady=4)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

    def _construir_panel_pestana(self, contenedor, tipo):
        frame_list = tk.Frame(contenedor, bg=BG_CARD)
        frame_list.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        scroll = tk.Scrollbar(frame_list)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        lb = tk.Listbox(
            frame_list,
            font=("Segoe UI", 10),
            bg=BG_MAIN,
            fg=TEXT_MAIN,
            selectbackground=PRIMARY,
            selectforeground="#FFFFFF",
            relief="flat",
            bd=0,
            activestyle="none",
            highlightthickness=1,
            highlightbackground=BORDER,
            yscrollcommand=scroll.set,
            exportselection=False
        )
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=lb.yview)

        frame_btns = tk.Frame(contenedor, bg=BG_CARD)
        frame_btns.pack(fill=tk.X)

        if tipo == "ingrediente":
            self.list_ingredientes = lb
            self.list_ingredientes.bind("<Double-Button-1>", lambda e: self._modal_modificar_ingrediente())
            BotonPlano(frame_btns, text="➕ Agregar Ingrediente", bg=PRIMARY, command=self._modal_agregar_ingrediente).pack(side=tk.LEFT, padx=(0, 4))
            BotonPlano(frame_btns, text="✏ Modificar Seleccionado", bg="#64748B", command=self._modal_modificar_ingrediente).pack(side=tk.LEFT, padx=4)
            BotonPlano(frame_btns, text="🗑 Eliminar Seleccionado", bg=DANGER, command=self._eliminar_ingrediente).pack(side=tk.LEFT, padx=4)
        else:
            self.list_pasos = lb
            self.list_pasos.bind("<Double-Button-1>", lambda e: self._modal_modificar_paso())
            BotonPlano(frame_btns, text="➕ Agregar Paso", bg=PRIMARY, command=self._modal_agregar_paso).pack(side=tk.LEFT, padx=(0, 4))
            BotonPlano(frame_btns, text="✏ Modificar Seleccionado", bg="#64748B", command=self._modal_modificar_paso).pack(side=tk.LEFT, padx=4)
            BotonPlano(frame_btns, text="🗑 Eliminar Seleccionado", bg=DANGER, command=self._eliminar_paso).pack(side=tk.LEFT, padx=4)

    # ================= Control de Datos y Persistencia =================

    def _obtener_postre_actual(self):
        sel = self.list_postres.curselection()
        if not sel:
            return None
        nombre = self.list_postres.get(sel[0])
        idx = self.sistema.buscar_indice(nombre)
        return self.sistema.postres[idx] if idx != -1 else None

    def _refrescar_lista_postres(self, sel_nombre=None):
        self.list_postres.delete(0, tk.END)
        idx_destino = 0
        for i, p in enumerate(self.sistema.postres):
            self.list_postres.insert(tk.END, p.nombre)
            if sel_nombre and p.nombre.lower() == sel_nombre.lower():
                idx_destino = i

        if self.sistema.postres:
            self.list_postres.selection_set(idx_destino)
            self._al_seleccionar_postre(None)
        else:
            self.lbl_titulo_postre.config(text="No hay postres registrados")
            self.lbl_metricas.config(text="")
            self.list_ingredientes.delete(0, tk.END)
            self.list_pasos.delete(0, tk.END)

    def _al_seleccionar_postre(self, event):
        postre = self._obtener_postre_actual()
        if not postre:
            return

        self.lbl_titulo_postre.config(text=f"Postre: {postre.nombre}")

        self.list_ingredientes.delete(0, tk.END)
        for ing in postre.ingredientes.obtener_todos():
            self.list_ingredientes.insert(tk.END, f"• {ing}")

        self.list_pasos.delete(0, tk.END)
        for i, paso in enumerate(postre.pasos.obtener_todos(), 1):
            self.list_pasos.insert(tk.END, f"{i}. {paso}")

        n_ing = postre.ingredientes.cantidad()
        n_pasos = postre.pasos.cantidad()
        self.lbl_metricas.config(text=f"{n_ing} ingrediente(s) | {n_pasos} paso(s)")
        self.barra_estado.config(text=f"Postre '{postre.nombre}' cargado. Total de postres guardados: {len(self.sistema.postres)}")

    def _filtrar_postres(self, event):
        patron = self.txt_filtro.get().strip().lower()
        self.list_postres.delete(0, tk.END)
        for p in self.sistema.postres:
            if patron in p.nombre.lower():
                self.list_postres.insert(tk.END, p.nombre)

        if self.list_postres.size() > 0:
            self.list_postres.selection_set(0)
            self._al_seleccionar_postre(None)

    # ================= Modales: Ingredientes =================

    def _modal_agregar_ingrediente(self):
        postre = self._obtener_postre_actual()
        if not postre:
            messagebox.showwarning("Atención", "Selecciona un postre de la lista primero.")
            return

        self._dialogo_entrada(
            titulo="Agregar Nuevo Ingrediente",
            etiqueta=f"Ingrediente para '{postre.nombre}':",
            valor_inicial="",
            callback_guardar=lambda nuevo: self._accion_agregar_ing(postre, nuevo)
        )

    def _accion_agregar_ing(self, postre, nuevo):
        exito, msg = postre.ingredientes.insertar(nuevo)
        if exito:
            self.sistema.guardar_en_disco()
            self._al_seleccionar_postre(None)
            self.barra_estado.config(text=msg)
            return True
        messagebox.showinfo("Duplicado Evitado", msg)
        return False

    def _modal_modificar_ingrediente(self):
        postre = self._obtener_postre_actual()
        if not postre:
            messagebox.showwarning("Atención", "Selecciona un postre primero.")
            return

        sel = self.list_ingredientes.curselection()
        if not sel:
            messagebox.showinfo("Información", "Por favor selecciona un ingrediente de la lista para modificar.")
            return

        item_completo = self.list_ingredientes.get(sel[0])
        item_viejo = item_completo.replace("•", "").strip()

        self._dialogo_entrada(
            titulo="Modificar Ingrediente",
            etiqueta=f"Editar ingrediente de '{postre.nombre}':",
            valor_inicial=item_viejo,
            callback_guardar=lambda nuevo: self._accion_modificar_ing(postre, item_viejo, nuevo)
        )

    def _accion_modificar_ing(self, postre, viejo, nuevo):
        exito, msg = postre.ingredientes.modificar(viejo, nuevo)
        if exito:
            self.sistema.guardar_en_disco()
            self._al_seleccionar_postre(None)
            self.barra_estado.config(text=f"Ingrediente actualizado a '{nuevo}'.")
            return True
        messagebox.showwarning("Atención", msg)
        return False

    def _eliminar_ingrediente(self):
        postre = self._obtener_postre_actual()
        if not postre:
            return

        sel = self.list_ingredientes.curselection()
        if not sel:
            messagebox.showinfo("Información", "Por favor selecciona un ingrediente de la lista para eliminar.")
            return

        item = self.list_ingredientes.get(sel[0]).replace("•", "").strip()
        if messagebox.askyesno("Confirmar Eliminación", f"¿Eliminar el ingrediente '{item}' de la lista?"):
            exito, msg = postre.ingredientes.eliminar(item)
            if exito:
                self.sistema.guardar_en_disco()
                self._al_seleccionar_postre(None)
                self.barra_estado.config(text=msg)

    # ================= Modales: Pasos =================

    def _modal_agregar_paso(self):
        postre = self._obtener_postre_actual()
        if not postre:
            messagebox.showwarning("Atención", "Selecciona un postre de la lista primero.")
            return

        self._dialogo_entrada(
            titulo="Agregar Paso de Preparación",
            etiqueta=f"Nuevo paso para '{postre.nombre}':",
            valor_inicial="",
            es_multilinea=True,
            callback_guardar=lambda nuevo: self._accion_agregar_paso(postre, nuevo)
        )

    def _accion_agregar_paso(self, postre, nuevo):
        exito, msg = postre.pasos.insertar(nuevo)
        if exito:
            self.sistema.guardar_en_disco()
            self._al_seleccionar_postre(None)
            self.barra_estado.config(text=msg)
            return True
        messagebox.showinfo("Duplicado Evitado", msg)
        return False

    def _modal_modificar_paso(self):
        postre = self._obtener_postre_actual()
        if not postre:
            messagebox.showwarning("Atención", "Selecciona un postre primero.")
            return

        sel = self.list_pasos.curselection()
        if not sel:
            messagebox.showinfo("Información", "Por favor selecciona un paso de la lista para modificar.")
            return

        texto_completo = self.list_pasos.get(sel[0])
        item_viejo = texto_completo.split(". ", 1)[-1].strip()

        self._dialogo_entrada(
            titulo="Modificar Paso",
            etiqueta=f"Editar paso de '{postre.nombre}':",
            valor_inicial=item_viejo,
            es_multilinea=True,
            callback_guardar=lambda nuevo: self._accion_modificar_paso(postre, item_viejo, nuevo)
        )

    def _accion_modificar_paso(self, postre, viejo, nuevo):
        exito, msg = postre.pasos.modificar(viejo, nuevo)
        if exito:
            self.sistema.guardar_en_disco()
            self._al_seleccionar_postre(None)
            self.barra_estado.config(text="Paso actualizado correctamente.")
            return True
        messagebox.showwarning("Atención", msg)
        return False

    def _eliminar_paso(self):
        postre = self._obtener_postre_actual()
        if not postre:
            return

        sel = self.list_pasos.curselection()
        if not sel:
            messagebox.showinfo("Información", "Por favor selecciona un paso de la lista para eliminar.")
            return

        item = self.list_pasos.get(sel[0]).split(". ", 1)[-1].strip()
        if messagebox.askyesno("Confirmar Eliminación", f"¿Eliminar el paso seleccionado?"):
            exito, msg = postre.pasos.eliminar(item)
            if exito:
                self.sistema.guardar_en_disco()
                self._al_seleccionar_postre(None)
                self.barra_estado.config(text=msg)

    # ================= Modales Genéricas y Acciones Globales =================

    def _dialogo_entrada(self, titulo, etiqueta, valor_inicial, callback_guardar, es_multilinea=False):
        modal = tk.Toplevel(self)
        modal.title(titulo)
        modal.configure(bg=BG_CARD)
        modal.transient(self)
        modal.grab_set()

        pnl = tk.Frame(modal, bg=BG_CARD, padx=22, pady=18)
        pnl.pack(fill=tk.BOTH, expand=True)

        tk.Label(pnl, text=etiqueta, font=("Segoe UI", 10, "bold"), bg=BG_CARD, fg=TEXT_MAIN).pack(anchor=tk.W, pady=(0, 6))

        if es_multilinea:
            frame_txt = tk.Frame(pnl, bg=BG_MAIN, highlightthickness=1, highlightbackground=BORDER)
            frame_txt.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            txt = tk.Text(frame_txt, height=4, font=("Segoe UI", 10), bg=BG_MAIN, relief="flat", bd=0)
            txt.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
            txt.insert("1.0", valor_inicial)
            txt.focus_set()
            
            def obtener_valor():
                return txt.get("1.0", tk.END).strip()
        else:
            entry = tk.Entry(pnl, font=("Segoe UI", 10), bg=BG_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER)
            entry.pack(fill=tk.X, ipady=6, pady=(0, 15))
            entry.insert(0, valor_inicial)
            entry.focus_set()

            def obtener_valor():
                return entry.get().strip()

        frame_btns = tk.Frame(pnl, bg=BG_CARD)
        frame_btns.pack(fill=tk.X)

        def guardar():
            val = obtener_valor()
            if not val:
                messagebox.showwarning("Campo Vacío", "Por favor ingresa un texto válido.", parent=modal)
                return
            if callback_guardar(val):
                modal.destroy()

        BotonPlano(frame_btns, text="Cancelar", bg="#94A3B8", command=modal.destroy).pack(side=tk.RIGHT, padx=(6, 0))
        BotonPlano(frame_btns, text="Guardar", bg=PRIMARY, command=guardar).pack(side=tk.RIGHT)

        modal.bind("<Escape>", lambda e: modal.destroy())
        if not es_multilinea:
            modal.bind("<Return>", lambda e: guardar())
        else:
            modal.bind("<Control-Return>", lambda e: guardar())

        alto = 220 if es_multilinea else 170
        self._centrar_ventana(modal, 440, alto)

    def _modal_alta_postre(self):
        modal = tk.Toplevel(self)
        modal.title("Dar de Alta un Postre")
        modal.configure(bg=BG_CARD)
        modal.transient(self)
        modal.grab_set()

        header_modal = tk.Frame(modal, bg=BG_HEADER, height=50)
        header_modal.pack(fill=tk.X)
        header_modal.pack_propagate(False)

        tk.Label(header_modal, text="🧁 Registrar Nuevo Postre", font=("Segoe UI", 11, "bold"),
                 bg=BG_HEADER, fg="#FFFFFF").pack(side=tk.LEFT, padx=15, pady=12)

        cuerpo = tk.Frame(modal, bg=BG_CARD, padx=20, pady=15)
        cuerpo.pack(fill=tk.BOTH, expand=True)

        tk.Label(cuerpo, text="Nombre del Postre *", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MAIN).pack(anchor=tk.W)
        entry_nom = tk.Entry(cuerpo, font=("Segoe UI", 10), bg=BG_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER)
        entry_nom.pack(fill=tk.X, ipady=6, pady=(4, 12))
        entry_nom.focus_set()

        tk.Label(cuerpo, text="Ingredientes (uno por línea o separados por coma):",
                 font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MAIN).pack(anchor=tk.W)
        
        frame_txt_ing = tk.Frame(cuerpo, bg=BG_MAIN, highlightthickness=1, highlightbackground=BORDER)
        frame_txt_ing.pack(fill=tk.X, pady=(4, 12))
        scroll_ing = tk.Scrollbar(frame_txt_ing)
        scroll_ing.pack(side=tk.RIGHT, fill=tk.Y)
        txt_ing = tk.Text(frame_txt_ing, height=4, font=("Segoe UI", 9), bg=BG_MAIN, relief="flat", bd=0, yscrollcommand=scroll_ing.set)
        txt_ing.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=4)
        scroll_ing.config(command=txt_ing.yview)

        tk.Label(cuerpo, text="Pasos de Preparación (uno por cada renglón):",
                 font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MAIN).pack(anchor=tk.W)
        
        frame_txt_pasos = tk.Frame(cuerpo, bg=BG_MAIN, highlightthickness=1, highlightbackground=BORDER)
        frame_txt_pasos.pack(fill=tk.X, pady=(4, 15))
        scroll_pasos = tk.Scrollbar(frame_txt_pasos)
        scroll_pasos.pack(side=tk.RIGHT, fill=tk.Y)
        txt_pasos = tk.Text(frame_txt_pasos, height=4, font=("Segoe UI", 9), bg=BG_MAIN, relief="flat", bd=0, yscrollcommand=scroll_pasos.set)
        txt_pasos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=4)
        scroll_pasos.config(command=txt_pasos.yview)

        frame_botones = tk.Frame(cuerpo, bg=BG_CARD)
        frame_botones.pack(fill=tk.X, pady=(5, 0))

        def guardar():
            nombre = entry_nom.get().strip()
            if not nombre:
                messagebox.showwarning("Campo Requerido", "Escribe el nombre del postre para continuar.", parent=modal)
                entry_nom.focus_set()
                return

            raw_ing = txt_ing.get("1.0", tk.END).replace("\n", ",").split(",")
            lista_ing = [i.strip() for i in raw_ing if i.strip()]

            raw_pasos = txt_pasos.get("1.0", tk.END).split("\n")
            lista_pasos = [p.strip() for p in raw_pasos if p.strip()]

            exito, msg = self.sistema.dar_de_alta_postre(nombre, lista_ing, lista_pasos)
            modal.destroy()
            self.txt_filtro.delete(0, tk.END)
            self._refrescar_lista_postres(nombre)
            self.barra_estado.config(text=msg)
            messagebox.showinfo("Registro", msg)

        BotonPlano(frame_botones, text="Cancelar", bg="#94A3B8", command=modal.destroy).pack(side=tk.RIGHT, padx=(6, 0))
        BotonPlano(frame_botones, text="Guardar Postre", bg=SUCCESS, command=guardar).pack(side=tk.RIGHT)

        modal.bind("<Escape>", lambda e: modal.destroy())
        modal.bind("<Control-Return>", lambda e: guardar())

        self._centrar_ventana(modal, 480, 520)

    def _baja_postre(self):
        postre = self._obtener_postre_actual()
        if not postre:
            messagebox.showwarning("Aviso", "Selecciona un postre para dar de baja.")
            return

        if messagebox.askyesno("Confirmar Baja", f"¿Eliminar definitivamente '{postre.nombre}' y sus listas de ingredientes y pasos?"):
            exito, msg = self.sistema.dar_de_baja_postre(postre.nombre)
            if exito:
                self.txt_filtro.delete(0, tk.END)
                self._refrescar_lista_postres()
                self.barra_estado.config(text=msg)

    def _renombrar_postre_dialog(self):
        postre = self._obtener_postre_actual()
        if not postre:
            messagebox.showwarning("Aviso", "Selecciona un postre para renombrar.")
            return

        self._dialogo_entrada(
            titulo="Renombrar Postre",
            etiqueta=f"Nuevo nombre para '{postre.nombre}':",
            valor_inicial=postre.nombre,
            callback_guardar=lambda nuevo: self._accion_renombrar(postre.nombre, nuevo)
        )

    def _accion_renombrar(self, viejo, nuevo):
        exito, msg = self.sistema.renombrar_postre(viejo, nuevo)
        if exito:
            self.txt_filtro.delete(0, tk.END)
            self._refrescar_lista_postres(nuevo)
            self.barra_estado.config(text=msg)
            return True
        messagebox.showwarning("Atención", msg)
        return False

    def _exportar_receta(self):
        postre = self._obtener_postre_actual()
        if not postre:
            messagebox.showwarning("Atención", "Selecciona un postre para exportar.")
            return

        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")],
            initialfile=f"Receta_{postre.nombre.replace(' ', '_')}.txt"
        )
        if not archivo:
            return

        try:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(f"==================================================\n")
                f.write(f"RECETA: {postre.nombre.upper()}\n")
                f.write(f"==================================================\n\n")
                
                f.write("[ INGREDIENTES ]\n")
                for ing in postre.ingredientes.obtener_todos():
                    f.write(f" • {ing}\n")
                
                f.write("\n[ PASOS DE PREPARACIÓN ]\n")
                for i, paso in enumerate(postre.pasos.obtener_todos(), 1):
                    f.write(f" {i}. {paso}\n")
                
                f.write(f"\n==================================================\n")
            
            messagebox.showinfo("Exportado", f"Receta exportada exitosamente a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))


if __name__ == "__main__":
    app = AppPostresFinal()
    app.mainloop()