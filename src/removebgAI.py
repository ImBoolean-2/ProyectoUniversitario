from removebg import RemoveBg
from dotenv import load_dotenv
import os
import datetime
from PIL import Image

def remove_background(input_image_path, output_folder, api_key):
    rmbg = RemoveBg(api_key, "error.log")
    rmbg.remove_background_from_img_file(input_image_path)
    no_bg_image_path = input_image_path+"_no_bg.png"
    
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    base_name = os.path.basename(input_image_path)
    new_name = current_time + "_" + base_name
    
    output_path = os.path.join(output_folder, new_name)
    image = Image.open(no_bg_image_path)
    image.save(output_path)
    print("Eliminación de fondo de imagen completada. Imagen guardada en:", output_path)

# Cargar las variables de entorno del archivo .env
load_dotenv('ApiKEY.env')

# Uso de la función
api_key = os.getenv("API_KEY")
input_image_path = "C:\\Users\\Val\\Documents\\OIPtest.jpg"
output_folder = './resources/reescaladas_imgs/'
remove_background(input_image_path, output_folder, api_key)