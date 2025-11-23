document.addEventListener('DOMContentLoaded', async () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const imageButton = document.getElementById('image-button');
    const audioButton = document.getElementById('audio-button');
    const imageInput = document.getElementById('image-input');
    const audioInput = document.getElementById('audio-input');
    const chatBox = document.getElementById('chat-box');
    const mainAvatar = document.getElementById('main-avatar');

    // Génère ou récupère un userId unique pour la session
    let userId = localStorage.getItem('userId');
    if (!userId) {
        userId = 'user_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('userId', userId);
    }

    let uploadedImageUrl = null;
    let uploadedAudioUrl = null;
    let jennyProfileImage = null;

    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');
    const closeBtn = document.getElementsByClassName('close')[0];

    // Récupérer l'image de profil de Jenny
    try {
        const response = await fetch('/profile_image');
        const data = await response.json();
        if (data.url) {
            jennyProfileImage = data.url;
            mainAvatar.src = data.url;
        }
    } catch (error) {
        console.error('Erreur récupération image profil:', error);
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    imageButton.addEventListener('click', () => {
        imageInput.click();
    });

    audioButton.addEventListener('click', () => {
        audioInput.click();
    });

    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            uploadFile(file, 'image');
        }
    });

    audioInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            uploadFile(file, 'audio');
        }
    });

    function uploadFile(file, type) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('type', type);

        fetch('/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                if (type === 'image') {
                    uploadedImageUrl = data.url;
                    addMessageToChatBox('user', '', data.url); // Afficher l'image uploadée
                } else if (type === 'audio') {
                    uploadedAudioUrl = data.url;
                    addMessageToChatBox('user', '', null, data.url); // Pour audio, modifier addMessageToChatBox
                }
            } else if (data.error) {
                addMessageToChatBox('bot', `Erreur upload : ${data.error}`);
            }
        })
        .catch((error) => {
            console.error('Erreur upload:', error);
            addMessageToChatBox('bot', 'Erreur lors de l\'upload.');
        });
    }

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message === '' && !uploadedImageUrl && !uploadedAudioUrl) return;

        // Afficher le message texte si présent
        if (message) {
            addMessageToChatBox('user', message);
        }

        // Ajouter un indicateur de frappe pour Jenny
        const typingMessage = addTypingIndicator();

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                userId: userId,
                message: message,
                image_url: uploadedImageUrl,
                audio_url: uploadedAudioUrl
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Supprimer l'indicateur de frappe
            removeTypingIndicator(typingMessage);
            if (data.response) {
                addMessageToChatBox('bot', data.response, data.image_url);
            } else if (data.error) {
                addMessageToChatBox('bot', `Erreur : ${data.error}`);
            }
            // Reset uploaded files
            uploadedImageUrl = null;
            uploadedAudioUrl = null;
        })
        .catch((error) => {
            console.error('Erreur:', error);
            removeTypingIndicator(typingMessage);
            addMessageToChatBox('bot', 'Désolé, une erreur de connexion est survenue.');
            uploadedImageUrl = null;
            uploadedAudioUrl = null;
        });

        messageInput.value = '';
    }

    function addTypingIndicator() {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('flex', 'mb-4', 'justify-start');

        const typingBubble = document.createElement('div');
        typingBubble.classList.add('bg-gray-700', 'rounded-2xl', 'p-4', 'max-w-xs', 'lg:max-w-md');

        const typingElement = document.createElement('div');
        typingElement.classList.add('flex', 'space-x-1');
        typingElement.innerHTML = '<div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div><div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s;"></div><div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s;"></div>';
        typingBubble.appendChild(typingElement);

        messageWrapper.appendChild(typingBubble);
        chatBox.appendChild(messageWrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageWrapper;
    }

    function removeTypingIndicator(typingMessage) {
        if (typingMessage && typingMessage.parentNode) {
            typingMessage.parentNode.removeChild(typingMessage);
        }
    }

    // Gestionnaire pour fermer le modal
    closeBtn.onclick = function() {
        modal.style.display = "none";
    }

    // Fermer le modal en cliquant en dehors
    modal.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }

    function addMessageToChatBox(sender, message, imageUrl = null, audioUrl = null) {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('flex', 'mb-4', sender === 'user' ? 'justify-end' : 'justify-start');

        const messageBubble = document.createElement('div');
        const bubbleColor = sender === 'user' ? 'bg-pink-500' : 'bg-gray-700';
        messageBubble.classList.add(bubbleColor, 'rounded-2xl', 'p-4', 'max-w-xs', 'lg:max-w-md');

        if (message) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('text-white', 'text-sm');
            messageElement.innerHTML = marked.parse(message);
            messageBubble.appendChild(messageElement);
        }

        if (imageUrl) {
            const imageElement = document.createElement('img');
            imageElement.src = imageUrl;
            imageElement.classList.add('chat-image', 'rounded-lg', 'mt-2', 'cursor-pointer');
            imageElement.onclick = () => {
                modal.classList.remove('hidden');
                modal.classList.add('flex');
                modalImg.src = imageElement.src;
            };
            messageBubble.appendChild(imageElement);
        }

        if (audioUrl) {
            const audioElement = document.createElement('audio');
            audioElement.src = audioUrl;
            audioElement.controls = true;
            audioElement.classList.add('chat-audio', 'w-full', 'mt-2');
            messageBubble.appendChild(audioElement);
        }

        messageWrapper.appendChild(messageBubble);
        chatBox.appendChild(messageWrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});