// Seleccionar los elementos arrastrables y los contenedores

document.addEventListener("DOMContentLoaded", () => {
    const draggables = document.querySelectorAll('.draggable');
    const containers = document.querySelectorAll('.container');
    let first_container;
    let last_container;

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', () => {
            draggable.classList.add('dragging');
        });

        draggable.addEventListener('dragend', () => {
            draggable.classList.remove('dragging');
        });
    });

    containers.forEach(container => {

        container.addEventListener('click', function(event) {
            const tarjeta = event.target.closest('.clickable'); 
            if (tarjeta) {
                const url = tarjeta.dataset.urlTest;
                window.location.href = url
            }
          });
            
        container.addEventListener('dragover', e => {
            e.preventDefault();

            const draggable = document.querySelector('.dragging');

            if (draggable) {
                /*
                container.appendChild(draggable);
                
                const cardId = draggable.id;
                const cardlistId = container.id;
                console.log(cardId);
                console.log(cardlistId);
                const url = `/update_card_position/${cardId}/cardlist/${cardlistId}/`;
                
                
                // Enviar la solicitud al servidor
                
                fetch(url, {
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
                });*/
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