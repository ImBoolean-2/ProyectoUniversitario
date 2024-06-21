import os
import datetime
from numpy import array
from cv2 import imread, resize, INTER_AREA, normalize, medianBlur, cvtColor, COLOR_BGR2RGB, NORM_MINMAX, CV_8U
from PIL import Image, ImageFilter

image_path = 'C:\\Users\\Val\\Documents\\OIPtest.jpg'

image = imread(image_path)

height, width = image.shape[:2]
new_height = 1080
new_width = int(new_height * width / height)
image = resize(image, (new_width, new_height), interpolation = INTER_AREA)


for _ in range(5):
    image = normalize(image, None, 0, 255, NORM_MINMAX, CV_8U)
    image = medianBlur(image, 3)
    image = cvtColor(image, COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    pil_image = pil_image.filter(ImageFilter.SHARPEN)
    image = array(pil_image)

current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
base_name = os.path.basename(image_path)
new_name = current_time + "_" + base_name

output_folder = './resources/reescaladas_imgs/'
output_path = os.path.join(output_folder, new_name)

pil_image = Image.fromarray(image)
pil_image.save(output_path)
print("Reescalado de imagen completado. Imagen guardada en:", output_path)