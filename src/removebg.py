import cv2
import numpy as np

def adjust_threshold(image):
    # Convertir a gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral adaptativo
    thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)

    return thresholded

def adjust_kernel(image):
    # Ajustar el tamaño del kernel en función del tamaño de la imagen
    height, width = image.shape[:2]
    kernel_size = (width // 100, height // 100)
    kernel = np.ones(kernel_size, np.uint8)

    return kernel

def refine_mask(mask):
    # Aplica operaciones morfológicas adicionales para limpiar y refinar la máscara
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)

    return mask

def remove_background(image):
    # Ajustar el umbral
    thresholded = adjust_threshold(image)

    # Ajustar el tamaño del kernel
    kernel = adjust_kernel(image)

    # Aplicar morfología para limpiar puntos extraños
    cleaned = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

    # Obtener contornos externos
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encuentra el contorno más grande
    if contours:
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

        # Dibuja el contorno con relleno blanco sobre un fondo negro como máscara
        mask = np.zeros_like(thresholded)
        cv2.drawContours(mask, [biggest_contour], -1, (255), thickness=cv2.FILLED)

        # Refinar la máscara
        mask = refine_mask(mask)

        # Antialias la máscara
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        # Pon eso en el canal alfa de la imagen de entrada
        b, g, r = cv2.split(image)
        rgba = [b, g, r, mask]
        dst = cv2.merge(rgba, 4)

        return dst
    else:
        print("No se encontraron contornos en la imagen.")
        return image

# Ejemplo de uso de la función
if __name__ == '__main__':
    input_image_path = 'C:\\Users\\AUTONOMA\\Desktop\\input.jpg'
    output_image_path = 'C:\\Users\\AUTONOMA\\Desktop\\output.png'

    input_image = cv2.imread(input_image_path)
    if input_image is None:
        print("No se pudo cargar la imagen.")
    else:
        output_image = remove_background(input_image)
        cv2.imwrite(output_image_path, output_image)
        print("Fondo removido correctamente. Imagen guardada en:", output_image_path)
