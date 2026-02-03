import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#---

np.random.seed(42)

data = np.column_stack((
    np.random.uniform(15, 35, 100),   # Temperatura
    np.random.uniform(40, 90, 100),   # Humedad
    np.random.uniform(950, 1050, 100) # Presión
))

#---

def build_kd_tree(points, depth=0):
    if len(points) == 0:
        return None

    k = len(points[0])
    axis = depth % k

    points = sorted(points, key=lambda x: x[axis])
    median = len(points) // 2

    return {
        "point": points[median],
        "axis": axis,
        "left": build_kd_tree(points[:median], depth + 1),
        "right": build_kd_tree(points[median + 1:], depth + 1)
    }
#---
def range_search(node, lower, upper, results):
    if node is None:
        return

    # Verifica si el punto está dentro del rango
    dentro = True
    for i in range(len(lower)):
        if node["point"][i] < lower[i] or node["point"][i] > upper[i]:
            dentro = False
            break

    if dentro:
        results.append(node["point"])

    axis = node["axis"]

    if lower[axis] <= node["point"][axis]:
        range_search(node["left"], lower, upper, results)

    if upper[axis] >= node["point"][axis]:
        range_search(node["right"], lower, upper, results)

#---

np.random.seed(42)
data = np.column_stack((
np.random.uniform(15, 35, 100), # Temperatura
np.random.uniform(40, 90, 100), # Humedad
np.random.uniform(950, 1050, 100) # Presión
))

#---

kd_tree = build_kd_tree(data.tolist())

lower_bounds = [20, 60, 980]
upper_bounds = [25, 90, 1020]

results = []
range_search(kd_tree, lower_bounds, upper_bounds, results)

print("Registros encontrados:")
for r in results:
    print(r)

#---

df = pd.DataFrame(data, columns=["Temperatura", "Humedad", "Presion"])
df.head()

#---

X = df[["Humedad", "Presion"]]   # Variables independientes (matriz)
y = df["Temperatura"]           # Variable dependiente (vector)

modelo = LinearRegression()
modelo.fit(X, y)

df["Temp_Predicha"] = modelo.predict(X)
df.head()

#---

plt.figure()
plt.scatter(df["Humedad"], df["Temperatura"])
plt.xlabel("Humedad (%)")
plt.ylabel("Temperatura (°C)")
plt.title("Relación entre Humedad y Temperatura")
plt.show()

#---

plt.figure()
plt.plot(df["Temperatura"].values, label="Temperatura Real")
plt.plot(df["Temp_Predicha"].values, label="Temperatura Predicha")
plt.xlabel("Índice de registros")
plt.ylabel("Temperatura (°C)")
plt.title("Comparación: Temperatura Real vs Predicha")
plt.legend()
plt.show()

#---

def build_kd_tree(points, depth=0):
    ...

def range_search(node, lower, upper, results):
    ...

kd_tree = build_kd_tree(data.tolist())


#  Búsqueda secuencial (lineal)
def linear_search(points, lower, upper):
    results = []
    for p in points:
        if all(lower[i] <= p[i] <= upper[i] for i in range(len(lower))):
            results.append(p)
    return results

#---

#  Comparación de tiempos
import time

# Búsqueda lineal
start = time.perf_counter()
linear_results = linear_search(data.tolist(), lower_bounds, upper_bounds)
end = time.perf_counter()
linear_time = end - start

# Búsqueda KD-Tree
results_kd = []
start = time.perf_counter()
range_search(kd_tree, lower_bounds, upper_bounds, results_kd)
end = time.perf_counter()
kd_time = end - start

print("Tiempo búsqueda lineal:", linear_time)
print("Tiempo búsqueda KD-Tree:", kd_time)

#---

# Tabla comparativa
import pandas as pd

comparison_table = pd.DataFrame({
    "Método de Búsqueda": ["Búsqueda Secuencial", "KD-Tree"],
    "Tiempo de Ejecución (s)": [linear_time, kd_time],
    "Resultados Encontrados": [len(linear_results), len(results_kd)],
    "Eficiencia Teórica": ["O(n)", "O(log n)"]
})

comparison_table

#---

