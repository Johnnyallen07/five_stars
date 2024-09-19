let scale = 1;
let translateX = 0;
let translateY = 0;
let isDragging = false;
let startX, startY;

const imageContainer = document.querySelector('.image-container');
const preview = document.getElementById('photoPreview');

// Image preview on file upload
function previewImage() {
    const input = document.getElementById('photoInput');

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Zoom image with scroll
imageContainer.addEventListener('wheel', function (e) {
    e.preventDefault();
    if (e.deltaY < 0) {
        scale = Math.min(scale + 0.05, 3); // Max zoom level 3x
    } else {
        scale = Math.max(scale - 0.05, 0.05); // Min zoom level 1x
    }
    updateImageTransform();
});

// Start dragging on mouse down
imageContainer.addEventListener('mousedown', function (e) {
    isDragging = true;
    startX = e.clientX - translateX;
    startY = e.clientY - translateY;
    preview.style.cursor = 'grabbing';
});

// Update dragging as long as mouse is pressed and moved
imageContainer.addEventListener('mousemove', function (e) {
    if (isDragging) {
        translateX = e.clientX - startX;
        translateY = e.clientY - startY;
        console.log(translateX)
        updateImageTransform();
    }
});

// Stop dragging on mouse up
document.addEventListener('mouseup', function () {
    isDragging = false;
    preview.style.cursor = 'grab';
});

// Update the image position and zoom
function updateImageTransform() {
    preview.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
}