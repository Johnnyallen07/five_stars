// let scale = 1;
// let translateX = 0;
// let translateY = 0;
// let isDragging = false;
// let startX, startY;
// let img = new Image();
// let imgWidth, imgHeight;
// const imageContainer = document.querySelector('.image-container');
// const preview = document.getElementById('photoPreview');
//
// // Function to initialize transform properties
// function initializeTransforms() {
//     scale = 1;
//     translateX = 0;
//     translateY = 0;
//     updateImageTransform();
// }
//
//
// window.onload = function () {
//     const dataImageUrl = preview.getAttribute('data-image-url');
//     preview.src = dataImageUrl;
//     img.src = dataImageUrl;
// };
//
// // Image preview on file upload
// function previewImage() {
//     const input = document.getElementById('photoInput');
//
//     if (input.files && input.files[0]) {
//         const reader = new FileReader();
//         reader.onload = function (e) {
//             preview.src = e.target.result;
//             preview.style.display = 'block';
//
//             img.onload = function () {
//                 imgWidth = img.width;
//                 imgHeight = img.height;
//                 initializeTransforms(); // Reset transforms
//             };
//             img.src = e.target.result;
//         };
//         reader.readAsDataURL(input.files[0]);
//     }
// }
//
// // Zoom image with scroll for both canvas and preview
// imageContainer.addEventListener('wheel', function (e) {
//     e.preventDefault();
//     if (e.deltaY < 0) {
//         scale = Math.min(scale + 0.05, 3); // Max zoom level 3x
//     } else {
//         scale = Math.max(scale - 0.05, 0.05); // Min zoom level 0.05x
//     }
//     updateImageTransform();
// });
//
// // Update the image position and zoom for preview and canvas
// function updateImageTransform() {
//     preview.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
// }
//
// // Start dragging on image container
// imageContainer.addEventListener('mousedown', function (e) {
//     isDragging = true;
//     startX = e.clientX;
//     startY = e.clientY;
//     preview.style.cursor = 'grabbing';
// });
//
// imageContainer.addEventListener('mousemove', function (e) {
//     if (isDragging) {
//         let dx = e.clientX - startX;
//         let dy = e.clientY - startY;
//         translateX += dx;
//         translateY += dy;
//         startX = e.clientX;
//         startY = e.clientY;
//         updateImageTransform();
//     }
// });
//
// // Stop dragging
// document.addEventListener('mouseup', function () {
//     isDragging = false;
//     preview.style.cursor = 'grab';
// });
//
// // Capture the image inside the container and download it

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

// Set img.onload function outside previewImage()
img.onload = function () {
    imgWidth = img.width;
    imgHeight = img.height;
    initializeTransforms(); // Reset transforms
};

window.onload = function () {
    const dataImageUrl = preview.getAttribute('data-image-url');
    preview.src = dataImageUrl;
    img.src = dataImageUrl; // This will trigger img.onload
};

// Image preview on file upload
function previewImage() {
    const input = document.getElementById('photoInput');

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            img.src = e.target.result; // img.onload will be called
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
        scale = Math.max(scale - 0.05, 0.05); // Min zoom level 0.05x
    }
    updateImageTransform();
});

// Update the image position and zoom
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

// Function to capture the image (ensure this function exists and is called appropriately)
function captureImage() {
    // Your existing code to capture and process the image
}
