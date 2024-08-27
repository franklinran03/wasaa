// Función para seguir a un usuario
/*function followUser(username) {
    fetch(`/follow/${username}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();  // Recargar la página
        } else {
            response.json().then(data => {
                console.error(data.error);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Función para dejar de seguir a un usuario
function unfollowUser(username) {
    fetch(`/unfollow/${username}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();  // Recargar la página
        } else {
            response.json().then(data => {
                console.error(data.error);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Asignar eventos a los botones de seguir y dejar de seguir
document.querySelectorAll('.follow-btn').forEach(button => {
    button.addEventListener('click', event => {
        event.preventDefault();
        const username = button.getAttribute('data-username');
        followUser(username);
    });
});

document.querySelectorAll('.unfollow-btn').forEach(button => {
    button.addEventListener('click', event => {
        event.preventDefault();
        const username = button.getAttribute('data-username');
        unfollowUser(username);
    });
});*/
// Obtener el token CSRF

// Función para manejar el seguimiento
function handleFollow(event) {
    event.preventDefault();
    const form = event.target;

    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        }
    })
    .then(response => {
        if (response.ok) {
            // Recargar la página después de seguir/dejar de seguir
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Asignar eventos a los formularios de seguir y dejar de seguir
document.getElementById('follow-form')?.addEventListener('submit', handleFollow);
document.getElementById('unfollow-form')?.addEventListener('submit', handleFollow);
