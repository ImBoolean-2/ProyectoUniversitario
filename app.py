from flask import Flask, request, render_template
from src.interpolacion import interpolar_imagen

app = Flask(__name__)

@app.route('/')
def index():
    # Renderiza la página de inicio con el formulario de carga
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file:
        print("Imagen cargada")
        puntos_de_control = [(0, 0), (255, 255)] # Ejemplo simple
        return interpolar_imagen(file, puntos_de_control)
    else:
        return "No se ha cargado ninguna imagen", 400

if __name__ == '__main__':
    app.run(debug=True)
