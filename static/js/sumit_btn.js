document.getElementById('submit-btn').addEventListener('click', function () {
    // Collect subjects and set the hidden input value
    let subjectInputs = document.querySelectorAll('input[name="subject[]"]');
    let subjects = [];

    subjectInputs.forEach(function (input) {
        if (input.value.trim()) {
            subjects.push(input.value.trim());
        }
    });

    // Join subjects into a comma-separated string
    let subjectsString = subjects.join(',');

    // Set the value to a hidden input field
    const hiddenInput = document.getElementById('id_subjects');
    hiddenInput.value = subjectsString;

    // Capture the image from the container using canvas
    const imageContainer = document.querySelector('.image-container');
    const preview = document.getElementById('photoPreview'); // Image element

    // Create a canvas element for capturing the image
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size to match the container's size
    canvas.width = imageContainer.clientWidth;
    canvas.height = imageContainer.clientHeight;

    // Apply the current transformations to the canvas context (scale and translate)
    ctx.translate(translateX + (canvas.width / 2), translateY + (canvas.height / 2)); // Translate first
    ctx.scale(scale, scale); // Apply scaling
    ctx.translate(-(imgWidth / 2), -(imgHeight / 2)); // Adjust the position for scaling

    // Draw the image on the canvas with the applied transformations
    ctx.drawImage(preview, 0, 0, imgWidth, imgHeight);

    // Now we crop the circular portion
    const cropWidth = 100; // Diameter of the circle
    const cropHeight = 100;
    const cropX = (canvas.width - cropWidth) / 2;
    const cropY = (canvas.height - cropHeight) / 2;

    // Create another canvas for the circular crop
    const croppedCanvas = document.createElement('canvas');
    croppedCanvas.width = cropWidth;
    croppedCanvas.height = cropHeight;
    const croppedCtx = croppedCanvas.getContext('2d');

    // Clip the context to a circle
    croppedCtx.beginPath();
    croppedCtx.arc(cropWidth / 2, cropHeight / 2, cropWidth / 2, 0, Math.PI * 2);
    croppedCtx.clip();

    // Draw the cropped image area
    croppedCtx.drawImage(canvas, cropX, cropY, cropWidth, cropHeight, 0, 0, cropWidth, cropHeight);

    // Convert the cropped canvas to a Blob and append it to the form data
    croppedCanvas.toBlob(function (blob) {
        // Create a new FormData object to hold form data
        let formData = new FormData(document.getElementById('combined-form'));

        // Append the image blob to the form data
        formData.append('image', blob, 'profile-image.png');

        // Submit the form via AJAX
        const xhr = new XMLHttpRequest();
        xhr.open('POST', window.location.href, true);
        xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);
        xhr.onload = function () {
            if (xhr.status === 200) {
                // Handle success
                console.log('Form submitted successfully.');
            } else {
                // Handle error
                console.log('Error submitting the form.');
            }
        };
        xhr.send(formData);
    }, 'image/png');
});
