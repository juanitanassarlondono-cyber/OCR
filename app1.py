import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image


st.set_page_config(
    page_title="Reconocimiento óptico de Caracteres",
    page_icon="📷",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(59, 130, 246, 0.18), transparent 32%),
        linear-gradient(135deg, #0f172a 0%, #111827 45%, #1e293b 100%);
    color: #f8fafc;
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 900px;
}

h1 {
    text-align: center;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    color: #f8fafc !important;
    margin-bottom: 0.7rem !important;
    letter-spacing: -0.04em;
}

h1::after {
    content: "Captura una imagen, aplica el filtro si lo necesitas y extrae el texto automáticamente.";
    display: block;
    font-size: 1rem;
    font-weight: 400;
    color: #cbd5e1;
    margin-top: 0.75rem;
    letter-spacing: 0;
}

section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid rgba(148, 163, 184, 0.22);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

section[data-testid="stSidebar"] label {
    color: #f8fafc !important;
    font-weight: 700 !important;
}

.stRadio {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 18px;
    padding: 1.1rem;
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.22);
}

.stRadio div[role="radiogroup"] label {
    background: rgba(30, 41, 59, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 999px;
    padding: 0.55rem 0.9rem;
    margin-bottom: 0.45rem;
    transition: all 0.2s ease;
}

.stRadio div[role="radiogroup"] label:hover {
    background: rgba(59, 130, 246, 0.18);
    border-color: rgba(96, 165, 250, 0.65);
}

div[data-testid="stCameraInput"] {
    background: rgba(15, 23, 42, 0.82);
    border: 1px solid rgba(148, 163, 184, 0.28);
    border-radius: 28px;
    padding: 1.5rem;
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.32);
    backdrop-filter: blur(16px);
    margin-top: 2rem;
}

div[data-testid="stCameraInput"] label {
    color: #f8fafc !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
}

button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, #2563eb, #06b6d4) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.75rem 1.2rem !important;
    font-weight: 700 !important;
    box-shadow: 0 14px 35px rgba(37, 99, 235, 0.35);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 18px 45px rgba(37, 99, 235, 0.48);
}

.stMarkdown, .stText, .stWrite {
    color: #f8fafc;
}

div[data-testid="stMarkdownContainer"] {
    color: #f8fafc;
}

div[data-testid="stImage"] {
    border-radius: 22px;
    overflow: hidden;
}

div[data-testid="stVerticalBlock"] > div:has(.stMarkdown) {
    background: rgba(15, 23, 42, 0.72);
    border-radius: 22px;
}

.stAlert {
    border-radius: 18px;
}

@media (max-width: 768px) {
    .block-container {
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    h1 {
        font-size: 2rem !important;
    }

    h1::after {
        font-size: 0.92rem;
    }

    div[data-testid="stCameraInput"] {
        padding: 1rem;
        border-radius: 22px;
    }
}
</style>
""", unsafe_allow_html=True)


st.title("Reconocimiento óptico de Caracteres")

img_file_buffer = st.camera_input("Toma una Foto")

with st.sidebar:
      filtro = st.radio("Aplicar Filtro",('Con Filtro', 'Sin Filtro'))


if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    if filtro == 'Con Filtro':
         cv2_img=cv2.bitwise_not(cv2_img)
    else:
         cv2_img= cv2_img
    
        
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text=pytesseract.image_to_string(img_rgb)

    st.markdown("### Texto extraído")
    st.write(text)
