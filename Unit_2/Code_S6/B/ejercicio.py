import numpy as np

# Crear un arreglo multidimensional (3x5) con valores aleatorios entre 1 y 20
arr = np.random.randint(1, 21, size=(3, 5))

# Mostrar el arreglo generado
print("Arreglo original:")
print(arr)

# Extraer una submatriz usando slicing (por ejemplo, las dos primeras filas y las tres primeras columnas)
submatriz = arr[:2, :3]

# Mostrar la submatriz
print("\nSubmatriz extraída (filas 0-1, columnas 0-2):")
print(submatriz)

# Filtrar los valores mayores a 10 del arreglo
valoresMayores10 = arr[arr > 10]

# Mostrar los valores mayores a 10
print("\nValores mayores a 10:")
print(valoresMayores10)

# Aplicar broadcasting sumando un vector a cada fila del arreglo
# Creamos un vector con 5 valores (uno para cada columna)
vector = np.array([1, 2, 3, 4, 5])
arrBroadcasted = arr + vector

# Mostrar el arreglo después del broadcasting
print("\nArreglo después de aplicar broadcasting:")
print(arrBroadcasted)

# Utilizar np.where() para modificar los valores menores a 5 por 0
arrModificado = np.where(arr < 5, 0, arr)

# Mostrar el arreglo modificado
print("\nArreglo después de aplicar np.where() (valores menores a 5 son 0):")
print(arrModificado)
