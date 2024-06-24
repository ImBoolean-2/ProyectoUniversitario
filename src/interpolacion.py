# interpolacion.py
from numpy import array, polyfit, polyval, zeros_like
from cv2 import cvtColor, ORB_create, COLOR_BGR2GRAY

def calcular_coeficientes(imagen):
    def obtener_puntos_de_control(imagen):
        imagen_gris = cvtColor(imagen, COLOR_BGR2GRAY) # Convertir a escala de grises para la detección de características
        orb = ORB_create() # Inicializar ORB
        puntos_clave = orb.detect(imagen_gris, None) # Detectar puntos clave
        puntos_de_control = [(int(pk.pt[0]), int(pk.pt[1])) for pk in puntos_clave] # Convertir puntos clave a una lista de tuplas (x, y)
        
        return puntos_de_control

    puntos_de_control = obtener_puntos_de_control(imagen)
    x = array([punto[0] for punto in puntos_de_control])
    y = array([punto[1] for punto in puntos_de_control])
    
    # Verificar que hay suficientes puntos para calcular un polinomio
    if len(puntos_de_control) > 1:
        coeficientes = polyfit(x, y, min(len(puntos_de_control) - 1, 3))  # Limitar el grado para evitar errores Calcula los coeficientes del polinomio
    else:
        raise ValueError("No se encontraron suficientes puntos de control para calcular coeficientes.")
    
    return coeficientes

def interpolar(imagen, coeficientes):
    if len(imagen.shape) == 2: # Verifica si la imagen tiene un canal de color (es decir, es en escala de grises)
        imagen_interpolada = polyval(coeficientes, imagen) # Aplica la interpolación directamente a toda la imagen
    else:
        imagen_interpolada = zeros_like(imagen) # Si la imagen es a color, aplica la interpolación a cada canal por separado
        for canal in range(imagen.shape[2]):
            imagen_interpolada[:, :, canal] = polyval(coeficientes, imagen[:, :, canal])
            
    return imagen_interpolada