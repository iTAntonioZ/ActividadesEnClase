import tkinter as tk
from tkinter import ttk, messagebox
from logica import ArbolBinario

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Laboratorio de árboles binarios')
        self.geometry(f'{min(1050,int(self.winfo_screenwidth()*.85))}x{min(740,int(self.winfo_screenheight()*.8))}+40+40')
        self.arbol = ArbolBinario()
        self.pos = {}; self.seleccion = None; self.origen = None
        self.pasos = []; self.visitas = []; self.timer = None
        self.configure(bg='#eef2ff')
        tk.Label(self,text='Árbol binario · laboratorio visual',bg='#172554',fg='white',font=('Segoe UI',20,'bold'),pady=16).pack(fill='x')
        barra = ttk.Frame(self,padding=10); barra.pack(fill='x')
        self.dato = ttk.Entry(barra,width=15); self.dato.pack(side='left')
        self.lado = ttk.Combobox(barra,values=['izquierdo','derecho'],state='readonly',width=11); self.lado.set('izquierdo'); self.lado.pack(side='left',padx=5)
        for texto,fn in [('Agregar',self.agregar),('Eliminar subárbol',self.eliminar),('Mover subárbol',self.mover),('Ordenar dibujo',self.distribuir)]:
            ttk.Button(barra,text=texto,command=fn).pack(side='left',padx=3)
        ttk.Button(self,text='Cargar ejemplo A–G',command=self.ejemplo).pack(anchor='w',padx=10)
        self.estadisticas=ttk.Label(self,padding=8,wraplength=950); self.estadisticas.pack(fill='x')
        self.estado = ttk.Label(self,text='Escribe un dato para crear la raíz. Después selecciona un padre y el lado.',padding=10,wraplength=900); self.estado.pack(fill='x')
        marco = ttk.Frame(self); marco.pack(fill='both',expand=True)
        self.c = tk.Canvas(marco,bg='#f8fafc',highlightthickness=0)
        v = ttk.Scrollbar(marco,orient='vertical',command=self.c.yview); v.pack(side='right',fill='y')
        h = ttk.Scrollbar(self,orient='horizontal',command=self.c.xview); h.pack(fill='x')
        self.c.configure(yscrollcommand=v.set,xscrollcommand=h.set); self.c.pack(fill='both',expand=True)
        self.c.bind('<B1-Motion>',self.arrastrar)
        pie = ttk.Frame(self,padding=10); pie.pack(fill='x')
        self.orden = ttk.Combobox(pie,values=['inorden','preorden','postorden'],state='readonly',width=12); self.orden.set('inorden'); self.orden.pack(side='left')
        for texto,fn in [('Preparar recorrido',self.preparar),('Siguiente',self.avanzar),('Reproducir',self.reproducir),('Pausar',self.pausar)]:
            ttk.Button(pie,text=texto,command=fn).pack(side='left',padx=4)
        self.resultado = ttk.Label(self,text='Arrastra los nodos para acomodarlos. Mover subárbol cambia sus conexiones.',padding=10,wraplength=950); self.resultado.pack(fill='x')
        self.protocol('WM_DELETE_WINDOW',self.cerrar)

    def pausar(self):
        if self.timer: self.after_cancel(self.timer); self.timer=None
    def limpiar(self):
        self.pausar(); self.pasos=[]; self.visitas=[]; self.resultado.configure(text='')
    def error(self,e): messagebox.showerror('Operación inválida',str(e),parent=self)
    def agregar(self):
        try: n=self.arbol.agregar(self.dato.get(),self.seleccion,self.lado.get())
        except ValueError as e: self.error(e); return
        self.limpiar(); self.dato.delete(0,'end'); self.distribuir()
    def eliminar(self):
        if not self.seleccion: self.error('Selecciona el nodo a eliminar.'); return
        if not messagebox.askyesno('Eliminar subárbol','Se eliminará el nodo y todos sus descendientes. ¿Continuar?',parent=self): return
        self.arbol.eliminar(self.seleccion); self.seleccion=None; self.origen=None; self.limpiar(); self.distribuir()
    def mover(self):
        self.pausar()
        if not self.seleccion: self.error('Selecciona el nodo que deseas mover.'); return
        self.origen=self.seleccion
        self.estado.configure(text='Elige el lado y haz clic en el nuevo padre. Se mueve también todo el subárbol.')
    def elegir(self,n):
        if self.origen:
            try: self.arbol.mover(self.origen,n,self.lado.get())
            except ValueError as e: self.error(e)
            else: self.limpiar(); self.distribuir(); self.estado.configure(text='Conexión actualizada. El recorrido seguirá los nuevos enlaces.')
            self.origen=None
        self.seleccion=n; self.dibujar()
    def arrastrar(self,e):
        if self.seleccion and not self.origen:
            self.pos[self.seleccion]=(max(40,self.c.canvasx(e.x)),max(40,self.c.canvasy(e.y))); self.dibujar()
    def ejemplo(self):
        if self.arbol.nodos and not messagebox.askyesno('Cargar ejemplo','¿Reemplazar el árbol actual por el ejemplo A–G?',parent=self): return
        self.limpiar(); self.arbol=ArbolBinario(); self.seleccion=None; self.origen=None
        a=self.arbol.agregar('A'); b=self.arbol.agregar('B',a); c=self.arbol.agregar('C',a,'derecho')
        self.arbol.agregar('D',b); self.arbol.agregar('E',b,'derecho')
        self.arbol.agregar('F',c); self.arbol.agregar('G',c,'derecho'); self.distribuir()

    def distribuir(self):
        self.arbol.validar()
        # Cada subárbol recibe espacio propio; se reserva también el lado vacío.
        anchos={}
        for n in self.arbol.recorrer('postorden'):
            anchos[n]=max(1,anchos.get(n.izquierdo,0))+max(1,anchos.get(n.derecho,0))
        self.pos={}; pila=[(self.arbol.raiz,0,0)]
        while pila:
            n,inicio,nivel=pila.pop()
            if n:
                izquierda=max(1,anchos.get(n.izquierdo,0))
                self.pos[n]=(80+(inicio+anchos[n]/2)*80,70+nivel*120)
                pila.extend([(n.izquierdo,inicio,nivel+1),(n.derecho,inicio+izquierda,nivel+1)])
        self.dibujar()
    def dibujar(self):
        self.c.delete('all')
        props=self.arbol.propiedades()
        tipos=', '.join(nombre for nombre in ('completo','perfecto','estricto') if props[nombre]) or 'general'
        self.estadisticas.configure(text=f"Nodos: {props['nodos']} · Hojas: {props['hojas']} · Altura: {props['altura']} · Niveles: {props['niveles']} · Tipo: {tipos}")
        niveles={}
        pila=[(self.arbol.raiz,0)]
        while pila:
            n,nivel=pila.pop()
            if n:
                niveles[n]=nivel
                pila.extend([(n.izquierdo,nivel+1),(n.derecho,nivel+1)])
        for n,(x,y) in self.pos.items():
            for lado in ('izquierdo','derecho'):
                hijo=getattr(n,lado)
                if hijo:
                    dx,dy=self.pos[hijo]; self.c.create_line(x,y,dx,dy,arrow='last',width=2,fill='#6366f1')
                    self.c.create_text((x+dx)/2,(y+dy)/2,text='I' if lado=='izquierdo' else 'D',fill='#4338ca')
        for i,n in enumerate(self.arbol.nodos):
            x,y=self.pos[n]; tag=f'n{i}'
            color='#fde68a' if n is self.seleccion else '#bbf7d0' if n in self.visitas else '#e0e7ff'
            self.c.create_oval(x-32,y-25,x+32,y+25,fill=color,outline='#6366f1',width=2,tags=tag)
            self.c.create_text(x,y,text=n.dato[:10],tags=tag)
            self.c.tag_bind(tag,'<Button-1>',lambda e,n=n:self.elegir(n))
            self.c.create_text(x,y-37,text=('RAÍZ · ' if n is self.arbol.raiz else '')+f'Nivel {niveles[n]}',fill='#475569')
            if not n.izquierdo and not n.derecho: self.c.create_text(x,y+38,text='I: NULL · D: NULL',fill='#64748b')
        self.c.configure(scrollregion=(0,0,max([900]+[x+80 for x,y in self.pos.values()]),max([450]+[y+80 for x,y in self.pos.values()])))
    def preparar(self):
        self.limpiar(); self.pasos=self.arbol.recorrer(self.orden.get()); self.estado.configure(text='Recorrido preparado. Pulsa Siguiente o Reproducir.' if self.pasos else 'El árbol está vacío.'); self.dibujar()
    def avanzar(self):
        if self.pasos:
            n=self.pasos.pop(0); self.visitas.append(n); self.seleccion=n
            self.resultado.configure(text=' → '.join(n.dato for n in self.visitas)); self.dibujar()
            if not self.pasos: self.estado.configure(text='Recorrido terminado.')
    def reproducir(self):
        self.pausar(); self.avanzar()
        if self.pasos: self.timer=self.after(650,self.reproducir)
    def cerrar(self): self.pausar(); self.destroy()

if __name__=='__main__': Aplicacion().mainloop()
