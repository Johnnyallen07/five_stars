let scale = 1;
let translateX = 0;
let translateY = 0;
let isDragging = false;
let startX, startY;
let img = new Image();
let imgWidth, imgHeight;
const imageContainer = document.querySelector('.image-container');
const preview = document.getElementById('photoPreview');

// Function to initialize transform properties
function initializeTransforms() {
    scale = 1;
    translateX = 0;
    translateY = 0;
    updateImageTransform();
}

// Image preview on file upload
function previewImage() {
    const input = document.getElementById('photoInput');

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';

            img.onload = function () {
                imgWidth = img.width;
                imgHeight = img.height;
                initializeTransforms(); // Reset transforms
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    } else {
        // When no new image is selected, ensure the original image from the database is used
        if (preview.src === "") {
            preview.src = preview.getAttribute('data-image-url');
        }
    }
}

// Zoom image with scroll for both canvas and preview
imageContainer.addEventListener('wheel', function (e) {
    e.preventDefault();
    if (e.deltaY < 0) {
        scale = Math.min(scale + 0.05, 3); // Max zoom level 3x
    } else {
        scale = Math.max(scale - 0.05, 0.05); // Min zoom level 0.05x
    }
    updateImageTransform();
});

// Update the image position and zoom for preview and canvas
function updateImageTransform() {
    preview.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
}

// Start dragging on image container
imageContainer.addEventListener('mousedown', function (e) {
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    preview.style.cursor = 'grabbing';
});

imageContainer.addEventListener('mousemove', function (e) {
    if (isDragging) {
        let dx = e.clientX - startX;
        let dy = e.clientY - startY;
        translateX += dx;
        translateY += dy;
        startX = e.clientX;
        startY = e.clientY;
        updateImageTransform();
    }
});

// Stop dragging
document.addEventListener('mouseup', function () {
    isDragging = false;
    preview.style.cursor = 'grab';
});

// Capture the image inside the container and download it
