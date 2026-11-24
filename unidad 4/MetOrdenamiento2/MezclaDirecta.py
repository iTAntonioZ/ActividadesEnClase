
class MezclaDirecta:

    def mezclar(self, izquierda, derecha):

        resultado = []
        i = 0
        j = 0

        while i < len(izquierda) and j < len(derecha):

            if izquierda[i] <= derecha[j]:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        resultado += izquierda[i:]
        resultado += derecha[j:]

        return resultado

    def ordenar(self, datos):

        resultado = datos.copy()
        tamaño = 1
        n = len(resultado)

        # Aumentamos el tamaño de los bloques
        while tamaño < n:

            nueva_lista = []

            for i in range(0, n, tamaño * 2):

                izquierda = resultado[i:i + tamaño]

                derecha = resultado[
                    i + tamaño:i + tamaño * 2
                ]

                # Combinamos los bloques
                nueva_lista.extend(
                    self.mezclar(izquierda, derecha)
                )

            resultado = nueva_lista
            tamaño *= 2

        return resultado


# Ejemplo de uso
numeros = [42, 16, 8, 53, 21, 4, 37, 11, 29]

metodo = MezclaDirecta()

resultado = metodo.ordenar(numeros)

print("Lista original:", numeros)
print("Lista ordenada:", resultado)
