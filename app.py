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
        # Convierte la imagen cargada en un array de NumPy
        imagen = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        
        # Aquí deberías definir tus puntos de control para la interpolación
        puntos_de_control = [(0, 0), (255, 255)] # Ejemplo simple
        
        # Calcula los coeficientes de interpolación
        coeficientes = calcular_coeficientes(puntos_de_control)
        
        # Aplica la interpolación a la imagen
        imagen_interpolada = interpolar(imagen, coeficientes)
        
        # Convierte la imagen interpolada de vuelta a un formato que se pueda enviar
        _, buffer = cv2.imencode('.png', imagen_interpolada)
        return send_file(
            io.BytesIO(buffer),
            mimetype='image/png',
            as_attachment=True,
            download_name='imagen_interpolada.png'
        )
    else:
        return "No se ha cargado ninguna imagen", 400

if __name__ == '__main__':
    app.run(debug=True)
