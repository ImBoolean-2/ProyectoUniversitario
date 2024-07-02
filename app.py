from flask import Flask, render_template, request, jsonify
from src.interpolacion import calcular_coeficientes, interpolar, reducir_ruido, enfocar_y_refinar
from src.reescalar_img import reescalar_img
from src.removebg import remove_background
from numpy import frombuffer, uint8
from cv2 import imdecode, imencode, IMREAD_UNCHANGED
from io import BytesIO
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file:
        content_type = file.content_type
        if content_type == 'image/gif' or content_type.startswith('video/'):
            return jsonify(
                error="Por favor, suba la imagen en un formato soportado. Los formatos .gif y de video no son admitidos."), 415

        try:
            image_data = file.read()
            print("Image data read successfully")
            imagen = imdecode(frombuffer(image_data, uint8), IMREAD_UNCHANGED)
            print("Image decoded successfully")

            if imagen is None:
                return jsonify(
                    error="No se pudo leer la imagen. Asegúrese de que el archivo sea una imagen válida."), 400

            coeficientes = calcular_coeficientes(imagen)
            print("Coeficientes calculated successfully")
            imagen_interpolada = interpolar(imagen, coeficientes)
            print("Image interpolated successfully")
            imagen_reducida_ruido = reducir_ruido(imagen)
            print("Noise reduced successfully")
            imagen_enfocada_y_refinada = enfocar_y_refinar(imagen)
            print("Image focused and refined successfully")

            _, buffer_interpolada = imencode('.png', imagen_interpolada)
            _, buffer_reducida = imencode('.png', imagen_reducida_ruido)
            _, buffer_refinada = imencode('.png', imagen_enfocada_y_refinada)

            interpolated_image_url = 'data:image/png;base64,' + base64.b64encode(buffer_interpolada).decode('utf-8')
            noise_reduced_image_url = 'data:image/png;base64,' + base64.b64encode(buffer_reducida).decode('utf-8')
            focused_image_url = 'data:image/png;base64,' + base64.b64encode(buffer_refinada).decode('utf-8')

            original_image_path = './resources/original_image.png'
            with open(original_image_path, 'wb') as f:
                f.write(image_data)
            print("Original image saved successfully")

            reescalada_image = reescalar_img(original_image_path)
            reescalada_buffer = BytesIO()
            reescalada_image.save(reescalada_buffer, format='PNG')
            reescalada_image_url = 'data:image/png;base64,' + base64.b64encode(reescalada_buffer.getvalue()).decode('utf-8')

            # Eliminar el fondo
            imagen_sin_fondo = remove_background(imagen)
            _, buffer_sin_fondo = imencode('.png', imagen_sin_fondo)
            remove_background_image_url = 'data:image/png;base64,' + base64.b64encode(buffer_sin_fondo).decode('utf-8')

            return jsonify({
                'interpolated_image_url': interpolated_image_url,
                'noise_reduced_image_url': noise_reduced_image_url,
                'focused_image_url': focused_image_url,
                'rescaled_image_url': reescalada_image_url,
                'remove_background_image_url': remove_background_image_url
            })

        except ValueError as e:
            return jsonify(
                error=f"{str(e)}. Esta imagen no tiene los puntos de control suficientes para ser interpolada."), 422
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify(error=f"Se produjo un error al procesar la imagen: {str(e)}"), 500
    else:
        return jsonify(error="No se proporcionó una imagen."), 400

if __name__ == '__main__':
    if not os.path.exists('./resources'):
        os.makedirs('./resources')
    app.run(debug=True)
