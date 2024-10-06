const slots = existingSlots || [];
const ONE_WEEK_MS = 7 * 24 * 60 * 60 * 1000; // One week in milliseconds

// Check if two time slots overlap
function isOverlapping(newStart, newEnd) {
    for (const slot of slots) {
        const slotStart = new Date(slot.start);
        const slotEnd = new Date(slot.end);
        if (newStart < slotEnd && newEnd > slotStart) {
            return true;
        }
    }
    return false;
}

function deleteSlot(index) {
    slots.splice(index, 1);
    renderSlots();
}


const formatDateWithoutSeconds = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
};

function renderSlots() {
    const slotList = document.getElementById('slotList');
    slotList.innerHTML = '';

    console.log(slots)

    if (slots.length === 0) {
        slotList.innerHTML = '<li class="empty-message">No time slots available yet.</li>';
    } else {
        slots.forEach((slot, index) => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
    <div class="time-slot">
        <div class="slot-header">
            <span class="slot-label">Start Time:</span>
            <span class="slot-time">${formatDateWithoutSeconds(slot.start)}</span>
        </div>
        <div class="slot-header">
            <span class="slot-label">End Time:</span>
            <span class="slot-time">${formatDateWithoutSeconds(slot.end)}</span>
        </div>
        <button class="delete-btn" onclick="deleteSlot(${index})">Delete</button>
    </div>
  `;
            slotList.appendChild(listItem);
        });

    }
}

renderSlots();

document.getElementById('addSlotBtn').addEventListener('click', function (event) {
    event.preventDefault();

    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;

    if (!startTime || !endTime) {
        alert('Please fill both start and end times.');
        return;
    }

    const start = new Date(startTime);
    const end = new Date(endTime);

    if (start >= end) {
        alert('End time must be after start time.');
        return;
    }

    if (isOverlapping(start, end)) {
        alert('This time slot overlaps with an existing slot.');
        return;
    }

    // Restrict time slot length to one week
    if (end - start > ONE_WEEK_MS) {
        alert('The time slot cannot surpass one week.');
        return;
    }

    // Add the new slot
    slots.push({start: startTime, end: endTime});
    renderSlots();

    // Clear input fields
    document.getElementById('startTime').value = '';
    document.getElementById('endTime').value = '';
});

// Add event listener to submit the schedule
document.getElementById('scheduleForm').addEventListener('submit', function (event) {
    // Prevent the default form submission
    event.preventDefault();
    document.getElementById('slots').value = JSON.stringify(slots);

    // Submit the form
    this.submit();
});
