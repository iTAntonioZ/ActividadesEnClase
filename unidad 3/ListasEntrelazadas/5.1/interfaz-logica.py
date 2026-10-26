"""Ejecuta python interfaz-logica.py. Requiere Python con Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox
from logica import ListaLigada


class Aplicacion(tk.Tk):
    MODOS = {
        'Insertar': {'Al inicio': 'inicio', 'Al final': 'final', 'En medio': 'medio', 'Antes de X': 'antes', 'Después de X': 'despues', 'En una posición': 'posicion'},
        'Eliminar': {'El primero': 'inicio', 'El último': 'final', 'El de en medio': 'medio', 'El dato X': 'valor', 'El anterior a X': 'antes', 'El posterior a X': 'despues', 'Omitir el siguiente de X (reconectar)': 'reconectar', 'En una posición': 'posicion'},
        'Buscar': {'Desordenada (secuencial)': 'desordenada', 'Ordenada (con corte temprano)': 'ordenada', 'Recursiva': 'recursiva'},
        'Recorrer': {'Iterativo': 'iterativo', 'Recursivo': 'recursivo', 'Inverso (recursivo)': 'inverso'},
    }

    def __init__(self):
        super().__init__()
        self.title('Laboratorio de listas simplemente ligadas')
        self.state('normal')
        self.attributes('-fullscreen', False)
        self.resizable(True, True)
        pantalla_w, pantalla_h = self.winfo_screenwidth(), self.winfo_screenheight()
        ancho = min(1080, int(pantalla_w * 0.85))
        alto = min(780, int(pantalla_h * 0.82))
        self.geometry(f'{ancho}x{alto}+{max(0, (pantalla_w-ancho)//2)}+{max(30, (pantalla_h-alto)//2)}')
        self.configure(bg='#edf2f7')
        self.minsize(min(680, ancho), min(460, alto))
        self.lista = ListaLigada()
        self.antes, self.despues = [], []
        self.marca_antes, self.marca_despues = {}, {}
        self.pasos, self.paso, self.timer = [], 0, None
        self.final_texto = ''
        estilo = ttk.Style(self)
        estilo.theme_use('clam')
        estilo.configure('TFrame', background='#f1f5f9')
        estilo.configure('TLabel', background='#f1f5f9', foreground='#0f172a', font=('Segoe UI', 10))
        estilo.configure('TButton', padding=(14, 9), font=('Segoe UI', 10), background='#ffffff', borderwidth=0)
        estilo.map('TButton', background=[('active', '#e0e7ff')], foreground=[('disabled', '#94a3b8')])
        estilo.configure('Primary.TButton', background='#4f46e5', foreground='white', font=('Segoe UI', 10, 'bold'))
        estilo.map('Primary.TButton', background=[('active', '#4338ca')], foreground=[('active', 'white')])
        estilo.configure('TEntry', padding=9, bordercolor='#cbd5e1', lightcolor='#cbd5e1', fieldbackground='white')
        estilo.map('TEntry', fieldbackground=[('disabled', '#e2e8f0')])
        estilo.configure('TCombobox', padding=8, bordercolor='#cbd5e1', arrowcolor='#4f46e5')
        estilo.configure('TNotebook', background='#f1f5f9', borderwidth=0)
        estilo.configure('TNotebook.Tab', padding=(24, 11), background='#e2e8f0', font=('Segoe UI', 10, 'bold'))
        estilo.map('TNotebook.Tab', background=[('selected', '#4f46e5')], foreground=[('selected', 'white')])
        estilo.configure('Badge.TLabel', padding=(12, 8), background='#e0e7ff', foreground='#4338ca', font=('Segoe UI', 10, 'bold'))
        estilo.configure('Title.TLabel', font=('Segoe UI', 22, 'bold'))
        # La barra nativa de Windows ofrece minimizar, maximizar y cerrar.
        self.overrideredirect(False)
        self.bind('<F11>', self.alternar_maximizado)
        self.bind('<Escape>', self.restaurar_ventana)
        self.bind('<Configure>', self.actualizar_boton_ventana)
        contenedor = ttk.Frame(self)
        contenedor.pack(fill='both', expand=True)
        self.pagina = tk.Canvas(contenedor, bg='#f1f5f9', highlightthickness=0)
        scroll_vertical = ttk.Scrollbar(contenedor, orient='vertical', command=self.pagina.yview)
        scroll_vertical.pack(side='right', fill='y')
        self.pagina.pack(side='left', fill='both', expand=True)
        self.pagina.configure(yscrollcommand=scroll_vertical.set)
        p = ttk.Frame(self.pagina, padding=16)
        self.contenido_id = self.pagina.create_window((0, 0), window=p, anchor='nw')
        p.bind('<Configure>', lambda e: self.pagina.configure(scrollregion=self.pagina.bbox('all')))
        self.pagina.bind('<Configure>', lambda e: self.pagina.itemconfigure(self.contenido_id, width=max(e.width, 820)))
        scroll_horizontal = ttk.Scrollbar(self, orient='horizontal', command=self.pagina.xview)
        scroll_horizontal.pack(fill='x')
        self.pagina.configure(xscrollcommand=scroll_horizontal.set)
        cabecera = tk.Frame(p, bg='#172554', padx=20, pady=16)
        cabecera.pack(fill='x', pady=(0, 8))
        tk.Label(cabecera, text='ESTRUCTURAS DE DATOS  /  LISTA SIMPLEMENTE LIGADA', bg='#172554', fg='#a5b4fc', font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        tk.Label(cabecera, text='Laboratorio de listas', bg='#172554', fg='white', font=('Segoe UI', 23, 'bold')).pack(anchor='w', pady=(3, 0))
        ttk.Label(p, text='1. Elige una operación   →   2. Completa los datos   →   3. Observa los enlaces').pack(anchor='w', pady=(3, 12))
        herramientas = ttk.Frame(p)
        herramientas.pack(fill='x')
        ttk.Button(p, text='Editar conexiones entre nodos ↗', command=self.editor_conexiones, style='Primary.TButton').pack(anchor='w', pady=6)
        ttk.Button(herramientas, text='Cargar ejemplo: 10 → 20 → 30 → 40', command=self.ejemplo).pack(side='left')
        ttk.Button(herramientas, text='Ordenar ascendente', command=self.ordenar).pack(side='left', padx=8)
        ttk.Button(herramientas, text='Vaciar lista', command=self.vaciar).pack(side='left')
        self.contador = ttk.Label(herramientas, style='Badge.TLabel')
        self.contador.pack(side='right')
        self.tabs = ttk.Notebook(p)
        self.tabs.pack(fill='x', pady=14)
        for nombre in self.MODOS:
            self.tabs.add(ttk.Frame(self.tabs), text=nombre, padding=10)
        self.tabs.bind('<<NotebookTabChanged>>', self.cambiar_operacion)
        formulario = ttk.Frame(p)
        formulario.pack(fill='x')
        ttk.Label(formulario, text='Modalidad').grid(row=0, column=0, sticky='w')
        self.selector = ttk.Combobox(formulario, state='readonly', width=34)
        self.selector.grid(row=1, column=0, padx=(0, 16), pady=5)
        self.selector.bind('<<ComboboxSelected>>', self.actualizar_campos)
        self.et_dato = ttk.Label(formulario, text='Dato')
        self.et_dato.grid(row=0, column=1, sticky='w')
        self.dato = ttk.Entry(formulario, width=24)
        self.dato.grid(row=1, column=1, padx=(0, 16))
        self.et_ref = ttk.Label(formulario, text='Referencia')
        self.et_ref.grid(row=0, column=2, sticky='w')
        self.ref = ttk.Entry(formulario, width=24)
        self.ref.grid(row=1, column=2)
        self.ayuda = ttk.Label(p, wraplength=980)
        self.ayuda.pack(anchor='w', pady=8)
        acciones = ttk.Frame(p)
        acciones.pack(fill='x', pady=(0, 12))
        self.boton = ttk.Button(acciones, text='Insertar', command=self.ejecutar, style='Primary.TButton')
        self.boton.pack(side='left')
        self.siguiente = ttk.Button(acciones, text='Siguiente paso', command=self.avanzar)
        self.siguiente.pack(side='left', padx=8)
        self.auto = ttk.Button(acciones, text='Reproducir', command=self.reproducir)
        self.auto.pack(side='left')
        ttk.Button(acciones, text='Pausar', command=self.pausar).pack(side='left', padx=8)
        marco_grafo = ttk.Frame(p)
        marco_grafo.pack(fill='both', expand=True)
        self.canvas = tk.Canvas(marco_grafo, bg='white', highlightthickness=1, highlightbackground='#dbe3ef', height=310)
        vertical_grafo = ttk.Scrollbar(marco_grafo, orient='vertical', command=self.canvas.yview)
        vertical_grafo.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.configure(yscrollcommand=vertical_grafo.set)
        barra = ttk.Scrollbar(p, orient='horizontal', command=self.canvas.xview)
        barra.pack(fill='x')
        self.canvas.configure(xscrollcommand=barra.set)
        self.canvas.bind('<Configure>', lambda e: self.dibujar() if hasattr(self, 'estado') else None)
        ttk.Label(p, text='Verde: insertado / encontrado / reconectado    Rojo: eliminado    Amarillo: visita actual    Azul: visitado').pack(anchor='w', pady=8)
        self.estado = ttk.Label(p, text='Empieza insertando un dato o carga el ejemplo.', wraplength=980)
        self.estado.pack(anchor='w')
        self.salida = tk.Text(p, height=3, wrap='word', font=('Segoe UI', 10), relief='flat', bg='#e0e7ff', fg='#312e81', padx=12, pady=8, state='disabled')
        self.salida.pack(fill='x', pady=(8, 0))
        self.bind('<Return>', lambda e: self.ejecutar())
        self.protocol('WM_DELETE_WINDOW', self.cerrar)
        self.cambiar_operacion()
        self.dibujar()

    def alternar_maximizado(self, evento=None):
        self.state('normal' if self.state() == 'zoomed' else 'zoomed')
        self.actualizar_boton_ventana()
        return 'break'

    def restaurar_ventana(self, evento=None):
        self.attributes('-fullscreen', False)
        self.state('normal')
        self.actualizar_boton_ventana()

    def actualizar_boton_ventana(self, evento=None):
        if hasattr(self, 'boton_maximizar'):
            self.boton_maximizar.configure(text='Restaurar ❐' if self.state() == 'zoomed' else 'Maximizar □')

    def editor_conexiones(self):
        self.cancelar()
        ventana = tk.Toplevel(self)
        ventana.title('Conexiones interactivas · selecciona origen y destino')
        ventana.geometry('900x650')
        ventana.minsize(650, 480)
        ventana.transient(self)
        ventana.grab_set()
        panel = ttk.Frame(ventana, padding=16)
        panel.pack(fill='both', expand=True)
        ttk.Label(panel, text='Conecta tus nodos', style='Title.TLabel').pack(anchor='w')
        ttk.Label(panel, text='1. Haz clic en el origen.  2. Haz clic en el destino o pulsa Apuntar a NULL.', wraplength=820).pack(anchor='w', pady=8)
        fila = ttk.Frame(panel)
        fila.pack(fill='x')
        entrada = ttk.Entry(fila, width=18)
        entrada.pack(side='left')
        seleccionado = [None]
        estado = ttk.Label(panel, text='Selecciona un origen. Cada nodo tiene una sola salida y puede recibir varias entradas.', wraplength=820)
        area = tk.Canvas(panel, bg='white', highlightthickness=0)
        barra = ttk.Scrollbar(panel, orient='vertical', command=area.yview)
        posiciones = {}
        def sincronizar():
            self.despues = self.lista.valores()
            self.marca_antes, self.marca_despues = {}, {}
            self.actualizar_campos()
            self.dibujar()
        def dibujar():
            area.delete('all')
            posiciones.clear()
            for i, nodo in enumerate(self.lista.nodos):
                posiciones[nodo] = (120 + (i % 3) * 260, 80 + (i // 3) * 150)
            for i, nodo in enumerate(self.lista.nodos):
                x, y = posiciones[nodo]
                if nodo.liga is not None:
                    dx, dy = posiciones[nodo.liga]
                    area.create_line(x+55, y, x+95, y-55, dx-95, dy-55, dx-55, dy, smooth=True, arrow='last', width=2, fill='#6366f1')
                else:
                    area.create_line(x+55, y, x+85, y, arrow='last', fill='#94a3b8')
                    area.create_text(x+107, y, text='NULL', fill='#64748b')
            for i, nodo in enumerate(self.lista.nodos):
                x, y = posiciones[nodo]
                tag = f'nodo{i}'
                color = '#fde68a' if nodo is seleccionado[0] else '#e0e7ff'
                area.create_rectangle(x-55,y-23,x+55,y+23,fill=color,outline='#6366f1',width=2,tags=tag)
                valor = str(nodo.info)
                area.create_text(x,y,text=valor if len(valor)<=12 else valor[:11]+'…',font=('Segoe UI',11,'bold'),tags=tag)
                entradas = sum(n.liga is nodo for n in self.lista.nodos)
                etiqueta = f'N{i+1} · {entradas} entrada(s)' + (' · INICIO' if nodo is self.lista.inicio else '')
                area.create_text(x,y+38,text=etiqueta,fill='#475569',tags=tag)
                area.tag_bind(tag,'<Button-1>',lambda e,n=nodo: elegir(n))
            area.configure(scrollregion=(0,0,840,max(360,((len(self.lista.nodos)+2)//3)*150+60)))
        def conectar(destino):
            origen = seleccionado[0]
            if origen is None:
                messagebox.showerror('Falta el origen','Selecciona primero el nodo que quieres conectar.',parent=ventana)
                return
            try:
                self.antes = self.lista.valores()
                self.lista.conectar(origen,destino)
            except ValueError as error:
                messagebox.showerror('Conexión inválida',str(error),parent=ventana)
                return
            estado.configure(text=f'{origen.info!r} ahora apunta a {repr(destino.info) if destino else "NULL"}. Los nodos desconectados permanecen visibles.')
            seleccionado[0] = None
            sincronizar()
            dibujar()
        def elegir(nodo):
            if seleccionado[0] is None:
                seleccionado[0] = nodo
                estado.configure(text=f'Origen: {nodo.info!r}. Selecciona el destino o pulsa Apuntar a NULL.')
                dibujar()
            else:
                conectar(nodo)
        def agregar():
            try:
                self.lista.agregar_suelto(entrada.get())
            except ValueError as error:
                messagebox.showerror('Dato vacío',str(error),parent=ventana)
                return
            entrada.delete(0,'end')
            sincronizar()
            dibujar()
        def cancelar():
            seleccionado[0] = None
            estado.configure(text='Selección cancelada. Elige un nuevo origen.')
            dibujar()
        ttk.Button(fila,text='Añadir nodo',command=agregar).pack(side='left',padx=6)
        ttk.Button(fila,text='Apuntar a NULL',command=lambda: conectar(None)).pack(side='left')
        ttk.Button(fila,text='Cancelar selección',command=cancelar).pack(side='left',padx=6)
        estado.pack(anchor='w',pady=12)
        barra.pack(side='right',fill='y')
        area.pack(fill='both',expand=True)
        area.configure(yscrollcommand=barra.set)
        horizontal = ttk.Scrollbar(panel,orient='horizontal',command=area.xview)
        horizontal.pack(fill='x')
        area.configure(xscrollcommand=horizontal.set)
        ttk.Label(panel,text='La vista principal muestra estas mismas conexiones. Los recorridos siguen los punteros desde INICIO hasta NULL.',wraplength=820).pack(anchor='w',pady=8)
        dibujar()

    def operacion(self):
        return self.tabs.tab(self.tabs.select(), 'text')

    def cambiar_operacion(self, evento=None):
        self.pausar()
        self.selector.configure(values=list(self.MODOS[self.operacion()]))
        self.selector.current(0)
        self.actualizar_campos()

    def actualizar_campos(self, evento=None):
        op = self.operacion()
        modo = self.MODOS[op][self.selector.get()]
        self.boton.configure(text=op if op in ('Insertar', 'Eliminar') else 'Preparar ' + op.lower())
        self.dato.configure(state='normal' if op in ('Insertar', 'Buscar') else 'disabled')
        self.et_dato.configure(text='Dato a buscar' if op == 'Buscar' else 'Dato nuevo')
        necesita = op in ('Insertar', 'Eliminar') and modo in ('antes', 'despues', 'valor', 'posicion', 'reconectar')
        self.ref.configure(state='normal' if necesita else 'disabled')
        self.et_ref.configure(text='Posición (desde 1)' if modo == 'posicion' else 'Dato X de referencia')
        texto = 'X usa la primera coincidencia. Los datos se conservan como texto; la búsqueda usa igualdad exacta.'
        if modo == 'medio':
            texto = ('Inserta después de n // 2 nodos; con 3 nodos ocupa la posición 2.' if op == 'Insertar' else 'Elimina el central. Si hay dos centrales, elimina el primero: con 4 nodos, la posición 2.')
        elif modo == 'posicion':
            texto = (f'Posición válida: 1 a {len(self.lista.valores()) + (op == "Insertar")}. No se admiten posiciones cero, negativas ni decimales.' if self.lista.valores() or op == 'Insertar' else 'La lista está vacía. Inserta un nodo antes de eliminar.')
        elif modo == 'reconectar':
            texto = 'X apunta al nodo que está dos lugares adelante y retira al intermedio. Ejemplo: 10 → 20 → 30 pasa a 10 → 30 con X = 10. Si el omitido es el último, X apunta a NIL.'
        elif modo == 'ordenada':
            texto = 'Requiere orden ascendente. Números por valor; después textos por orden Unicode. La validación previa recorre la lista.'
        elif op == 'Recorrer':
            texto = 'El recorrido inverso muestra los datos al regresar de la recursión; no invierte los enlaces.' if modo == 'inverso' else 'Prepara el recorrido y usa Siguiente paso o Reproducir para visitar los nodos.'
        self.ayuda.configure(text=texto)

    def pausar(self):
        if self.timer is not None:
            self.after_cancel(self.timer)
            self.timer = None

    def cancelar(self):
        self.pausar()
        self.pasos, self.paso = [], 0

    def salida_texto(self, texto):
        self.salida.configure(state='normal')
        self.salida.delete('1.0', 'end')
        self.salida.insert('1.0', texto)
        self.salida.configure(state='disabled')

    def ejecutar(self):
        op = self.operacion()
        modo = self.MODOS[op][self.selector.get()]
        dato, ref = self.dato.get().strip(), self.ref.get().strip()
        antes = self.lista.valores()
        campo_error = self.ref if modo in ('posicion', 'antes', 'despues', 'valor', 'reconectar') else self.dato
        try:
            posicion = None
            if modo == 'posicion':
                try:
                    posicion = int(ref)
                except ValueError:
                    raise ValueError(f'La posición {ref!r} no es un número entero.\nEscribe una posición como 1, 2 o 3.') from None
            if op in ('Insertar', 'Buscar') and not dato:
                campo_error = self.dato
                raise ValueError('Escribe el dato primero. El campo no puede quedar vacío.')
            if op in ('Insertar', 'Eliminar') and modo in ('antes', 'despues', 'valor', 'reconectar') and not ref:
                raise ValueError('Escribe el dato X de referencia.')
            if op == 'Insertar':
                indice = self.lista.insertar(dato, modo, ref, posicion)
            elif op == 'Eliminar':
                if modo == 'reconectar':
                    indice, eliminado = self.lista.omitir_siguiente(ref)
                else:
                    indice, eliminado = self.lista.eliminar(modo, ref, posicion)
            elif op == 'Buscar':
                encontrado, visitas = self.lista.buscar(dato, modo)
            else:
                recorrido = self.lista.recorrer(modo)
        except (ValueError, RecursionError) as error:
            self.pausar()
            mensaje = str(error) if not isinstance(error, RecursionError) else 'La lista supera el límite recursivo de Python. Usa el modo iterativo.'
            self.estado.configure(text='Operación cancelada. Corrige el campo indicado e inténtalo de nuevo.')
            messagebox.showerror('No se puede ' + op.lower(), mensaje + '\n\nLa lista no se modificó.', parent=self)
            if str(campo_error.cget('state')) != 'disabled':
                campo_error.focus_set()
                campo_error.selection_range(0, 'end')
            return
        self.cancelar()
        self.antes, self.despues = antes, self.lista.valores()
        self.marca_antes, self.marca_despues = {}, {}
        self.salida_texto('')
        if op == 'Insertar':
            self.marca_despues[indice] = '#bbf7d0'
            siguiente = repr(self.despues[indice + 1]) if indice + 1 < len(self.despues) else 'NIL'
            self.estado.configure(text=f'Insertado en posición {indice + 1}: el nuevo nodo apunta a {siguiente}; el anterior (o INICIO) apunta al nuevo.')
        elif op == 'Eliminar':
            self.marca_antes[indice] = '#fecaca'
            if modo == 'reconectar':
                self.marca_despues[indice - 1] = '#bbf7d0'
            self.estado.configure(text=f'Eliminado {eliminado!r} de la posición {indice + 1}. El anterior (o INICIO) apunta al siguiente; se desconecta el nodo eliminado.')
            if modo == 'reconectar':
                destino = repr(self.despues[indice]) if indice < len(self.despues) else 'NIL'
                self.estado.configure(text=f'Reconexión: {ref!r} ahora apunta a {destino}. Se omitió y retiró {eliminado!r}; los demás nodos conservan su orden.')
        else:
            self.encontrado = encontrado if op == 'Buscar' else None
            self.pasos = visitas if op == 'Buscar' else [i for i, _ in recorrido]
            self.final_texto = (f'Encontrado en posición {encontrado + 1}.' if encontrado is not None else 'Dato no encontrado.') if op == 'Buscar' else 'Recorrido terminado.'
            self.estado.configure(text='Usa Siguiente paso o Reproducir.' if self.pasos else self.final_texto + ' La lista está vacía.')
        self.actualizar_campos()
        self.canvas.xview_moveto(0)
        self.dibujar()

    def avanzar(self):
        if self.paso >= len(self.pasos):
            return
        self.marca_despues = {i: '#bfdbfe' for i in self.pasos[:self.paso]}
        indice = self.pasos[self.paso]
        self.marca_despues[indice] = '#fde68a'
        self.paso += 1
        fin = self.paso == len(self.pasos)
        if fin and self.encontrado is not None:
            self.marca_despues[self.encontrado] = '#bbf7d0'
        self.estado.configure(text=f'Paso {self.paso}/{len(self.pasos)}: posición {indice + 1}, dato {self.despues[indice]!r}. ' + (self.final_texto if fin else ''))
        self.salida_texto(' → '.join(self.despues[i] for i in self.pasos[:self.paso]))
        self.dibujar()
        nodo = self.lista.inicio
        for _ in range(indice):
            nodo = nodo.liga
        x, y = self.posiciones_principal[nodo]
        self.canvas.xview_moveto(max(0, (x - 180) / self.ancho_grafo))
        self.canvas.yview_moveto(max(0, (y - 120) / self.alto_grafo))

    def reproducir(self):
        self.pausar()
        self.avanzar()
        if self.paso < len(self.pasos):
            self.timer = self.after(700, self.reproducir)

    def cambio_general(self, accion, texto):
        self.cancelar()
        self.antes = self.lista.valores()
        accion()
        self.despues = self.lista.valores()
        self.marca_antes, self.marca_despues = {}, {}
        self.estado.configure(text=texto)
        self.salida_texto('')
        self.actualizar_campos()
        self.dibujar()

    def ejemplo(self):
        def cargar():
            self.lista.vaciar()
            for dato in ('10', '20', '30', '40'):
                self.lista.insertar(dato, 'final')
        self.cambio_general(cargar, 'Ejemplo cargado. Prueba eliminar el de en medio: se eliminará 20.')

    def ordenar(self):
        self.cambio_general(self.lista.ordenar, 'Lista ordenada ascendentemente. Números primero por valor; después textos por orden Unicode.')

    def vaciar(self):
        self.cambio_general(self.lista.vaciar, 'Lista vacía. INICIO apunta a NIL.')

    def dibujar(self):
        """Dibuja el registro completo y cada enlace real, sin aplanar la cadena."""
        c = self.canvas
        c.delete('all')
        nodos = self.lista.nodos
        cadena = []
        actual = self.lista.inicio
        while actual is not None and actual not in cadena:
            cadena.append(actual)
            actual = actual.liga
        ancho_visible = max(760, c.winfo_width())
        columnas = max(3, min(5, int(ancho_visible // 250)))
        paso_x, paso_y = 250, 155
        self.paso_x = paso_x
        posiciones = {n: (125 + (i % columnas) * paso_x, 110 + (i // columnas) * paso_y)
                      for i, n in enumerate(nodos)}
        self.posiciones_principal = posiciones
        indices = {n: i for i, n in enumerate(cadena)}
        c.create_text(20, 24, text='CONEXIONES ACTUALES · las flechas representan los punteros', anchor='w', fill='#475569', font=('Segoe UI', 11, 'bold'))
        colores = {n: self.marca_despues.get(i, '#eef2ff') for n, i in indices.items()}
        for n in nodos:
            x, y = posiciones[n]
            destino = n.liga
            if destino is None:
                c.create_line(x+52,y,x+77,y,arrow='last',fill='#94a3b8',width=2)
                c.create_text(x+99,y,text='NULL',fill='#64748b',font=('Segoe UI',9))
            elif destino in posiciones:
                dx, dy = posiciones[destino]
                resaltado = colores.get(n) in ('#bfdbfe', '#fde68a', '#bbf7d0')
                color = '#d97706' if resaltado else '#6366f1'
                # La curva sale del origen y la punta termina en el destino.
                if abs(dy-y) < 1:
                    c.create_line(x+52,y,x+85,y-55,dx-85,dy-55,dx-52,dy,
                                  smooth=True,arrow='last',width=3 if resaltado else 2,fill=color)
                else:
                    c.create_line(x,y+24,x+60,y+65,dx-60,dy-65,dx,dy-24,
                                  smooth=True,arrow='last',width=3 if resaltado else 2,fill=color)
        for i,n in enumerate(nodos):
            x,y = posiciones[n]
            color = colores.get(n, '#f1f5f9')
            c.create_rectangle(x-52,y-24,x+52,y+24,fill=color,outline='#6366f1',width=2)
            valor = str(n.info)
            c.create_text(x,y,text=valor if len(valor)<=12 else valor[:11]+'…',font=('Segoe UI',11,'bold'))
            etiqueta = f'N{i+1}'
            if n is self.lista.inicio:
                etiqueta += ' · INICIO'
            elif n not in indices:
                etiqueta += ' · fuera del recorrido'
            c.create_text(x,y+42,text=etiqueta,fill='#64748b',font=('Segoe UI',9))
        if not nodos:
            c.create_text(30,100,text='INICIO → NULL   ·   Inserta un nodo para comenzar.',anchor='w',fill='#64748b')
        filas = (len(nodos)+columnas-1)//columnas
        self.alto_grafo = max(300,filas*paso_y+80)
        self.ancho_grafo = max(760,columnas*paso_x+30)
        c.configure(scrollregion=(0,0,self.ancho_grafo,self.alto_grafo))
        self.contador.configure(text=f'{len(cadena)} en recorrido / {len(nodos)} total')
        estado = 'normal' if self.paso < len(self.pasos) else 'disabled'
        self.siguiente.configure(state=estado)
        self.auto.configure(state=estado)

    def cerrar(self):
        self.pausar()
        self.destroy()


if __name__ == '__main__':
    Aplicacion().mainloop()
