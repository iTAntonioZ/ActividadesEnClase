class Intercalacion:

    def ordenar(self, lista1, lista2):
        resultado = []

        i = 0
        j = 0

        while i < len(lista1) and j < len(lista2):

            if lista1[i] <= lista2[j]:
                resultado.append(lista1[i])
                i += 1
            else:
                resultado.append(lista2[j])
                j += 1

        while i < len(lista1):
            resultado.append(lista1[i])
            i += 1

        while j < len(lista2):
            resultado.append(lista2[j])
            j += 1

        return resultado


lista1 = [4, 9, 15, 28, 36]
lista2 = [2, 7, 12, 19, 31]

metodo = Intercalacion()

resultado = metodo.ordenar(lista1, lista2)

print("Primera lista:", lista1)
print("Segunda lista:", lista2)
print("Resultado:", resultado)
