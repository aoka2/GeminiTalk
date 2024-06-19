async function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    const chatLog = document.getElementById('chatLog');
    let messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'user');
    messageDiv.innerHTML = `<div class="message-content">${userInput}</div>`;
    chatLog.appendChild(messageDiv);

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({message: userInput})
        });
        const data = await response.json();

        messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot');
        if (data.error) {
            messageDiv.innerHTML = `<div class="message-content" style="color: red;">エラー: ${data.error}</div>`;
        } else {
            messageDiv.innerHTML = `<div class="message-content">${data.response}</div>`;
        }
        chatLog.appendChild(messageDiv);
    } catch (error) {
        console.error('リクエスト中にエラーが発生しました:', error);
    }

    document.getElementById('userInput').value = '';
}
