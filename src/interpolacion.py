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
    imagen_filtrada = cv2.GaussianBlur(imagen, (5, 5), 0)
    return imagen_filtrada


def enfocar_y_refinar(imagen):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    imagen_enfocada = cv2.filter2D(imagen, -1, kernel)
    imagen_refinada = cv2.bilateralFilter(imagen_enfocada, 5, 50, 50)
    return imagen_refinada


if __name__ == "__main__":
    # Código de prueba
    imagen = cv2.imread('C:\\Users\\AUTONOMA\\Desktop\\input.jpg')
    if imagen is None:
        print("No se pudo leer la imagen. Asegúrese de que el archivo sea una imagen válida.")
    else:
        coeficientes = calcular_coeficientes(imagen)
        imagen_reducida_ruido = reducir_ruido(imagen)
        imagen_interpolada = interpolar(imagen, coeficientes)
        imagen_enfocada_y_refinada = enfocar_y_refinar(imagen)
        # Guardar las imágenes procesadas
        cv2.imwrite('C:\\Users\\AUTONOMA\\Desktop\\imagen_reducida_ruido.jpg', imagen_reducida_ruido)
        cv2.imwrite('C:\\Users\\AUTONOMA\\Desktop\\imagen_interpolada.jpg', imagen_interpolada)
        cv2.imwrite('C:\\Users\\AUTONOMA\\Desktop\\imagen_enfocada_y_refinada.jpg', imagen_enfocada_y_refinada)
