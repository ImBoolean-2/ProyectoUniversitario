document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData();
    var imageFile = document.getElementById('image-input').files[0];
    formData.append('image', imageFile);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    xhr.responseType = 'blob';

    // Muestra la barra de progreso y actualiza el ancho de la barra y el porcentaje de progreso
    document.getElementById('progress-container').style.display = 'block';
    xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
            var percentComplete = (e.loaded / e.total) * 100;
            document.getElementById('progress-bar').style.width = percentComplete + '%';
            document.getElementById('progress-percent').textContent = Math.round(percentComplete) + '%';
        }
    };

    // Cuando la imagen se ha cargado, oculta la barra de progreso y muestra la imagen
    xhr.onload = function() {
        if (this.status == 200) {
            document.getElementById('progress-container').style.display = 'none';
            var imageUrl = URL.createObjectURL(this.response);
            document.getElementById('result-image').src = imageUrl;
            document.getElementById('result-image').style.display = 'block';
        }
    };

    xhr.send(formData);
});