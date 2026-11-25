from secuencial import ejecutar as secuencial
from binaria import ejecutar as binaria
from hash_busqueda import ejecutar as hash_busqueda


def main():
    opciones = {'1': secuencial, '2': binaria, '3': hash_busqueda}
    while True:
        print('\n--- MÉTODOS DE BÚSQUEDA ---')
        print('1. Búsqueda secuencial')
        print('2. Búsqueda binaria')
        print('3. Búsqueda hash')
        print('0. Salir')
        opcion = input('Selecciona una opción: ').strip()
        if opcion == '0':
            print('Programa finalizado.')
            break
        if opcion in opciones:
            opciones[opcion]()
        else:
            print('Opción inválida.')


if __name__ == '__main__':
    main()
