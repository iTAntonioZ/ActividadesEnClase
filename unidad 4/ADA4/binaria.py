def buscar_binaria(lista, objetivo):
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio] == objetivo:
            return medio
        if lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1


def ejecutar():
    matriculas = [1002, 1015, 1028, 1040, 1053, 1071, 1090]
    print('Matrículas:', matriculas)
    try:
        objetivo = int(input('Matrícula a buscar: '))
    except ValueError:
        print('Ingresa un número entero.')
        return
    indice = buscar_binaria(matriculas, objetivo)
    print(f'Encontrada en la posición {indice + 1}.' if indice != -1 else 'Matrícula no encontrada.')


if __name__ == '__main__':
    ejecutar()
