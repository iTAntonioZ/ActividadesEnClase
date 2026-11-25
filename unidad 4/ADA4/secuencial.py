def buscar_secuencial(lista, objetivo):
    for i, elemento in enumerate(lista):
        if elemento == objetivo:
            return i
    return -1


def ejecutar():
    productos = ['pan', 'leche', 'arroz', 'huevo', 'queso']
    print('Productos:', ', '.join(productos))
    objetivo = input('Producto a buscar: ').strip().lower()
    indice = buscar_secuencial(productos, objetivo)
    print(f'Encontrado en la posición {indice + 1}.' if indice != -1 else 'Producto no encontrado.')


if __name__ == '__main__':
    ejecutar()
