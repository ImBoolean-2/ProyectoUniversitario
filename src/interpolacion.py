import cv2
import numpy as np
from numpy import array, polyfit, polyval, zeros_like
from cv2 import cvtColor, ORB_create, COLOR_BGR2GRAY

def calcular_coeficientes(imagen):
    def obtener_puntos_de_control(imagen):
        imagen_gris = cvtColor(imagen, COLOR_BGR2GRAY) 
        orb = ORB_create() 
        puntos_clave = orb.detect(imagen_gris, None) 
        puntos_de_control = [(int(pk.pt[0]), int(pk.pt[1])) for pk in puntos_clave] 
        return puntos_de_control

    puntos_de_control = obtener_puntos_de_control(imagen)
    
    x = array([punto[0] for punto in puntos_de_control])
    y = array([punto[1] for punto in puntos_de_control])
    
    if len(puntos_de_control) > 1:
        coeficientes = polyfit(x, y, min(len(puntos_de_control) - 1, 3))  
    else:
        raise ValueError("No se encontraron suficientes puntos de control para calcular coeficientes.")
    
    return coeficientes

def interpolar(imagen, coeficientes):
    imagen_filtrada = cv2.GaussianBlur(imagen, (5, 5), 0)
    
    if len(imagen_filtrada.shape) == 2: 
        imagen_interpolada = polyval(coeficientes, imagen_filtrada) 
    else:
        imagen_interpolada = zeros_like(imagen_filtrada) 
        for canal in range(imagen_filtrada.shape[2]):
            imagen_interpolada[:, :, canal] = polyval(coeficientes, imagen_filtrada[:, :, canal])
    return imagen_interpolada

def reducir_ruido(imagen):
    # Aplicar filtro Gaussiano para reducir ruido
    imagen_filtrada = cv2.GaussianBlur(imagen, (5, 5), 0)
    return imagen_filtrada

def enfocar_y_refinar(imagen):
    # Aplicar enfoque utilizando un filtro de sharpening
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    imagen_enfocada = cv2.filter2D(imagen, -1, kernel)
    
    # Aplicar refinamiento utilizando un filtro de bilateral
    imagen_refinada = cv2.bilateralFilter(imagen_enfocada, 5, 50, 50)
    
    return imagen_refinada

# Load the image
imagen = cv2.imread('C:\\Users\\AUTONOMA\\Downloads\\gato.png')

# Calculate the coefficients
coeficientes = calcular_coeficientes(imagen)
#reducir ruido
imagen_reducida_ruido=reducir_ruido(imagen)

# Interpolate the image
imagen_interpolada = interpolar(imagen, coeficientes)

# Apply focus and refinement
imagen_enfocada_y_refinada = enfocar_y_refinar(imagen)


# Display the original and interpolated images
cv2.imshow('Imagen original', imagen)
cv2.imshow('Imagen reducida ruido', imagen_reducida_ruido)
cv2.imshow('Imagen interpolada', imagen_interpolada)
cv2.imshow('Imagen interpolada enfocada y refinada', imagen_enfocada_y_refinada)
cv2.waitKey(0)
cv2.destroyAllWindows()