MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
DEPARTAMENTOS = ["Ropa", "Deportes", "Jugueteria"]

ventas = [[None] * len(DEPARTAMENTOS) for _ in MESES]


def posicion_valida(mes, depto):
    return 0 <= mes < len(MESES) and 0 <= depto < len(DEPARTAMENTOS)


def insertar(mes, depto, monto):
    if not posicion_valida(mes, depto):
        return False
    ventas[mes][depto] = monto
    return True


def buscar(monto):
    encontrados = []
    for i, fila in enumerate(ventas):
        for j, valor in enumerate(fila):
            if valor is not None and valor == monto:
                encontrados.append((MESES[i], DEPARTAMENTOS[j]))
    return encontrados


def consultar(mes, depto):
    if not posicion_valida(mes, depto):
        return None
    return ventas[mes][depto]


def eliminar(mes, depto):
    if not posicion_valida(mes, depto) or ventas[mes][depto] is None:
        return False
    ventas[mes][depto] = None
    return True


def mostrar_tabla():
    print("\n" + " " * 12 + "".join(f"{d:<14}" for d in DEPARTAMENTOS))
    for i, mes in enumerate(MESES):
        celdas = "".join(
            f"{'-' if v is None else f'${v:.2f}':<14}" for v in ventas[i]
        )
        print(f"{mes:<12}{celdas}")


def pedir_entero(mensaje):
    try:
        return int(input(mensaje).strip())
    except ValueError:
        return -1000


def pedir_decimal(mensaje):
    try:
        return float(input(mensaje).strip())
    except ValueError:
        return None


def pedir_mes():
    for i, m in enumerate(MESES, 1):
        print(f"{i}. {m}")
    return pedir_entero("Elige el mes (1-12): ") - 1


def pedir_departamento():
    for j, d in enumerate(DEPARTAMENTOS, 1):
        print(f"{j}. {d}")
    return pedir_entero("Elige el departamento (1-3): ") - 1


def main():
    opcion = -1
    while opcion != 0:
        print("\n=== VENTAS POR DEPARTAMENTO ===")
        print("1. Insertar venta")
        print("2. Buscar venta por monto")
        print("3. Consultar venta (mes y departamento)")
        print("4. Eliminar venta")
        print("5. Mostrar tabla")
        print("0. Salir")
        opcion = pedir_entero("Opcion: ")

        if opcion == 1:
            mes = pedir_mes()
            depto = pedir_departamento()
            monto = pedir_decimal("Monto de la venta: ")
            if monto is None or monto < 0:
                print("Monto invalido.")
            elif insertar(mes, depto, monto):
                print("Venta insertada correctamente.")
            else:
                print("Mes o departamento invalido.")
        elif opcion == 2:
            monto = pedir_decimal("Monto a buscar: ")
            if monto is None:
                print("Monto invalido.")
            else:
                resultados = buscar(monto)
                if resultados:
                    for mes, depto in resultados:
                        print(f"Encontrado: {mes} - {depto} = ${monto}")
                else:
                    print("No se encontro ese monto.")
        elif opcion == 3:
            mes = pedir_mes()
            depto = pedir_departamento()
            if not posicion_valida(mes, depto):
                print("Mes o departamento invalido.")
            else:
                valor = consultar(mes, depto)
                print("Sin venta registrada." if valor is None else f"Venta: ${valor}")
        elif opcion == 4:
            mes = pedir_mes()
            depto = pedir_departamento()
            if eliminar(mes, depto):
                print("Venta eliminada.")
            else:
                print("No hay venta que eliminar en esa posicion.")
        elif opcion == 5:
            mostrar_tabla()
        elif opcion == 0:
            print("Hasta luego.")
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()