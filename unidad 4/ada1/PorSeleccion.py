
# Metodo de ordenamiento: Seleccion

def seleccion(lista):
    n = len(lista)

    for i in range(n):
        menor = i

        # Buscar el elemento menor
        for j in range(i + 1, n):
            if lista[j] < lista[menor]:
                menor = j

        # Intercambiar elementos
        lista[i], lista[menor] = lista[menor], lista[i]

    return lista


# Programa principal
numeros = [8, 3, 5, 1, 9, 2, 7, 4]

print("Lista original:", numeros)

resultado = seleccion(numeros)

print("Lista ordenada:", resultado)
