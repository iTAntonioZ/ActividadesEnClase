pendientes = []

def menu():
    print("\n--- LISTA DE PENDIENTES ---")
    print("0. Salir")
    print("1. Añadir nuevo pendiente")
    print("2. Eliminar / marcar como listo")
    print("3. Visualizar lista")

    opcion = int(input("Ingresa una opción: "))

    if opcion == 0:
        print("Programa finalizado.")
        return

    elif opcion == 1:
        pendiente = input("Ingresa el nuevo pendiente: ")
        pendientes.append(pendiente)
        print("Pendiente añadido.")

    elif opcion == 2:
        if len(pendientes) == 0:
            print("No hay pendientes.")
        else:
            print("\nPendientes:")
            for i in range(len(pendientes)):
                print(i + 1, ".", pendientes[i])

            numero = int(input("Ingresa el número del pendiente: "))

            if numero > 0 and numero <= len(pendientes):
                pendientes.pop(numero - 1)
                print("Pendiente eliminado / marcado como listo.")
            else:
                print("Número inválido.")

    elif opcion == 3:
        if len(pendientes) == 0:
            print("No tienes pendientes.")
        else:
            print("\n--- MIS PENDIENTES ---")
            for i in range(len(pendientes)):
                print(i + 1, ".", pendientes[i])

    else:
        print("Opción inválida.")

    # Llamada recursiva
    menu()


menu()