import os
import google.generativeai as genai

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
genai.configure(api_key='AIzaSyDIOSHb1tAUisHOTexjoDXp8_jRc_eFKys')

# モデルの生成
gemini_pro = genai.GenerativeModel("gemini-1.5-pro-latest")

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
print('\'end\' と打てばチャットが終了します。')
print(text)
response = gemini_pro.generate_content(text + "\nはじめまして！")
print(response.text)
while True:
    try:
      # プロンプトの設定
      print("あなた>>>")
      prompt =""
      prompt = input()
      if prompt == "end":
          break
      
      if prompt != "":
          # テキスト生成
          response = gemini_pro.generate_content(prompt)

          # 生成結果の表示
          if response.candidate and response.candidate.safety_ratings:
              print(response)
              try:
                  print(response.text)
              except Exception as er:
                  print(f"Error accessing response text: {er}")
          else:
              print("Response does not contain a valid Part or was blocked.")
    except Exception as e:
      print(f"An error occurred: {e}")
