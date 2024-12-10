#!/usr/bin/env python
# coding: utf-8

# # KNN from Scratch
# 
# 
# Este cuaderno implementa KNN utilizando únicamente numpy y datos del dataset Iris.
# Incluye pasos para cargar datos, dividirlos, calcular distancias y predecir etiquetas.

# In[5]:


import numpy as np


# ### 1. Función para cargar el dataset Iris
# 
#  Usamos la librería sklearn para obtener el dataset Iris, pero la implementación del algoritmo
# será puramente con NumPy. El dataset contiene 150 muestras de flores con 4 características
#  y 3 clases (setosa, versicolor, virginica).

# In[7]:


def load_iris_dataset_csv():
  data = np.genfromtxt('Iris.csv', delimiter=',', dtype=str, skip_header=1) 
  features = data[:, 1:-1].astype(float) 
  classes = data[:, -1]    
  unique_classes, encoded_classes = np.unique(classes, return_inverse=True)
  
  print("Clases únicas:", unique_classes)
  print("Clases codificadas:", encoded_classes[:5]) \
      
  print("\nCaracterísticas:")
  print(features[:5])  # Mostrar las primeras 5 filas 
  print("\nClases codificadas:")
  print(encoded_classes[:5])  # Mostrar las primeras 5 clases codificadas 
  
  return features, encoded_classes


# ### Extracción de Característica y Clases

# In[8]:


features, encoded_classes =load_iris_dataset_csv()


#  2. División de datos en entrenamiento y prueba
# Para evaluar nuestro modelo, dividimos los datos en dos partes:
#  - Conjunto de entrenamiento (80%)
#  - Conjunto de prueba (20%)

# In[12]:


def train_test_split(X, y, test_size=0.2, random_seed=42):
    np.random.seed(random_seed)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)  # Barajamos los índices aleatoriamente
    split_index = int(X.shape[0] * (1 - test_size))  # Índice para dividir
    train_indices = indices[:split_index]
    test_indices = indices[split_index:]
    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]


# Dividimos los datos
# 

# In[14]:


X_train, X_test, y_train, y_test = train_test_split(features, encoded_classes)
print("\nTamaño del conjunto de entrenamiento:", X_train.shape[0])
print("Tamaño del conjunto de prueba:", X_test.shape[0])


# 3. Función para calcular distancias euclidianas
# 
# 
# La distancia euclidiana entre dos puntos x1 y x2 es:
# d = sqrt(sum((x1 - x2)^2))
# Implementamos esta fórmula con NumPy, soportando cálculos vectorizados.

# In[15]:


def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2, axis=1))


# ### Ejemplo de cálculo de distancias
# 

# In[16]:


example_distances = euclidean_distance(X_train, X_test[0])
print("\nDistancias a la primera instancia de prueba:\n", example_distances[:5])


#  4. Implementación de KNN
# 
# En KNN, para cada punto de prueba, calculamos las distancias a todos los puntos
# de entrenamiento, seleccionamos los k vecinos más cercanos y predecimos la clase
# por mayoría.

# In[17]:


def knn_predict(X_train, y_train, X_test, k=3):
    predictions = []
    for x in X_test:
        # 1. Calcular distancias desde el punto de prueba a todos los puntos de entrenamiento
        distances = euclidean_distance(X_train, x)
        # 2. Obtener los índices de los k vecinos más cercanos
        nearest_indices = distances.argsort()[:k]
        # 3. Obtener las etiquetas de los k vecinos más cercanos
        nearest_labels = y_train[nearest_indices]
        # 4. Clasificar por mayoría (la clase con más votos)
        predicted_label = np.bincount(nearest_labels.astype(int)).argmax()
        predictions.append(predicted_label)
    return np.array(predictions)


# ###  Realizamos predicciones en el conjunto de prueba

# In[18]:


k = 5  # Número de vecinos
predictions = knn_predict(X_train, y_train, X_test, k)
print("\nPredicciones (primeras 5):", predictions[:5])
print("Etiquetas reales (primeras 5):", y_test[:5])


#  5. Evaluación del modelo
# 
# Calculamos la precisión como el porcentaje de etiquetas correctamente predichas.

# In[19]:


accuracy = np.mean(predictions == y_test) * 100
print(f"\nPrecisión del modelo KNN (k={k}): {accuracy:.2f}%")

