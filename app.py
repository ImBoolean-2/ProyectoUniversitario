import os
from src.interpolacion import calcular_coeficientes, interpolar
from flask import Flask, request, render_template, url_for
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    # Renderiza la página de inicio con el formulario de carga
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file:
        # Genera un nombre de archivo basado en la fecha y hora actual
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = secure_filename(f"{timestamp}_{file.filename}")
        
        # Define la ruta de la carpeta donde se guardarán las imágenes
        folder_path = os.path.join(app.root_path, 'static/images')
        
        # Crea la carpeta si no existe
        os.makedirs(folder_path, exist_ok=True)
        
        # Guarda la imagen en la carpeta especificada
        file.save(os.path.join(folder_path, filename))
        
        # Envía la ruta de la imagen al template HTML
        return render_template('index.html', 
                               uploaded_image_url=url_for('static', filename=f'images/{filename}'))
    else:
        return "No se ha cargado ninguna imagen", 400

if __name__ == '__main__':
    app.run(debug=True)