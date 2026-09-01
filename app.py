import streamlit as st
import os
import mimetypes
from google import genai
from google.genai import types

st.set_page_config(page_title="雲カメラ AI", page_icon="📸", layout="centered")
st.title("📸 雲カメラ AI (Streamlit版)")
st.write("撮影した写真をAIが判定し、雲の名前や天気の傾向を教えます。")

# 🔑 Renderの環境変数からAPIキーを確実に読み込みます
api_key = os.environ.get("GEMINI_API_KEY")

# 📸 スマホのカメラと連動するボタン
uploaded_file = st.file_uploader("真ん中のボタンを押して撮影してください。", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="撮影した写真", use_container_width=True)
    
    if not api_key:
        st.error("Gemini APIキーが設定されていません。RenderのEnvironment設定を確認してください。")
    else:
        with st.spinner("ここにAIの判定結果が出ます。解析中..."):
            try:
                # 🛠️ Streamlitの画像データを、1番目と同じ純粋なバイトデータに完全変換
                image_bytes = uploaded_file.getvalue()
                
                # 画像の形式を自動判別
                mime_type, _ = mimetypes.guess_type(uploaded_file.name)
                if not mime_type:
                    mime_type = "image/jpeg"
                
                client = genai.Client(api_key=api_key)
                
                # 🪐 1番目で100%成功した「types.Part.from_bytes」の書き方で送信
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                        "この空の雲の種類を判定し、明日の天気予報の確率を日本語で答えてください。"
                    ],
                )
                
                st.subheader("🤖 AIからの判定結果")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"AI解析エラーが発生しました: {e}")
