from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import gradio as gr
from transformers import pipeline
from diffusers import AutoPipelineForText2Image
from PIL import Image
import numpy as np
import torch

# 翻訳モデルとトークナイザを読み込む
translation_model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
translation_tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

# チャットボットパイプラインを読み込む
pipe_chatbot = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.float32, device="cpu")

# テキストから画像生成パイプラインを読み込む
pipe_image = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32)
pipe_image.to("cpu")

def translate_ja_to_en(text):
    # 日本語から英語への翻訳
    translation_tokenizer.src_lang = "ja"
    translation_tokenizer.tgt_lang = "en"
    encoded_text = translation_tokenizer(text, return_tensors="pt")
    generated_tokens = translation_model.generate(**encoded_text, forced_bos_token_id=translation_tokenizer.get_lang_id("en"))
    translated_result = translation_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated_result

def translate_en_to_ja(text):
    # 英語から日本語への翻訳
    translation_tokenizer.src_lang = "en"
    translation_tokenizer.tgt_lang = "ja"
    encoded_text = translation_tokenizer(text, return_tensors="pt")
    generated_tokens = translation_model.generate(**encoded_text, forced_bos_token_id=translation_tokenizer.get_lang_id("ja"))
    translated_result = translation_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated_result

def chatbot_and_image_generation(user_input_chat, user_input_image):
    # チャットボットの機能
    user_input_en = translate_ja_to_en(user_input_chat)
    messages_chat = [
        {"role": "system", "content": "フレンドリーなチャットボットです"},
        {"role": "user", "content": user_input_en},
    ]
    prompt_chat = pipe_chatbot.tokenizer.apply_chat_template(messages_chat, tokenize=False, add_generation_prompt=True)
    outputs_chat = pipe_chatbot(prompt_chat, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    generated_response_ja_chat = translate_en_to_ja(outputs_chat[0]["generated_text"])

    # 画像生成の機能
    prompt_image = translate_ja_to_en(user_input_image)
    image_result = pipe_image(prompt=prompt_image, num_inference_steps=1, guidance_scale=0.0).images[0]

    return generated_response_ja_chat, Image.fromarray(np.array(image_result))

# Gradioのインターフェースを定義
iface = gr.Interface(
    fn=chatbot_and_image_generation,
    inputs=[
        gr.Textbox(type="text", label="チャット入力", placeholder="Enterで送信"),
        gr.Textbox(type="text", label="画像入力", placeholder="Enterで送信"),
    ],
    outputs=[
        gr.Textbox(type="text", label="チャットボット応答"),
        gr.Image(type="pil", label="生成された画像")
    ],
    #live=True
)

# Gradio UIを起動してリンクを表示
iface.launch(share=True, debug=True)
