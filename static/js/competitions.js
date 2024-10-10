function addCompetition() {
    const container = document.getElementById('competitions-container');

    // Create a new subject input field
    const newField = document.createElement('div');
    newField.classList.add('competition-field');

    newField.innerHTML = `
                <input type="text" name="competition[]" placeholder="Enter Competition">
            `;

    // Add the new field to the container
    container.appendChild(newField);

    // Show the remove button if there are at least two subject fields
    const competitionFields = document.querySelectorAll('.competition-field');
    if (competitionFields.length > 1) {
        document.getElementById('competition-remove-btn').style.display = 'inline-block';
    }
}

function removeCompetition() {
    const container = document.getElementById('competitions-container');
    const competitionFields = document.querySelectorAll('.competition-field');

    if (competitionFields.length > 1) {
        // Remove the last subject field
        container.removeChild(competitionFields[competitionFields.length - 1]);

        // Hide the remove button if there's only one field left
        if (competitionFields.length - 1 === 1) {
            document.getElementById('competition-remove-btn').style.display = 'none';
        }
    }
}

