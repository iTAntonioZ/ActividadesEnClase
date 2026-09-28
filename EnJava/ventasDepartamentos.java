import java.util.Scanner;

public class ventasDepartamentos {

    static final String[] MESES = {
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    };
    static final String[] DEPARTAMENTOS = { "Ropa", "Deportes", "Jugueteria" };

    static Double[][] ventas = new Double[MESES.length][DEPARTAMENTOS.length];

    static boolean insertar(int mes, int depto, double monto) {
        if (!posicionValida(mes, depto)) {
            return false;
        }
        ventas[mes][depto] = monto;
        return true;
    }

    static int buscar(double monto) {
        int encontrados = 0;
        for (int i = 0; i < MESES.length; i++) {
            for (int j = 0; j < DEPARTAMENTOS.length; j++) {
                if (ventas[i][j] != null && ventas[i][j] == monto) {
                    System.out.println("Encontrado: " + MESES[i] + " - " + DEPARTAMENTOS[j] + " = $" + monto);
                    encontrados++;
                }
            }
        }
        return encontrados;
    }

    static Double consultar(int mes, int depto) {
        if (!posicionValida(mes, depto)) {
            return null;
        }
        return ventas[mes][depto];
    }

    static boolean eliminar(int mes, int depto) {
        if (!posicionValida(mes, depto) || ventas[mes][depto] == null) {
            return false;
        }
        ventas[mes][depto] = null;
        return true;
    }

    static boolean posicionValida(int mes, int depto) {
        return mes >= 0 && mes < MESES.length && depto >= 0 && depto < DEPARTAMENTOS.length;
    }

    static void mostrarTabla() {
        System.out.printf("%n%-12s", "");
        for (String d : DEPARTAMENTOS) {
            System.out.printf("%-14s", d);
        }
        System.out.println();
        for (int i = 0; i < MESES.length; i++) {
            System.out.printf("%-12s", MESES[i]);
            for (int j = 0; j < DEPARTAMENTOS.length; j++) {
                String valor = ventas[i][j] == null ? "-" : String.format("$%.2f", ventas[i][j]);
                System.out.printf("%-14s", valor);
            }
            System.out.println();
        }
    }

    static int pedirMes(Scanner sc) {
        for (int i = 0; i < MESES.length; i++) {
            System.out.println((i + 1) + ". " + MESES[i]);
        }
        System.out.print("Elige el mes (1-12): ");
        return leerEntero(sc) - 1;
    }

    static int pedirDepartamento(Scanner sc) {
        for (int j = 0; j < DEPARTAMENTOS.length; j++) {
            System.out.println((j + 1) + ". " + DEPARTAMENTOS[j]);
        }
        System.out.print("Elige el departamento (1-3): ");
        return leerEntero(sc) - 1;
    }

    static int leerEntero(Scanner sc) {
        try {
            return Integer.parseInt(sc.nextLine().trim());
        } catch (NumberFormatException e) {
            return -1000;
        }
    }

    static double leerDecimal(Scanner sc) {
        try {
            return Double.parseDouble(sc.nextLine().trim());
        } catch (NumberFormatException e) {
            return Double.NaN;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int opcion;
        do {
            System.out.println("\n=== VENTAS POR DEPARTAMENTO ===");
            System.out.println("1. Insertar venta");
            System.out.println("2. Buscar venta por monto");
            System.out.println("3. Consultar venta (mes y departamento)");
            System.out.println("4. Eliminar venta");
            System.out.println("5. Mostrar tabla");
            System.out.println("0. Salir");
            System.out.print("Opcion: ");
            opcion = leerEntero(sc);

            switch (opcion) {
                case 1: {
                    int mes = pedirMes(sc);
                    int depto = pedirDepartamento(sc);
                    System.out.print("Monto de la venta: ");
                    double monto = leerDecimal(sc);
                    if (Double.isNaN(monto) || monto < 0) {
                        System.out.println("Monto invalido.");
                    } else if (insertar(mes, depto, monto)) {
                        System.out.println("Venta insertada correctamente.");
                    } else {
                        System.out.println("Mes o departamento invalido.");
                    }
                    break;
                }
                case 2: {
                    System.out.print("Monto a buscar: ");
                    double monto = leerDecimal(sc);
                    if (Double.isNaN(monto)) {
                        System.out.println("Monto invalido.");
                    } else if (buscar(monto) == 0) {
                        System.out.println("No se encontro ese monto.");
                    }
                    break;
                }
                case 3: {
                    int mes = pedirMes(sc);
                    int depto = pedirDepartamento(sc);
                    if (!posicionValida(mes, depto)) {
                        System.out.println("Mes o departamento invalido.");
                    } else {
                        Double v = consultar(mes, depto);
                        System.out.println(v == null ? "Sin venta registrada." : "Venta: $" + v);
                    }
                    break;
                }
                case 4: {
                    int mes = pedirMes(sc);
                    int depto = pedirDepartamento(sc);
                    System.out.println(eliminar(mes, depto)
                            ? "Venta eliminada."
                            : "No hay venta que eliminar en esa posicion.");
                    break;
                }
                case 5:
                    mostrarTabla();
                    break;
                case 0:
                    System.out.println("Hasta luego.");
                    break;
                default:
                    System.out.println("Opcion invalida.");
            }
        } while (opcion != 0);
        sc.close();
    }
}