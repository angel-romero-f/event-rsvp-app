const params = new URLSearchParams(window.location.search);
const eventId = params.get('id');

if (!eventId) {
    window.location.href = '/';
}

async function loadEvent() {
    const container = document.getElementById('event-container');

    try {
        const response = await fetch(`/api/events/${eventId}`);

        if (!response.ok) {
            container.innerHTML = '<p class="text-danger">Event not found.</p>';
            return;
        }

        const event = await response.json();
        renderEvent(event);

    } catch (error) {
        container.innerHTML = '<p class="text-danger">Failed to load event.</p>';
        console.error('Error loading event:', error);
    }
}

function renderEvent(event) {
    const container = document.getElementById('event-container');
    const date = new Date(event.date);
    const formattedDate = date.toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit'
    });

    let buttonHtml = '';
    if (event.current_user_rsvp === 'confirmed') {
        buttonHtml = '<button id="action-btn" class="btn btn-danger">Cancel RSVP</button>';
    } else if (event.spots_remaining > 0) {
        buttonHtml = '<button id="action-btn" class="btn btn-success">RSVP</button>';
    } else {
        buttonHtml = '<button class="btn btn-secondary" disabled>Event Full</button>';
    }

    const attendeesList = event.attendees.length > 0
        ? event.attendees.map(a => `<li class="list-group-item">${a.name}</li>`).join('')
        : '<li class="list-group-item text-muted">No attendees yet</li>';

    container.innerHTML = `
        <div class="row">
            <div class="col-lg-8">
                <h2>${event.title}</h2>
                <p class="text-muted mb-4">${formattedDate} • ${event.location}</p>
                <p>${event.description}</p>

                <div class="mt-4">
                    <h5>Capacity</h5>
                    <p>${event.capacity - event.spots_remaining} / ${event.capacity} spots filled</p>
                    <div class="progress mb-3">
                        <div class="progress-bar ${event.spots_remaining === 0 ? 'bg-danger' : 'bg-primary'}"
                             style="width: ${((event.capacity - event.spots_remaining) / event.capacity) * 100}%">
                        </div>
                    </div>
                </div>

                <div class="mt-4">
                    ${buttonHtml}
                </div>
            </div>

            <div class="col-lg-4 mt-4 mt-lg-0">
                <h5>Attendees (${event.attendees.length})</h5>
                <ul class="list-group">
                    ${attendeesList}
                </ul>
            </div>
        </div>
    `;

    const actionBtn = document.getElementById('action-btn');
    if (actionBtn) {
        actionBtn.addEventListener('click', handleAction);
    }
}

async function handleAction() {
    const actionBtn = document.getElementById('action-btn');
    const originalText = actionBtn.textContent;
    actionBtn.disabled = true;
    actionBtn.textContent = 'Loading...';

    try {
        const response = await fetch(`/api/events/${eventId}/${originalText === 'RSVP' ? 'rsvp' : 'cancel'}`, {
            method: 'POST'
        });

        if (!response.ok) {
            const error = await response.json();
            alert(error.error || 'Something went wrong');
            actionBtn.disabled = false;
            actionBtn.textContent = originalText;
            return;
        }

        const event = await response.json();
        renderEvent(event);

    } catch (error) {
        alert('Failed to process request');
        actionBtn.disabled = false;
        actionBtn.textContent = originalText;
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadEvent);
