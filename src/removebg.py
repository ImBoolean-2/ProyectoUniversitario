import cv2
import numpy as np

def adjust_threshold(image, threshold_value, tolerance):
    # Convertir a gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral manual con tolerancia
    _, thresholded = cv2.threshold(gray, threshold_value - tolerance, threshold_value + tolerance, cv2.THRESH_BINARY)

    return thresholded

def adjust_kernel(image):
    # Ajustar el tamaño del kernel en función del tamaño de la imagen y la cantidad de ruido
    noise_level = np.var(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    kernel_size = int(min(image.shape) / 50 * noise_level / 100)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    return kernel

def remove_background(image_path, output_path):
    # Leer la entrada
    img = cv2.imread(image_path)

    # Verificar si la imagen se cargó correctamente
    if img is None:
        print("No se pudo cargar la imagen")
        return

    # Ajustar el umbral
    thresholded = adjust_threshold(img, 85, 20)

    # Ajustar el tamaño del kernel
    kernel = adjust_kernel(img)

    # Aplicar morfología para limpiar puntos extraños
    cleaned = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)

    # Obtener contornos externos
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encuentra el contorno más grande
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

    # Dibuja el contorno con relleno blanco sobre un fondo negro como máscara
    mask = np.zeros_like(thresholded)
    cv2.drawContours(mask, [biggest_contour], -1, (255), thickness=cv2.FILLED)

    # Antialias la máscara
    mask = cv2.GaussianBlur(mask, (5,5), 0)

    # Pon eso en el canal alfa de la imagen de entrada
    b, g, r = cv2.split(img)
    rgba = [b,g,r, mask]
    dst = cv2.merge(rgba, 4)

    # Guardar el resultado
    cv2.imwrite(output_path, dst)


# Uso de la función
remove_background('C:\\Users\\AUTONOMA\\Desktop\\input.jpg', 'C:\\Users\\AUTONOMA\\Desktop\\output.png')