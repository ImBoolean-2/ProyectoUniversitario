# interpolation.py
import numpy as np

def calcular_coeficientes(puntos):
    # Asumiendo que 'puntos' es una lista de tuplas (x, y)
    x = np.array([punto[0] for punto in puntos])
    y = np.array([punto[1] for punto in puntos])
    # Calcula los coeficientes del polinomio
    coeficientes = np.polyfit(x, y, len(puntos) - 1)
    return coeficientes

def interpolar(imagen, coeficientes):
    # Asumiendo que 'imagen' es un array de NumPy y 'coeficientes' es retornado por 'calcular_coeficientes'
    altura, anchura = imagen.shape
    imagen_interpolada = np.zeros_like(imagen)
    # Aplica la interpolación a cada píxel
    for i in range(altura):
        for j in range(anchura):
            # Aquí aplicarías la interpolación usando los coeficientes
            # Por ejemplo, podrías usar np.polyval para evaluar el polinomio
            imagen_interpolada[i, j] = np.polyval(coeficientes, imagen[i, j])
    return imagen_interpolada
