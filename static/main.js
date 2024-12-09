/*let newX = 0, newY = 0, startX = 0, startY = 0;

const card = document.getElementById('card')

card.addEventListener('mousedown', mouseDown)

function mouseDown(e){
    startX = e.clientX
    startY = e.clientY

    document.addEventListener('mousemove', mouseMove)
    document.addEventListener('mouseup', mouseUp)
}

function mouseMove(e){
    newX = startX - e.clientX
    newY = startY - e.clientY

    startX = e.clientX
    startY = e.clientY

    card.style = startY + 'px'
    card.style = startX + 'px'

    console.log({newX, newY})
    console.log({startX, startY})
}

function mouseUp(e){
    document.removeEventListener('mousemove', mouseMove)
}*/

// Seleccionar los elementos arrastrables y los contenedores

document.addEventListener("DOMContentLoaded", () => {
    const draggables = document.querySelectorAll('.draggable');
    const containers = document.querySelectorAll('.container');

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', () => {
            draggable.classList.add('dragging');
        });

        draggable.addEventListener('dragend', () => {
            draggable.classList.remove('dragging');
        });
    });

    containers.forEach(container => {
        container.addEventListener('dragover', e => {
            e.preventDefault();
            const draggable = document.querySelector('.dragging');
            if (draggable) {
                container.appendChild(draggable);

                const cardId = draggable.id;
                const cardlistId = container.id;

                const url = `/update_card_position/${cardId}/cardlist/${cardlistId}/`;

                // Enviar la solicitud al servidor
                fetch(`/update_card_position/${cardId}/cardlist/${containerId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to update card position');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Card position updated successfully:', data);
                })
                .catch(error => {
                    console.error('Error updating card position:', error);
                });
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
