from flask import Flask, send_file, render_template, request
from src.interpolacion import calcular_coeficientes, interpolar
from numpy import frombuffer, uint8
from cv2 import imdecode, imencode, IMREAD_UNCHANGED
from io import BytesIO

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
            return "Por favor, suba la imagen en un formato soportado. Los formatos .gif y de video no son admitidos.", 402 # Verificar el tipo MIME para bloquear .gif y formatos de video
        try:
            imagen = imdecode(frombuffer(file.read(), uint8), IMREAD_UNCHANGED)
            coeficientes = calcular_coeficientes(imagen)
            imagen_interpolada = interpolar(imagen, coeficientes)

            _, buffer = imencode('.png', imagen_interpolada)
            return send_file(
                BytesIO(buffer),
                mimetype='image/png',
                as_attachment=True,
                download_name='imagen_interpolada.png'
            )
        except ValueError as e:
            return f"{str(e)}. Esta imagen no tiene los puntos de control suficientes para ser interpolada", 401
    else:
        return "No se proporcionó una imagen.", 400

if __name__ == '__main__':
    app.run(debug=True)
