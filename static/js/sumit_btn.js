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

    let competitionInputs = document.querySelectorAll('input[name="competition[]"]');
    let competitions = [];

    competitionInputs.forEach(function (input) {
        if (input.value.trim()) {
            competitions.push(input.value.trim());
        }
    });

    let competitionsString = competitions.join(',');

    // Set the value to a hidden input field
    const subjectHiddenInput = document.getElementById('id_subjects');
    subjectHiddenInput.value = subjectsString;
    const competitionHiddenInput = document.getElementById('id_competitions');
    competitionHiddenInput.value = competitionsString;
    // console.log(competitionsString)

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

    // Convert the cropped canvas to data URL and set it to the hidden input
    const imageBlob = croppedCanvas.toDataURL('image/png');
    const imageInput = document.createElement('input');
    imageInput.type = 'hidden';
    imageInput.name = 'image'; // Set the name attribute for the form
    imageInput.id = 'image'; // Set the id for future reference
    document.getElementById('combined-form').appendChild(imageInput);
    imageInput.value = imageBlob;
    document.getElementById('combined-form').submit();
});
