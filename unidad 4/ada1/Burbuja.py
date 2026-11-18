def burbuja(lista):
    n = len(lista)

    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                # Intercambiar elementos
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    return lista


# Programa principal
numeros = [8, 3, 5, 1, 9, 2, 7, 4]

print("Lista original:", numeros)

resultado = burbuja(numeros)

print("Lista ordenada:", resultado)
