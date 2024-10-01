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

document.getElementById('submit-btn').addEventListener('click', function () {
    // Manually dispatch the submit event to the form, which will trigger the attached event listeners
    let subjectInputs = document.querySelectorAll('input[name="subject[]"]');
    let subjects = [];

    subjectInputs.forEach(function (input) {
        if (input.value.trim()) {
            subjects.push(input.value.trim());
        }
    });
    // Join subjects into a comma-separated string
    let subjectsString = subjects.join(',');
    console.log('Subjects string:', subjectsString);
    // Set the value to a hidden input field or directly pass to the form submission
    const hiddenInput = document.getElementById('id_subjects');
    hiddenInput.value = subjectsString

    // Debugging step
    console.log('Hidden input value set:', document.getElementById('id_subjects').value);
    console.log(document.getElementById('first-name').value);

    document.getElementById('combined-form').submit();

});
