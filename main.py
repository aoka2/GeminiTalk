import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import google.generativeai as genai
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションを使用するために必要

# API-KEYの設定
genai.configure(api_key='AIzaSyC6m3rthOaCarBypLbBOgip8W6_OCr2ruk')

#セッションの設定
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
initial_prompt_template = {
    "default": (
        "デートで異性と会った時のコミュニケーションの練習に付き合ってください。"
        "恋愛シミュレーションゲームのヒロインのように話してくれれば大丈夫です。\n"
        "あなたは{ai_gender}性役です。私と受け答えをしてください。\n"
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
        "以下は{ai_gender}性役であるあなたのプロフィールです。このプロフィールに従って会話をしてください。\n"
        "名前：{ai_name}\n"
        "性別：{ai_gender}\n"
        "年齢：{ai_age}\n"
        "趣味：{ai_hobbies}\n"
        "仕事：{ai_occupation}\n"
        "あなたの性格：犬系彼女\n"
        "一人称：私\n"
        "恋愛シミュレーションゲームのような会話をする際に、情報が足りない場合は、足りない情報を具体的に私に質問してください。"
    ),
    "ご飯デート": (
        "今日はご飯デートの日です。異性と初めての食事を楽しみながら、楽しい会話を続けましょう。\n"
        "あなたは{ai_gender}性役です。私と受け答えをしてください。\n"
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
        "待ち合わせ場所はレストランです。\n"
        "ここで、質問は一回に一つだけです。\n"
        "以下は{ai_gender}性役であるあなたのプロフィールです。このプロフィールに従って会話をしてください。\n"
        "名前：{ai_name}\n"
        "性別：{ai_gender}\n"
        "年齢：{ai_age}\n"
        "趣味：{ai_hobbies}\n"
        "仕事：{ai_occupation}\n"
        "あなたの性格：犬系彼女\n"
        "一人称：私\n"
        "恋愛シミュレーションゲームのような会話をする際に、情報が足りない場合は、足りない情報を具体的に私に質問してください。"
    ),
    "ドライブデート": (
        "今日はドライブデートの日です。車での移動中に楽しい会話を続けましょう。\n"
        "あなたは{ai_gender}性役です。私と受け答えをしてください。\n"
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
        "待ち合わせ場所は車です。\n"
        "ここで、質問は一回に一つだけです。\n"
        "以下は{ai_gender}性役であるあなたのプロフィールです。このプロフィールに従って会話をしてください。\n"
        "名前：{ai_name}\n"
        "性別：{ai_gender}\n"
        "年齢：{ai_age}\n"
        "趣味：{ai_hobbies}\n"
        "仕事：{ai_occupation}\n"
        "あなたの性格：犬系彼女\n"
        "一人称：私\n"
        "恋愛シミュレーションゲームのような会話をする際に、情報が足りない場合は、足りない情報を具体的に私に質問してください。"
    ),
    "スケベデート": (
        "今日はスケベデートの日です。あなたは{ai_gender}性役です。私と受け答えをしてください。\n"
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
        "待ち合わせ場所は秘密の場所です。\n"
        "ここで、質問は一回に一つだけです。\n"
        "以下は{ai_gender}性役であるあなたのプロフィールです。このプロフィールに従って会話をしてください。\n"
        "名前：{ai_name}\n"
        "性別：{ai_gender}\n"
        "年齢：{ai_age}\n"
        "趣味：{ai_hobbies}\n"
        "仕事：{ai_occupation}\n"
        "あなたの性格：犬系彼女\n"
        "一人称：私\n"
        "恋愛シミュレーションゲームのような会話をする際に、情報が足りない場合は、足りない情報を具体的に私に質問してください。"
    )
}

#GETをPOSTに変更
@app.route('/reset_session', methods=['POST'])
def reset_session():
    session.clear()  # セッションをクリア
    return redirect(url_for('profile'))  # プロフィールページにリダイレクト


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile.html', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['gender'] = request.form['gender']
        session['age'] = request.form['age']
        session['hobbies'] = request.form['hobbies']
        session['occupation'] = request.form['occupation']
        session['mbti'] = request.form['mbti']
        return redirect(url_for('AIprofile.html'))

    return render_template('profile.html',
        name=session.get('name', ''),
        gender=session.get('gender', ''),
        age=session.get('age', ''),
        hobbies=session.get('hobbies', ''),
        occupation=session.get('occupation', ''),
        mbti=session.get('mbti', ''))

@app.route('/AIprofile.html', methods=['GET', 'POST'])
def AIprofile():
    if request.method == 'POST':
        session['ai_name'] = request.form['name']
        session['ai_gender'] = request.form['gender']
        session['ai_age'] = request.form['age']
        session['ai_hobbies'] = request.form['hobbies']
        session['ai_occupation'] = request.form['occupation']
        return redirect(url_for('profile.html'))  # 適切な次のページにリダイレクト

    return render_template('AIprofile.html',
        ai_name=session.get('ai_name', ''),
        ai_gender=session.get('ai_gender', ''),
        ai_age=session.get('ai_age', ''),
        ai_hobbies=session.get('ai_hobbies', ''),
        ai_occupation=session.get('ai_occupation', ''))

@app.route('/OkonomiJyosei.html')
def OkonomiJyosei():
    return render_template('OkonomiJyosei.html')

@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')

@app.route('/set_profile', methods=['POST'])
def set_profile():
    session['name'] = request.form['name']
    session['gender'] = request.form['gender']
    session['age'] = request.form['age']
    session['hobbies'] = request.form['hobbies']
    session['occupation'] = request.form['occupation']
    session['mbti'] = request.form['mbti']

    return redirect(url_for('AIprofile'))

@app.route('/set_AIprofile', methods=['POST'])
def set_AIprofile():
    session['ai_name'] = request.form['name']
    session['ai_gender'] = request.form['gender']
    session['ai_age'] = request.form['age']
    session['ai_hobbies'] = request.form['hobbies']
    session['ai_occupation'] = request.form['occupation']

    return redirect(url_for('OkonomiJyosei'))

@app.route('/set_OkonomiJyosei', methods=['POST'])
def set_OkonomiJyosei():
    date_preference = request.form.get('date_preference')

    # セッションからプロフィール情報を取得
    profile = session.get('profile', {})
    AIprofile = session.get('AIprofile', {})

    initial_prompt = initial_prompt_template.get(date_preference, initial_prompt_template["default"]).format(
        name=profile.get('name'),
        gender=profile.get('gender'),
        hobbies=profile.get('hobbies'),
        occupation=profile.get('occupation'),
        mbti=profile.get('mbti'),
        ai_name=AIprofile.get('ai_name'),
        ai_gender=AIprofile.get('ai_gender'),
        ai_age=AIprofile.get('ai_age'),
        ai_hobbies=AIprofile.get('ai_hobbies'),
        ai_occupation=AIprofile.get('ai_occupation')
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
