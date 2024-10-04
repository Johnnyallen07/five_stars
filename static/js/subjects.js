function addSubject() {
    const container = document.getElementById('subjects-container');

    // Create a new subject input field
    const newField = document.createElement('div');
    newField.classList.add('subject-field');

    newField.innerHTML = `
                <input type="text" name="subject[]" placeholder="Enter subject">
            `;

    // Add the new field to the container
    container.appendChild(newField);

    // Show the remove button if there are at least two subject fields
    const subjectFields = document.querySelectorAll('.subject-field');
    if (subjectFields.length > 1) {
        document.getElementById('remove-btn').style.display = 'inline-block';
    }
}

function removeSubject() {
    const container = document.getElementById('subjects-container');
    const subjectFields = document.querySelectorAll('.subject-field');

    if (subjectFields.length > 1) {
        // Remove the last subject field
        container.removeChild(subjectFields[subjectFields.length - 1]);

        // Hide the remove button if there's only one field left
        if (subjectFields.length - 1 === 1) {
            document.getElementById('remove-btn').style.display = 'none';
        }
    }
}

