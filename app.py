from flask import Flask, request, send_file
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    # Aquí iría el código para procesar la imagen y aplicar la interpolación
    # Por ahora, solo vamos a devolver la misma imagen sin modificar
    image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    _, buffer = cv2.imencode('.png', image)
    return send_file(
        io.BytesIO(buffer),
        mimetype='image/png',
        as_attachment=True,
        attachment_filename='result.png'
    )

if __name__ == '__main__':
    app.run(debug=True)
