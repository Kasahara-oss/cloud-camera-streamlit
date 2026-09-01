import streamlit as st
from google import genai
import os

st.set_page_config(page_title="雲カメラ AI", page_icon="📸", layout="centered")
st.title("📸 雲カメラ AI (Streamlit版)")
st.write("撮影した写真をAIが判定し、雲の名前や天気の傾向を教えます。")

# 🔑 Renderの「Environment」から自動的にAPIキーを読み込みます
api_key = os.environ.get("GEMINI_API_KEY")

# 📸 スマホのカメラを起動、またはアルバムから写真を選択するボタン
uploaded_file = st.file_uploader("真ん中のボタンを押して撮影してください。", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="撮影した写真", use_container_width=True)
    
    if not api_key:
        st.error("Gemini APIキーが設定されていません。RenderのEnvironment設定を確認してください。")
    else:
        with st.spinner("ここにAIの判定結果が出ます。解析中..."):
            try:
                # 🤖 新しいGoogle GenAI SDK（2025/2026年標準）での初期化
                client = genai.Client(api_key=api_key)
                image_bytes = uploaded_file.read()
                
                # 🪐 無料枠の最新Flashモデルで画像を解析
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        {'mime_type': 'image/jpeg', 'data': image_bytes},
                        "この画像に写っている雲の種類を特定し、その特徴と今後の天気の変化の予測を分かりやすく日本語で解説してください。"
                    ]
                )
                st.subheader("🤖 AIの判定結果")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI解析エラー: {e}")
