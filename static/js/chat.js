function onLoad() {
    console.log('onLoad')

    let messageInput = document.getElementById('message')
    let submitButton = document.getElementById('send-message')

    messageInput.addEventListener('input', (event) => {
        if (event.target.value.length > 0) {
            submitButton.classList.remove('disabled')
        } else {
            submitButton.classList.add('disabled')
        }
    })
}

document.addEventListener('DOMContentLoaded', onLoad)
