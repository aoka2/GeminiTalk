/**************************************************************************************** */
//音声入力系セットアップ

//入力場所
const resultDiv = document.querySelector('.result-div');


SpeechRecognition = webkitSpeechRecognition || SpeechRecognition;
let recognition = new SpeechRecognition();

recognition.lang = 'ja-JP';
recognition.interimResults = true;
recognition.continuous = true;

let finalTranscript = ''; // 確定した(黒の)認識結果

recognition.onresult = (event) => {
    console.log('音声認識実行');
    let interimTranscript = ''; // 暫定(灰色)の認識結果
    for (let i = event.resultIndex; i < event.results.length; i++) {
        
        let transcript = event.results[i][0].transcript;
    if (event.results[i].isFinal) {
        finalTranscript += transcript;
    } else {
        interimTranscript = transcript;
    }
    }
    resultDiv.value = finalTranscript +  interimTranscript;
}
/*************************************************************************************** */

async function sendMessage() {
    recognition.stop();
    console.log("sendMessage、32行目を実行")
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
            let url = `https://deprecatedapis.tts.quest/v2/voicevox/audio/?text=${data.response}&key=d-43s0230-T-Q_L`;
            let audio = new Audio(url)
            audio.play();
        }
        chatLog.appendChild(messageDiv);
        document.getElementById('userInput').value = '';
        //入力欄初期化・音声入力スタート
    } catch (error) {
        console.error('リクエスト中にエラーが発生しました:', error);
    }

    
}


window.onload = function(){
    const startBtn = document.querySelector('#start-btn');
    const stopBtn = document.querySelector('#stop-btn');

    startBtn.onclick = () => {
        recognition.start();
      }
      stopBtn.onclick = () => {
        recognition.stop();
      }
}