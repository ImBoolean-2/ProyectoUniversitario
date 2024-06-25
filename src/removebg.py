import cv2
import numpy as np

def remove_background(image):
    """
    Remueve el fondo de una imagen utilizando el algoritmo de GrabCut.
    """
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Crear una máscara inicial con todos los píxeles marcados como "unknown"
    mask = np.zeros(image.shape[:2], np.uint8)
    mask[:] = cv2.GC_PR_BGD

    # Selecionar un rectángulo que contenga el objeto
    rect = (10, 10, image.shape[1] - 20, image.shape[0] - 20)

    # Inicializar el algoritmo de GrabCut
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # Refinar la máscara utilizando iteraciones de GrabCut
    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_EVAL)

    # Convertir la máscara a una imagen binaria
    mask_binary = np.where((mask == 2) | (mask == 0), 0, 255).astype(np.uint8)

    # Encontrar los componentes conectados en la máscara
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_binary)

    # Encontrar el componente más grande
    max_label = 0
    max_area = 0
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area > max_area:
            max_area = area
            max_label = i

    # Crear una máscara que solo contenga el objeto más grande
    mask_final = np.zeros(mask_binary.shape, np.uint8)
    mask_final[labels == max_label] = 255

    # Reemplazar el fondo con un color blanco
    result = image.copy()
    result[mask_final == 0] = (255, 255, 255)  # Asignar blanco a los píxeles de fondo

    return result, mask_final

def display_images(original, mask, result):
    """
    Muestra las imágenes de manera organizada.
    """
    cv2.imshow('Original', original)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_result(result, filename):
    """
    Guarda el resultado en un archivo.
    """
    cv2.imwrite(filename, result)

if __name__ == '__main__':
    img_path = 'C:\\Users\\AUTONOMA\\Downloads\\flor.jpg'
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: No se pudo cargar la imagen '{img_path}'")
        exit()

    result, mask = remove_background(img)
    display_images(img, mask, result)
    save_result(result, 'result.png')