## Welcome to my repository

### This is work in the class
#### Ventas mensuales por departamento

Programa en **Java** y **Python** que administra un arreglo bidimensional con las ventas mensuales de tres departamentos: **Ropa**, **Deportes** y **Juguetería**.

##### ¿En qué consiste?

Se usa una matriz de **12 filas × 3 columnas**:

- Cada **fila** representa un mes (Enero a Diciembre).
- Cada **columna** representa un departamento (Ropa, Deportes, Juguetería).
- Cada **celda** guarda el monto de venta de ese departamento en ese mes.
- Una celda vacía (`null` en Java, `None` en Python) significa que aún no hay venta registrada.

| | Ropa | Deportes | Juguetería |
|---|---|---|---|
| Enero | | | |
| Febrero | | | |
| ... | | | |
| Diciembre | | | |

##### Archivos

- `ventasDepartamentos.java`: versión en Java.
- `ventas_departamentos.py`: versión en Python.

##### Métodos

### 1. `insertar(mes, depto, monto)`
Guarda el monto de venta en la posición `[mes][depto]`. Valida que el mes (0-11) y el departamento (0-2) existan; si ya había un valor, lo reemplaza. Devuelve `true/True` si se insertó y `false/False` si la posición no es válida.

### 2. `buscar(monto)` y `consultar(mes, depto)`
- `buscar(monto)` recorre toda la matriz con dos ciclos anidados y muestra en qué mes y departamento aparece ese monto (puede aparecer más de una vez).
- `consultar(mes, depto)` regresa directamente la venta de un mes y departamento específicos.

### 3. `eliminar(mes, depto)`
Borra la venta de un departamento en un mes en particular, dejando la celda vacía. Devuelve `true/True` si había una venta que eliminar y `false/False` si la posición es inválida o ya estaba vacía.

##### Extra: `mostrarTabla()` / `mostrar_tabla()`
Imprime la matriz completa en formato de tabla (las celdas vacías se muestran con `-`).

### Cómo ejecutarlo

**Java**
```bash
cd EnJava
java VentasDepartamentos
```

**Python**
```bash
cd Ejercicios
python ventas_departamentos.py
```

Ambos programas muestran un menú interactivo en consola:

```
1. Insertar venta
2. Buscar venta por monto
3. Consultar venta (mes y departamento)
4. Eliminar venta
5. Mostrar tabla
0. Salir
```