class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = self.derecho = self.padre = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None
        self.nodos = []

    def agregar(self, dato, padre=None, lado='izquierdo'):
        if not str(dato).strip():
            raise ValueError('Escribe un dato.')
        if self.raiz is not None and padre is None:
            raise ValueError('Selecciona el padre del nuevo nodo.')
        if padre is not None:
            self._sitio(padre, lado)
        n = Nodo(str(dato).strip())
        self.nodos.append(n)
        if padre is None:
            self.raiz = n
        else:
            setattr(padre, lado, n)
            n.padre = padre
        return n

    def _sitio(self, padre, lado):
        if padre not in self.nodos or lado not in ('izquierdo', 'derecho'):
            raise ValueError('Padre o lado inválido.')
        if getattr(padre, lado) is not None:
            raise ValueError('Ese lugar ya está ocupado. Elige el otro lado o mueve primero su nodo.')

    def mover(self, nodo, padre, lado):
        if nodo not in self.nodos:
            raise ValueError('Selecciona un nodo existente.')
        self._sitio(padre, lado)
        actual = padre
        while actual:
            if actual is nodo:
                raise ValueError('No puedes conectar un nodo consigo mismo ni con sus descendientes.')
            actual = actual.padre
        if nodo is self.raiz:
            raise ValueError('La raíz no se puede mover debajo de otro nodo.')
        anterior = nodo.padre
        setattr(anterior, 'izquierdo' if anterior.izquierdo is nodo else 'derecho', None)
        setattr(padre, lado, nodo)
        nodo.padre = padre

    def eliminar(self, nodo):
        if nodo not in self.nodos:
            raise ValueError('Selecciona un nodo.')
        retirados = self.recorrer('preorden', nodo)
        if nodo.padre:
            p = nodo.padre
            setattr(p, 'izquierdo' if p.izquierdo is nodo else 'derecho', None)
        else:
            self.raiz = None
        for n in retirados:
            self.nodos.remove(n)
            n.padre = n.izquierdo = n.derecho = None

    def recorrer(self, orden='inorden', inicio=None):
        if orden not in ('inorden', 'preorden', 'postorden'):
            raise ValueError('Recorrido inválido.')
        salida = []
        pila = [(self.raiz if inicio is None else inicio, False)]
        while pila:
            n, emitir = pila.pop()
            if n is None: continue
            if emitir:
                salida.append(n)
            elif orden == 'preorden':
                pila.extend([(n.derecho, False), (n.izquierdo, False), (n, True)])
            elif orden == 'inorden':
                pila.extend([(n.derecho, False), (n, True), (n.izquierdo, False)])
            else:
                pila.extend([(n, True), (n.derecho, False), (n.izquierdo, False)])
        return salida

    def validar(self):
        if self.raiz is None:
            if self.nodos: raise ValueError('Hay nodos sin raíz.')
            return True
        if self.raiz.padre is not None:
            raise ValueError('La raíz no puede tener padre.')
        vistos = set()
        pila = [self.raiz]
        while pila:
            n = pila.pop()
            if n in vistos or n not in self.nodos:
                raise ValueError('Ciclo, padre compartido o nodo externo.')
            vistos.add(n)
            for hijo in (n.izquierdo, n.derecho):
                if hijo:
                    if hijo.padre is not n: raise ValueError('Padre inconsistente.')
                    pila.append(hijo)
        if vistos != set(self.nodos): raise ValueError('Hay nodos desconectados.')
        return True

    def propiedades(self):
        self.validar()
        if self.raiz is None:
            return dict(nodos=0, hojas=0, altura=-1, niveles=0, completo=True, perfecto=True, estricto=True)
        cola = [(self.raiz,0)]
        hojas=[]; hueco=False; completo=True; estricto=True
        for n,nivel in cola:
            hijos=[n.izquierdo,n.derecho]
            if not any(hijos): hojas.append(nivel)
            if sum(h is not None for h in hijos)==1: estricto=False
            for h in hijos:
                if h is None: hueco=True
                else:
                    if hueco: completo=False
                    cola.append((h,nivel+1))
        altura=max(d for _,d in cola)
        return dict(nodos=len(cola),hojas=len(hojas),altura=altura,niveles=altura+1,
                    completo=completo,perfecto=estricto and len(set(hojas))==1,estricto=estricto)
