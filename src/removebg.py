import cv2
import numpy as np

def remove_background(image):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Encontrar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Crear una máscara para la imagen
    mask = np.zeros_like(image)

    # Rellenar los contornos encontrados en la máscara
    cv2.drawContours(mask, contours, -1, (255,255,255), thickness=cv2.FILLED)

    # Aplicar la máscara a la imagen
    result = cv2.bitwise_and(image, mask)

    return result