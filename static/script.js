document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var formData = new FormData();
    var imageFile = document.getElementById('image-input').files[0];
    formData.append('image', imageFile);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
        } else {
            if (data.interpolated_image_url) {
                document.getElementById('interpolated-image').src = data.interpolated_image_url;
                document.getElementById('interpolated-image').hidden = false;
            }
            if (data.noise_reduced_image_url) {
                document.getElementById('noise-reduced-image').src = data.noise_reduced_image_url;
                document.getElementById('noise-reduced-image').hidden = false;
            }
            if (data.focused_image_url) {
                document.getElementById('focused-image').src = data.focused_image_url;
                document.getElementById('focused-image').hidden = false;
            }
            if (data.rescaled_image_url) {
                document.getElementById('rescaled-image').src = data.rescaled_image_url;
                document.getElementById('rescaled-image').hidden = false;
            }
            if (data.remove_background_image_url) {
                document.getElementById('remove-background-image').src = data.remove_background_image_url;
                document.getElementById('remove-background-image').hidden = false;
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
