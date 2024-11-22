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

const draggables = document.querySelectorAll('.draggable')
const containers = document.querySelectorAll('.container')

let first_card
let first_container
let flag = false

draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
        draggable.classList.add('dragging')
    }) 

    draggable.addEventListener('dragend', () => {
        draggable.classList.remove('dragging')
    })
})

containers.forEach(container => {
    container.addEventListener('dragover', e => {
        e.preventDefault()
        const draggable = document.querySelector('.dragging')
        if (draggable && draggable instanceof Node) {
            container.appendChild(draggable)
        if (first_card ===undefined){
            first_card = draggable.id
            first_container = container.id
            console.log("Primera vez")
        }
        
        if (first_card != draggable.id) {
            first_card = draggable.id
            flag = false
        } else {
            if (first_container != container.id && flag == false){
                //console.log(draggable.getAttribute('data-url') + 'cardlist/' + container.id + "/")
                fetchCard(draggable.getAttribute('data-url') + 'cardlist/' + container.id + "/")
                console.log("Cambió de contenedor")
                first_container = container.id
                flag = true
            }
        }
        flag = false
        console.log("Card ID", draggable.id)
        console.log("Card list ID", container.id)
    }})
})

function fetchCard(url){
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    location.reload();
}

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