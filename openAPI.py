import streamlit as st
import easyocr
import numpy as np
import requests
from PIL import Image, ImageDraw
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# ----------- 설정값 -----------
PROB_THRESHOLD = 0.75  # 박스를 그릴 인식 확률 기준
READER = easyocr.Reader(['en', 'ko'], gpu=False)

# ----------- 번역 함수 -----------
def translate_text(text, source='en', target='ko'):
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": f"{source}|{target}"}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        return data['responseData']['translatedText']
    except Exception as e:
        return f"번역 실패: {e}"

# ----------- 이미지 처리 함수 -----------
def process_image(image: Image.Image):
    np_image = np.array(image)
    results = READER.readtext(np_image)

    draw = ImageDraw.Draw(image)
    texts = []

    for bbox, text, prob in results:
        if prob >= PROB_THRESHOLD:
            box = [tuple(map(int, point)) for point in bbox]
            draw.polygon(box, outline=(255, 0, 0), width=3)
            texts.append(text)

    return image, texts



# ----------- Streamlit UI -----------
st.set_page_config(page_title="이미지 텍스트 번역기", layout="centered")
st.title("🖼️ 이미지 텍스트 번역기")
st.write("이미지에서 텍스트를 추출하고 번역해줍니다.")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
target_lang = st.selectbox("번역할 언어", ['ko', 'en', 'ja', 'zh-CN', 'fr', 'de', 'es'])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("원본 이미지")
        st.image(image, use_container_width=True)

    with st.spinner("문자 인식 중..."):
        processed_image, text_list = process_image(image.copy())

    with col2:
        st.subheader("인식 결과 이미지")
        st.image(processed_image, use_container_width=True)

    st.subheader("📝 인식된 텍스트와 번역")
    if text_list:
        full_text = " ".join(text_list)
        with st.spinner("번역 중..."):
            translated = translate_text(full_text, source='auto', target=target_lang)
        st.markdown(f"**원문**: {full_text}")
        st.markdown(f"**번역**: {translated}")
    else:
        st.info("텍스트를 인식하지 못했습니다.")
