function loadMarkdown() {
    fetch('/static/markdown.md') // Assuming the markdown file is located in the static folder
        .then(response => response.text())
        .then(markdown => {
            const contentArea = document.getElementById('content-area');
            contentArea.innerHTML = marked.parse(markdown); // Parse markdown to HTML and insert it into content area
        })
        .catch(error => console.error('Error fetching markdown:', error));
}

// Load the markdown file by default when the page loads
window.onload = function () {
    loadMarkdown(); // Display markdown on page load
};

// Function to display the selected video
function displayVideo(videoUrl, title) {
    const contentArea = document.getElementById('content-area');
    const videoFrame = document.getElementById('video-frame');
    const videoTitle = document.getElementById('video-title');

    // Clear the markdown content
    contentArea.innerHTML = '';

    // Display the selected video and title
    videoFrame.src = videoUrl;
    videoTitle.textContent = title;
}

// Handle click event for the description link
document.getElementById('description-link').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    loadMarkdown(); // Display markdown on link click
});
// Add JS to toggle visibility of subtopics
document.querySelectorAll('.topic-header').forEach(function (header) {
    header.addEventListener('click', function () {
        const subtopics = document.getElementById('subtopics-' + this.id.split('-')[2]);
        subtopics.style.display = (subtopics.style.display === 'block') ? 'none' : 'block';
    });
});

// Function to handle click events on subtopics
document.querySelectorAll('.subtopics a').forEach(function (link) {
    link.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default link behavior
        const videoUrl = this.getAttribute('data-video');
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


