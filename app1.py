import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image


st.set_page_config(
    page_title="Reconocimiento óptico de Caracteres",
    page_icon="📷",
    layout="wide",
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
    max-width: 1100px;
}

h1 {
    text-align: center;
    font-size: 2.7rem !important;
    font-weight: 800 !important;
    color: #f8fafc !important;
    margin-bottom: 0.7rem !important;
    letter-spacing: -0.04em;
}

h1::after {
    content: "Captura o sube una imagen, aplica un filtro y extrae el texto automáticamente.";
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

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(148, 163, 184, 0.22);
}

.stRadio,
.stFileUploader {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 18px;
    padding: 1rem;
    margin-bottom: 1rem;
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

.ocr-result {
    background: rgba(15, 23, 42, 0.82);
    border: 1px solid rgba(148, 163, 184, 0.28);
    border-radius: 24px;
    padding: 1.5rem;
    margin-top: 2rem;
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.25);
}

.ocr-result h3 {
    margin-top: 0;
    color: #f8fafc;
}

.ocr-help {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 18px;
    padding: 1rem;
    margin-top: 1rem;
    color: #cbd5e1;
    font-size: 0.92rem;
    line-height: 1.55;
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


with st.sidebar:
    st.markdown("## ⚙️ Opciones")

    st.markdown("### 📥 Fuente de imagen:")
    fuente_imagen = st.radio(
        "Selecciona la fuente:",
        ("📷 Cámara", "🖼️ Subir imagen"),
        label_visibility="collapsed"
    )

    st.markdown("### 🎨 Filtros de imagen")
    filtro = st.radio(
        "Selecciona un filtro:",
        ("Sin filtro", "Invertir colores", "Escala de grises", "Alto contraste")
    )

    st.markdown("""
    <div class="ocr-help">
        <h3>📖 ¿Cómo funciona?</h3>
        <p>OCR (Optical Character Recognition) analiza los píxeles de una imagen para identificar letras y palabras.</p>

        <strong>Consejos para mejores resultados:</strong><br><br>
        💡 Buena iluminación<br>
        📄 Texto nítido y sin desenfoque<br>
        ⬛ Buen contraste entre texto y fondo<br>
        📐 Imagen lo más recta posible
    </div>
    """, unsafe_allow_html=True)


img_file_buffer = None

if fuente_imagen == "📷 Cámara":
    img_file_buffer = st.camera_input("Toma una Foto")
else:
    img_file_buffer = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])


if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == "Invertir colores":
        cv2_img = cv2.bitwise_not(cv2_img)

    elif filtro == "Escala de grises":
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_GRAY2BGR)

    elif filtro == "Alto contraste":
        lab = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        cv2_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    else:
        cv2_img = cv2_img

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)

    st.markdown("""
    <div class="ocr-result">
        <h3>Texto extraído</h3>
    </div>
    """, unsafe_allow_html=True)

    st.write(text)
