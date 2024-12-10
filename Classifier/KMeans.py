import numpy as np
import matplotlib.pyplot as plt

# 1. Cargar el dataset Iris
def load_iris_dataset(file_path):
    data = np.genfromtxt(file_path, delimiter=',', dtype=str, skip_header=1)
    features = data[:, 1:-1].astype(float)  # Tomamos las columnas 1 a 4 como características
    classes = data[:, -1]  # La última columna contiene las clases
    return features, classes

# 2. Inicializar centroides
def initialize_centroids(X, k):
    np.random.seed(42)
    random_indices = np.random.permutation(X.shape[0])[:k]
    return X[random_indices]

# 3. Asignar puntos al centroide más cercano
def assign_clusters(X, centroids):
    distances = np.sqrt(((X[:, np.newaxis] - centroids) ** 2).sum(axis=2))
    return np.argmin(distances, axis=1)

# 4. Actualizar centroides
def update_centroids(X, labels, k):
    new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])
    return new_centroids

# 5. Implementar el bucle completo de K-Means
def kmeans(X, k, max_iters=100, tol=1e-4):
    centroids = initialize_centroids(X, k)
    for _ in range(max_iters):
        old_centroids = centroids
        labels = assign_clusters(X, centroids)
        centroids = update_centroids(X, labels, k)
        if np.all(np.abs(centroids - old_centroids) < tol):
            break
    return centroids, labels

# 6. Visualizar los resultados
def plot_clusters_with_classes(X, labels, centroids, classes):
    # Crear un mapeo de colores para las clases reales
    unique_classes = np.unique(classes)
    class_colors = {cls: idx for idx, cls in enumerate(unique_classes)}
    true_colors = np.array([class_colors[cls] for cls in classes])

    # Crear la figura
    plt.figure(figsize=(10, 6))

    # Graficar cada clase con colores específicos
    for cls in unique_classes:
        cls_indices = classes == cls
        plt.scatter(X[cls_indices, 0], X[cls_indices, 1],
                    label=f'Clase: {cls}', s=50, alpha=0.7)

    # Graficar los clusters formados por K-Means
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='cool', s=20, alpha=0.4, label='Clusters K-Means')

    # Graficar los centroides
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=200, alpha=0.9, label='Centroides')

    # Añadir título y leyenda
    plt.title('Clusters K-Means con Clases Reales')
    plt.legend(loc='best')
    plt.show()

# Main
if __name__ == "__main__":
    # Ruta del archivo Iris.csv
    file_path = 'Iris.csv'  # Cambia esta ruta si el archivo está en otra ubicación

    # Cargar datos
    X, classes = load_iris_dataset(file_path)

    # Ejecutar K-Means
    k = 3  # Elegimos 3 clusters ya que Iris tiene 3 clases
    final_centroids, final_labels = kmeans(X, k)

    # Mostrar los centroides finales
    print("Centroides finales:")
    print(final_centroids)

    # Visualizar los clusters con clases reales
    plot_clusters_with_classes(X, final_labels, final_centroids, classes)
