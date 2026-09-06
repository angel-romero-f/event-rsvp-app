async function loadEvents() {
    const container = document.getElementById('events-container');

    try {
        const response = await fetch('/api/events');
        const events = await response.json();

        if (events.length === 0) {
            container.innerHTML = '<div class="col-12"><p class="text-muted">No events available.</p></div>';
            return;
        }

        container.innerHTML = events.map(event => {
            const date = new Date(event.date);
            const formattedDate = date.toLocaleDateString('en-US', {
                weekday: 'short',
                month: 'short',
                day: 'numeric',
                year: 'numeric',
                hour: 'numeric',
                minute: '2-digit'
            });

            let badgeClass = 'bg-success';
            let badgeText = `${event.spots_remaining} spots left`;

            if (event.spots_remaining === 0) {
                badgeClass = 'bg-danger';
                badgeText = 'Full';
            } else if (event.spots_remaining <= 5) {
                badgeClass = 'bg-warning text-dark';
            }

            const rsvpBadge = event.current_user_rsvp === 'confirmed'
                ? '<span class="badge bg-primary">RSVPd</span>'
                : '';

            return `
                <div class="col-md-6 col-lg-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start">
                                <h5 class="card-title">${event.title}</h5>
                                ${rsvpBadge}
                            </div>
                            <p class="card-text text-muted mb-2">
                                <small>${formattedDate}</small>
                            </p>
                            <p class="card-text text-muted mb-3">
                                <small>${event.location}</small>
                            </p>
                            <span class="badge ${badgeClass}">${badgeText}</span>
                        </div>
                        <div class="card-footer bg-transparent">
                            <a href="/event.html?id=${event.id}" class="btn btn-primary btn-sm w-100">View Details</a>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        container.innerHTML = '<div class="col-12"><p class="text-danger">Failed to load events.</p></div>';
        console.error('Error loading events:', error);
    }
}

async function loadCurrentUser() {
    const response = await fetch('/api/me');
    const user = await response.json();
    document.getElementById('user-name').textContent = user.name;
}

document.addEventListener('DOMContentLoaded', () => {
    loadCurrentUser();
    loadEvents();
});
