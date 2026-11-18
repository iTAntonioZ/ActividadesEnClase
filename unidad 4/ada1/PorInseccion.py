
# Metodo de ordenamiento: Insercion

def insercion(lista):
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1

        # Buscar la posicion correcta
        while j >= 0 and lista[j] > actual:
            lista[j + 1] = lista[j]
            j -= 1

        lista[j + 1] = actual

    return lista


# Programa principal
numeros = [8, 3, 5, 1, 9, 2, 7, 4]

print("Lista original:", numeros)

resultado = insercion(numeros)

print("Lista ordenada:", resultado)
