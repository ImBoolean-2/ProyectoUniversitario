from flask import Flask, render_template, request, jsonify
from src.interpolacion import calcular_coeficientes, interpolar, reducir_ruido, enfocar_y_refinar
from numpy import frombuffer, uint8
from cv2 import imdecode, imencode, IMREAD_UNCHANGED
from io import BytesIO
import base64

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
            imagen = imdecode(frombuffer(image_data, uint8), IMREAD_UNCHANGED)

            if imagen is None:
                return jsonify(
                    error="No se pudo leer la imagen. Asegúrese de que el archivo sea una imagen válida."), 400

            coeficientes = calcular_coeficientes(imagen)
            imagen_interpolada = interpolar(imagen, coeficientes)
            imagen_reducida_ruido = reducir_ruido(imagen)
            imagen_enfocada_y_refinada = enfocar_y_refinar(imagen)

            _, buffer_interpolada = imencode('.png', imagen_interpolada)
            _, buffer_reducida = imencode('.png', imagen_reducida_ruido)
            _, buffer_refinada = imencode('.png', imagen_enfocada_y_refinada)

            interpolated_image_url = 'data:image/png;base64,' + base64.b64encode(buffer_interpolada).decode('utf-8')
            noise_reduced_image_url = 'data:image/png;base64,' + base64.b64encode(buffer_reducida).decode('utf-8')
            focused_image_url = 'data:image/png;base64,' + base64.b64encode(buffer_refinada).decode('utf-8')

            return jsonify({
                'interpolated_image_url': interpolated_image_url,
                'noise_reduced_image_url': noise_reduced_image_url,
                'focused_image_url': focused_image_url
            })

        except ValueError as e:
            return jsonify(
                error=f"{str(e)}. Esta imagen no tiene los puntos de control suficientes para ser interpolada."), 422
        except Exception as e:
            return jsonify(error=f"Se produjo un error al procesar la imagen: {str(e)}"), 500
    else:
        return jsonify(error="No se proporcionó una imagen."), 400


if __name__ == '__main__':
    app.run(debug=True)
