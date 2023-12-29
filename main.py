from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chatbot con OpenAI</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                height: 100vh;
                background-color: #eaeaea;
            }
            #chatbot-header {
                text-align: center;
                color: #007bff;
                font-size: 2em;
                margin-top: 20px;
                padding: 10px;
                font-weight: normal;
            }
            #chat-container {
                width: 90%;
                max-width: 400px;
                height: 60vh;
                max-height: 600px;
                box-shadow: 0 0 10px 0 rgba(0,0,0,0.2);
                border-radius: 8px;
                overflow: hidden;
                background: white;
                display: flex;
                flex-direction: column;
                margin-bottom: 20px;
            }
            #messages {
                flex-grow: 1;
                overflow-y: auto;
                padding: 10px;
            }
            .message {
                background: #f1f1f1;
                padding: 10px 15px;
                margin: 5px;
                border-radius: 10px;
                width: fit-content;
            }
            .user {
                background: #007bff;
                color: white;
                margin-left: auto;
            }
            #input-box {
                display: flex;
                padding: 5px;
            }
            #user-input {
                flex: 1;
                padding: 10px;
                border: none;
                border-radius: 4px;
                margin-right: 5px;
            }
            #send-button {
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                background: #007bff;
                color: white;
                cursor: pointer;
            }
            #send-button:hover {
                background: #0056b3;
            }
                                  
            input, button {
                 font-size: 16px; /* Tamaño mínimo para prevenir el zoom en iPhone */
            }              
            @media (max-width: 768px) {
                #chatbot-header {
                    font-size: 1.5em;
                }
            }
        </style>
    </head>
    <body>
        <h1 id="chatbot-header">Bot creado por polvalero</h1>
        <div id="chat-container">
            <div id="messages"></div>
            <div id="input-box">
                <input type="text" id="user-input" placeholder="Escribe un mensaje..." autocomplete="off">
                <button id="send-button">Enviar</button>
            </div>
        </div>
                                  <script>document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button');
    const userInputField = document.getElementById('user-input');
    const messagesContainer = document.getElementById('messages');

    sendButton.addEventListener('click', () => {
        const userMessage = userInputField.value.trim();
        if (userMessage) {
            addMessage('user', userMessage);
            sendToOpenAI(userMessage);
            userInputField.value = '';
        }
    });

    function addMessage(sender, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = content;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function sendToOpenAI(message) {
        // En producción, reemplaza esta lógica por una solicitud a tu servidor.
        const apiKey = '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'; // Esta clave debe mantenerse en secreto
        fetch('https://api.openai.com/v1/engines/text-davinci-003/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                prompt: message,
                max_tokens: 150
            })
        })
        .then(response => response.json())
        .then(data => {
            const botReply = data.choices[0].text.trim();
            addMessage('bot', botReply);
        })
        .catch(error => {
            console.error('Error al conectar con OpenAI:', error);
            addMessage('bot', 'No se pudo obtener una respuesta.'); // Mensaje de error para el usuario
        });
    }
});

function sendToOpenAI(message) {
    const data = {
        prompt: message,
        max_tokens: 150,
        temperature: 0.7
    };

    fetch('https://api.openai.com/v1/engines/text-davinci-003/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${openaiApiKey}`
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error en la API: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (!data.choices || data.choices.length === 0) {
            throw new Error('No se recibieron opciones de la API.');
        }
        const botReply = data.choices[0].text.trim();
        addMessage('bot', botReply);
    })
    .catch(error => {
        console.error('Error al conectar con OpenAI:', error);
        addMessage('bot', 'No se pudo obtener una respuesta.'); // Mensaje de error para el usuario
    });
}
</script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='192.168.1.136', port=100)
