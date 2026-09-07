class vectores:
    def __init__(self, datos):
        self.datos = datos

    def mostrar(self):
        for element in self.datos:
            print(element)

    def media(self):
        return sum(self.datos) / len(self.datos) if self.datos else 0

pares = [2, 4, 6, 8, 10]
impares = [1, 3, 5, 7, 9]

vec = vectores(pares)
vec_np = vectores(impares)

print("Pares:")
{vec.mostrar()}
print("Impares:")
vec_np.mostrar()

print(f"Media {vec.media()} de pares | Media {vec_np.media()} de impares")

