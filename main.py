import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
import google.generativeai as genai

app = Flask(__name__)

# API-KEYの設定
genai.configure(api_key='AIzaSyC6m3rthOaCarBypLbBOgip8W6_OCr2ruk')

# 生成設定
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# モデルの生成
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)
chat_session = model.start_chat(history=[])

# 初期プロンプトの設定
initial_prompt_template = (
    "デートで異性と会った時のコミュニケーションの練習に付き合ってください。"
    "恋愛シミュレーションゲームのヒロインのように話してくれれば大丈夫です。\n"
    "あなたは女性役です。私と受け答えをしてください。\n"
    "返答の文章はできるだけ人間に寄せてください。\n"
    "私のMBTI診断の結果に合わせて喋り方を変えてください。\n"
    "以下がプロフィールです。\n"
    "性別：{gender}\n"
    "名前：{name}\n"
    "趣味：{hobbies}\n"
    "仕事：{occupation}\n"
    "性格：やんちゃ\n"
    "MBTI : {mbti}\n"
    "また、アドバイスなどの人間味の無い提案は、恋愛シミュレーションゲームでは全く行われないので、"
    "こちらが求めていなければ出さないようにしてください。\n"
    "待ち合わせ場所は岡山駅です。\n"
    "ここで、質問は一回に一つだけです。\n"
    "以下は女性役であるあなたのプロフィールです。このプロフィールに従って会話をしてください。\n"
    "名前：あい\n"
    "性別：女性\n"
    "年齢：２０\n"
    "趣味：ゲーム\n"
    "仕事：IT企業のマネージャー\n"
    "あなたの性格：犬系彼女\n"
    "一人称：私\n"
    "恋愛シミュレーションゲームのような会話をする際に、情報が足りない場合は、足りない情報を具体的に私に質問してください。"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')

@app.route('/set_profile', methods=['POST'])
def set_profile():
    name = request.form.get('name')
    gender = request.form.get('gender')
    hobbies = request.form.get('hobbies')
    occupation = request.form.get('occupation')
    mbti = request.form.get('mbti')

    initial_prompt = initial_prompt_template.format(
        name=name,
        gender=gender,
        hobbies=hobbies,
        occupation=occupation,
        mbti=mbti
    )

    # 初回メッセージ送信
    try:
        print(f"Sending initial prompt: {initial_prompt}")
        chat_session.send_message(initial_prompt)
    except Exception as e:
        print(f"初回メッセージの送信中にエラーが発生しました: {e}")

    return redirect(url_for('chatbot'))

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if user_input:
        try:
            response = chat_session.send_message(user_input)
            return jsonify({'response': response.text})
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'error': 'No message provided'})

if __name__ == '__main__':
    app.run(debug=True)
