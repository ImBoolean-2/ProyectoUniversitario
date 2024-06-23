from flask import Flask, request, send_file, render_template
import numpy as np
import cv2
import io
from src.interpolacion import calcular_coeficientes, interpolar

app = Flask(__name__)

@app.route('/')
def index():
    # Renderiza la página de inicio con el formulario de carga
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file:
        try:
            imagen = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            coeficientes = calcular_coeficientes(imagen)
            imagen_interpolada = interpolar(imagen, coeficientes)

            _, buffer = cv2.imencode('.png', imagen_interpolada)
            return send_file(
                io.BytesIO(buffer),
                mimetype='image/png',
                as_attachment=True,
                download_name='imagen_interpolada.png'
            )
        except ValueError as e:
            return f"{str(e)}. Esta imagen no tiene los puntos de control suficientes para ser interpolada", 400 # Devuelve el mensaje de error con un código de estado HTTP 400
    else:
        return "No se proporcionó una imagen.", 400

if __name__ == '__main__':
    app.run(debug=True)
