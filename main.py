import os
import google.generativeai as genai
import pyttsx3
import time


generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 2048,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

# API-KEYの設定
genai.configure(api_key='AIzaSyCBlL-cXc7WwWoM8hz3jP90Wt1pSXeoGzs')

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# モデルの生成
gemini_pro = genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=generation_config)

engine = pyttsx3.init()

#voice optimaiz
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)

#voice volume setting
volume = engine.getProperty('volume')
engine.setProperty('volume',volume+3.0)

#voice toone setting
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
print(voices)

name = "山田"
hobby = "ゲーム"
job = "システムエンジニア"
MBTI = "明るめ"
gender = "男性"
text ="これから"
text +="デートで異性と会った時のコミュニケーションの練習に付き合ってください。恋愛シュミレーションゲームのヒロインのように話してくれれば大丈夫です。\n あなたは女性役です。私と受け答えをしてください\n返答の文章はできるだけ人間に寄せてください。\n 私のMBTI診断の結果に合わせて喋り方を変えてください。\n以下がプロフィールです。\n性別："+gender+"\n名前："+name+"\n 趣味："+hobby+"\n仕事："+job+"\n性格："+MBTI
text += "\nまた、アドバイスなどの人間味の無い提案は、恋愛シュミレーションゲームでは全く行われないので、こちらが求めていなければ出さないようにしてください。"
text += "\nここで、質問は一回に一つだけです。"

text +="\n以下は女性役であるあなたのプロフィールです。このプロフィールに従って会話をしてください。\n性別：女性\n 名前：あい\n 趣味：マッチングアプリ\n仕事：IT企業のマネージャー\n あなたの性格：ぶりっこ\n一人称：私"
text += "\nすべての文章に対して、恋愛シュミレーションゲームのような会話をする際に、情報が足りない場合は、足りない情報を具体的に私に質問してください。私がその情報を渡します。"
text += "\n※あくまでもこれは会話です、私が入力した文章に反応をしてください。"
text += "\n顔文字や絵文字などの文字は使わないでください。"

print('\'end\' と打てばチャットが終了します。')
response = gemini_pro.generate_content(text + "\nはじめまして！")

#処理完了までの時間待機
startSec = time.time()
time.sleep(1.5)

print(response.text)
engine.say(response.text)
engine.runAndWait()
while True:
    # プロンプトの設定
    prompt = input()
    if prompt == "end":
        break
    
    if prompt != "":
        prompt += "\n※あくまでもこれは会話です、私が入力した文章に反応をしてください。"
        # テキスト生成
        response = gemini_pro.generate_content(prompt)

        # 生成結果の表示
        engine.say(response.text)
        print(response.text)
        engine.runAndWait()
