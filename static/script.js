document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var formData = new FormData();
    var imageFile = document.getElementById('image-input').files[0];
    formData.append('image', imageFile);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(imageBlob => {
        var imageUrl = URL.createObjectURL(imageBlob);
        document.getElementById('result-image').src = imageUrl;
        document.getElementById('result-image').hidden = false;
    });
});
