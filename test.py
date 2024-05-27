"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai

# API-KEYの設定
genai.configure(api_key='AIzaSyDIOSHb1tAUisHOTexjoDXp8_jRc_eFKys')
# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
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

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-latest",
  safety_settings=safety_settings,
  generation_config=generation_config,
)


# response = chat_session.send_message("")

# print(response.text)
# print(chat_session.history)


# モデルの生成
# gemini_pro = genai.GenerativeModel("gemini-1.5-pro-latest")

name = "山田"
hobby = "絵を描く事"
job = "プログラマー"
MBTI = ""

text ="出会い系アプリで会った方とのコミュニケーションの練習に付き合ってください\n あなたは女性役です。私と受け答えをしてください\n返答の文章はできるだけ人間に寄せてください。人間はアドバイスをたくさんせず、共感を使用としますので、アドバイスはしないでください\n 私のMBTI診断の結果に合わせて喋り方を変えてください。\n以下がプロフィールです。\n名前："+name+"\n 趣味："+hobby+"\n仕事："+job+"\nMBTI診断結果："+MBTI

print('\'end\' と打てばチャットが終了します。')
response = chat_session.send_message(text + "\nはじめまして！")
print(response.text)
while True:
    # プロンプトの設定
    prompt = input()
    if prompt == "end":
        break
    
    print("AIちゃん>>>")
    if prompt != "":
        # テキスト生成
        response = chat_session.send_message(prompt)

        # 生成結果の表示
        print(response.text)

