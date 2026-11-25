def buscar_hash(tabla, clave):
    return tabla.get(clave)


def ejecutar():
    contactos = {'ana': '555-0101', 'luis': '555-0102', 'maria': '555-0103', 'pedro': '555-0104'}
    print('Contactos:', ', '.join(contactos))
    clave = input('Nombre a buscar: ').strip().lower()
    telefono = buscar_hash(contactos, clave)
    print(f'Teléfono: {telefono}' if telefono is not None else 'Contacto no encontrado.')


if __name__ == '__main__':
    ejecutar()
