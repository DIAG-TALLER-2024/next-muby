function onLoad() {
    let messageInput = document.getElementById('message')
    let submitButton = document.getElementById('send-message')

    messageInput.addEventListener('input', (event) => {
        if (event.target.value.length > 0) {
            submitButton.classList.remove('disabled')
        } else {
            submitButton.classList.add('disabled')
        }
    })

    function addMessageToChat(message) {
        let messageHTML = ''

        if (message.author === 'assistant') {
            messageHTML = `
                <div class="d-flex flex-row justify-content-start mb-4">
                    <img class="bg-white" src="/static/muby.png" alt="avatar 1" style="width: 45px; height: 100%;">
                    <div class="p-3 ms-3" style="border-radius: 15px; background-color: rgba(57, 192, 237, .2);">
                        <p class="mb-0">${message.content}</p>
                    </div>
                </div>
            `;
        } else {
            messageHTML = `
                <div class="d-flex flex-row justify-content-end mb-4">
                    <div class="p-3 me-3 border bg-body-tertiary" style="border-radius: 15px;">
                        <p class="mb-0">${message.content}</p>
                    </div>
                </div>
            `
        }

        document.getElementById('messages').insertAdjacentHTML('beforeend', messageHTML)
    }

    document.addEventListener('submit', async (event) => {
        event.preventDefault()

        const form = event.target
        const formData = new FormData(form)

        submitButton.classList.add('disabled')
        messageInput.classList.add('disabled')
        submitButton.value = 'Enviando...'

        addMessageToChat({
            content: formData.get('message'),
            author: 'user',
        })

        messageInput.value = ''

        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
               'Accept': 'application/json',
            },
            body: formData,
        })

        const message = await response.json()
        addMessageToChat(message)
        messageInput.classList.remove('disabled')
        submitButton.value = 'Enviar'
    })
}

document.addEventListener('DOMContentLoaded', onLoad)
