## Welcome to my repository

### This is work in the class and homework

---  

#### Torre de Hanói

##### 1. ¿Qué es?

La **Torre de Hanói** es un problema matemático y de lógica que consiste en trasladar una cantidad de discos de diferentes tamaños desde una torre de origen hasta una torre de destino, utilizando una tercera torre como auxiliar.

Para resolverlo se deben cumplir tres reglas:

1. Solo se puede mover un disco a la vez.
2. No se puede colocar un disco grande encima de uno más pequeño.
3. Se deben trasladar todos los discos a la torre de destino respetando las reglas anteriores.

Este problema se utiliza principalmente para comprender el funcionamiento de los **algoritmos recursivos**, ya que permite dividir un problema grande en otros más pequeños.

##### 2. Métodos

Para implementar la Torre de Hanói en Python se pueden utilizar los siguientes métodos:

- **Método recursivo (`hanoi`)**: Es el método principal. Se llama a sí mismo para resolver el problema, trasladando los discos entre las tres torres hasta completar el proceso.

- **Método principal (`main`)**: Permite ejecutar el programa, solicitar la cantidad de discos y mostrar los resultados.

- **Medición del tiempo (`time.perf_counter`)**: Permite conocer cuánto tarda el programa en ejecutar el algoritmo para diferentes cantidades de discos.

##### Cantidad de movimientos

El número mínimo de movimientos necesarios se calcula mediante la fórmula:

$$
M(n) = 2^n - 1
$$

Donde `n` representa la cantidad de discos.

| Discos | Movimientos mínimos |
|--------|--------------------:|
| 5      | 31                  |
| 10     | 1,023               |
| 30     | 1,073,741,823       |
| 64     | 18,446,744,073,709,551,615 |

Esto demuestra que, conforme aumenta la cantidad de discos, el número de movimientos crece exponencialmente.

##### 3. Conclusiones

Considero que la **Torre de Hanói** es una buena manera de comprender cómo funciona la recursividad en la programación, ya que demuestra que un problema complicado puede resolverse dividiéndolo en tareas más pequeñas.

Su funcionamiento también puede relacionarse con situaciones cotidianas, como organizar objetos, planificar actividades. Además, permite comprender la importancia de crear algoritmos eficientes, porque al aumentar la cantidad de discos también aumenta considerablemente el tiempo necesario para resolver el problema.

---

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