        let chatHistory = []; // チャット履歴
        let canSendMessage = true; // メッセージを送信できるかどうか

        async function sendMessage() {
            if (!canSendMessage) return; // メッセージが送信できない場合は何もしない

            const userInput = document.getElementById("userInput");
            const chatLog = document.getElementById("chatLog");
            const historyLog = document.getElementById("historyLog");
            const userMessageValue = userInput.value.trim();

            if (userMessageValue !== "") {
                // メッセージ送信直前に入力欄を空にする
                userInput.value = "";
                canSendMessage = false; // メッセージが送信されたことを記録

                // 1秒後に再度メッセージを送信可能にする
                setTimeout(() => {
                    canSendMessage = true;
                }, 1000);

                // ユーザーのメッセージを追加
                const userMessage = `<div class="message user">${userName}: ${userMessageValue}</div>`;
                chatHistory.push(userMessage);
                historyLog.innerHTML += userMessage;

                try {
                    // ボットにメッセージを送信
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: userMessageValue }),
                    });
                    const data = await response.json();

                    // ボットの返答を追加
                    const botMessage = `<div class="message bot">${aiName}: ${data.response || "エラーが発生しました。"}</div>`;
                    chatHistory.push(botMessage);
                    historyLog.innerHTML += botMessage;

                    // 最新のメッセージだけを表示
                    chatLog.innerHTML = botMessage;
                } catch (error) {
                    // エラー時のメッセージを追加
                    const botMessage = `<div class="message bot">${aiName}: エラーが発生しました。</div>`;
                    chatHistory.push(botMessage);
                    historyLog.innerHTML += botMessage;

                    // 最新のメッセージだけを表示
                    chatLog.innerHTML = botMessage;
                }

                chatLog.scrollTop = chatLog.scrollHeight;
            }
        }

        function checkEnter(event) {
            if (event.key === "Enter") {
                event.preventDefault(); // デフォルトのEnterキーの動作を防ぐ
                sendMessage();
            }
        }

        function toggleHistory() {
            const historyModal = document.getElementById("historyModal");
            historyModal.style.display = historyModal.style.display === "block" ? "none" : "block";
        }

        window.onclick = function(event) {
            const historyModal = document.getElementById("historyModal");
            if (event.target === historyModal) {
                historyModal.style.display = "none";
            }
        }

        function spacesC(){
            const input = document.getElementById('userInput');
            hasSpaces(input.value);
        };

        function hasSpaces(str){
            if(str.startsWith(' ', 0) || str.startsWith('　', 0)){
                document.getElementById('userInput').value = '';
            }
        }