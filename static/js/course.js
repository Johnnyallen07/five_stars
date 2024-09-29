
function loadMarkdown() {
    fetch('/static/markdown.md') // Assuming the markdown file is located in the static folder
        .then(response => response.text())
        .then(markdown => {
            const contentArea = document.getElementById('content-area');
            contentArea.innerHTML = marked.parse(markdown); // Parse markdown to HTML and insert it into content area
        })
        .catch(error => console.error('Error fetching markdown:', error));
}


// Function to display the selected video
function displayVideo(videoUrl, title) {
    const videoFrame = document.getElementById('video-frame');
    const videoTitle = document.getElementById('video-title');

    videoFrame.style.display = 'block';
    videoTitle.style.display = 'block';
    videoFrame.src = videoUrl;
    videoTitle.textContent = title;
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('information').addEventListener('click', function (event) {
        loadMarkdown();
    });
});
// Add JS to toggle visibility of subtopics
document.querySelectorAll('.topic-header').forEach(function (header) {
    header.addEventListener('click', function () {
        const topicId = this.id.split('-')[2];
        document.querySelectorAll(`.course-item[data-topic-id="${topicId}"]`).forEach(function (subtopic) {
            subtopic.style.display = (subtopic.style.display === 'none') ? 'block' : 'none';
        });
    });

});

// Function to handle click events on subtopics
document.querySelectorAll('.course-item').forEach(function (link) {
    link.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default link behavior
        const videoUrl = this.querySelector('h4').getAttribute('data-video');
        const videoTitle = this.textContent;
        displayVideo(videoUrl, videoTitle); // Display video and remove markdown
    });
});


document.querySelectorAll('.course-item').forEach(item => {
    item.addEventListener('mouseenter', () => {
        item.style.backgroundColor = '#f0f0f0';
        item.style.borderLeft = '5px solid #007bff';
    });

    item.addEventListener('mouseleave', () => {
        item.style.backgroundColor = '';
        item.style.borderLeft = '';
    });
});


// document.addEventListener('DOMContentLoaded', function () {
//     let markdownDisplayed = false; // To track if markdown has been loaded already
//
//     function loadMarkdown() {
//         fetch('/static/markdown.md') // Adjust the path if necessary
//             .then(response => {
//                 if (!response.ok) throw new Error('Network response was not ok');
//                 return response.text();
//             })
//             .then(markdown => {
//                 const contentArea = document.getElementById('content-area');
//                 contentArea.innerHTML = marked.parse(markdown); // Parse and insert markdown
//                 markdownDisplayed = true;
//             })
//             .catch(error => console.error('Error fetching markdown:', error));
//     }
//
//     // Handle click event for the "Information" link
//     document.getElementById('information').addEventListener('click', function () {
//         if (!markdownDisplayed) {
//             // Load markdown content when "Information" is clicked
//             loadMarkdown();
//         }
//         // Proceed with normal navigation after markdown is loaded or displayed
//     });
//
//     // Other event listeners remain unchanged
//     document.querySelectorAll('.topic-header').forEach(function (header) {
//         header.addEventListener('click', function () {
//             const topicId = this.id.split('-')[2];
//             document.querySelectorAll(`.course-item[data-topic-id="${topicId}"]`).forEach(function (subtopic) {
//                 subtopic.style.display = (subtopic.style.display === 'none') ? 'block' : 'none';
//             });
//         });
//     });
//
//     document.querySelectorAll('.course-item').forEach(function (link) {
//         link.addEventListener('click', function (event) {
//             event.preventDefault(); // Prevent default link behavior
//             const videoUrl = this.querySelector('h4').getAttribute('data-video');
//             const videoTitle = this.textContent;
//             displayVideo(videoUrl, videoTitle); // Display video content
//         });
//     });
//
//     document.querySelectorAll('.course-item').forEach(item => {
//         item.addEventListener('mouseenter', () => {
//             item.style.backgroundColor = '#f0f0f0';
//             item.style.borderLeft = '5px solid #007bff';
//         });
//
//         item.addEventListener('mouseleave', () => {
//             item.style.backgroundColor = '';
//             item.style.borderLeft = '';
//         });
//     });
// });
