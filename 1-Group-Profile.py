import streamlit as st
from PIL import Image
from io import BytesIO
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Group Members",
    page_icon="👥",
    layout="wide"
)

# ---------------- SIDEBAR: LANGUAGE ----------------
st.sidebar.title("⚙️ Settings")
lang = st.sidebar.radio("Language / Bahasa:", ["English", "Bahasa Indonesia"], index=0)

# ---------------- CONTENT (BILINGUAL) ----------------
content = {
    "English": {
        "page_title": "👥 Group Members",
        "subtitle": "Meet the team behind this project — the people planning, designing, and building it.",
        "roles": {
            "leader": "Project Leader",
            "dev": "Developer",
            "rd": "Research & Design",
        }
    },
    "Bahasa Indonesia": {
        "page_title": "👥 Anggota Kelompok",
        "subtitle": "Kenali tim di balik proyek ini — orang-orang yang merencanakan, mendesain, dan membangunnya.",
        "roles": {
            "leader": "Ketua Proyek",
            "dev": "Pengembang",
            "rd": "Riset & Desain",
        }
    },
}
c = content[lang]

# ---------------- GLOBAL CSS (PREMIUM THEME) ----------------
st.markdown(
    """
    <style>
    :root {
        --card-radius: 22px;
        --glass-bg: rgba(10, 14, 35, 0.75);
        --glass-border: rgba(255, 255, 255, 0.08);
        --text-soft: #c9cce5;
    }

    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: "Plus Jakarta Sans", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top, #2b3459 0, #050818 40%, #02030a 100%);
        color: #f7f7ff;
    }

    .block-container {
        padding-top: 2.6rem !important;
        max-width: 1100px !important;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #ffffff66, transparent);
        margin-top: 8px;
        margin-bottom: 28px;
    }

    .glow-title {
        font-size: 44px !important;
        font-weight: 800 !important;
        text-align: center;
        color: #ffffff;
        text-shadow:
            0 0 18px rgba(135, 181, 255, 0.75),
            0 0 38px rgba(103, 232, 249, 0.45);
        letter-spacing: 1.4px;
        margin-bottom: 4px;
        margin-top: -10px;
    }

    .subtitle {
        text-align: center;
        margin: 0 auto 1.8rem;
        max-width: 520px;
        font-size: 0.96rem;
        color: var(--text-soft);
        line-height: 1.55;
        opacity: 0;
        animation: fadeUp 1.2s ease-out forwards;
    }

    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(24px) scale(0.97); filter: blur(4px); }
        60% { opacity: 0.9; transform: translateY(8px) scale(1.01); filter: blur(1px); }
        100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }

    .fade-in { opacity: 0; animation: fadeUp 1.1s ease-out forwards; }
    .delay-1 { animation-delay: 0.0s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.4s; }

    .member-card {
        width: 100%;
        max-width: 280px;
        margin: 0 auto 1.6rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.75rem;
    }

    .photo-frame {
        position: relative;
        width: 100%;
        padding: 2px;
        border-radius: var(--card-radius);
        background: linear-gradient(135deg,
            rgba(123, 157, 255, 0.9),
            rgba(255, 122, 196, 0.9),
            rgba(77, 227, 201, 1)
        );
        box-shadow:
            0 18px 40px rgba(0, 0, 0, 0.65),
            0 0 30px rgba(135, 181, 255, 0.45);
        overflow: hidden;
    }

    .member-photo {
        width: 100%;
        display: block;
        border-radius: calc(var(--card-radius) - 3px);
        background: var(--glass-bg);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.8),
            inset 0 0 18px rgba(255, 255, 255, 0.05);
        transition: transform 0.45s ease, box-shadow 0.45s ease, filter 0.45s ease;
    }

    .photo-glow {
        position: absolute;
        inset: -18%;
        border-radius: inherit;
        opacity: 0.55;
        filter: blur(22px);
        mix-blend-mode: screen;
        pointer-events: none;
    }

    .accent-blue .photo-glow { background: radial-gradient(circle at 0% 0%, #8bb2ff, transparent 55%); }
    .accent-pink .photo-glow { background: radial-gradient(circle at 100% 0%, #ff9fd8, transparent 55%); }
    .accent-teal .photo-glow { background: radial-gradient(circle at 50% 100%, #6df3d5, transparent 55%); }

    .member-card:hover .member-photo {
        transform: translateY(-7px) scale(1.03);
        box-shadow:
            0 22px 48px rgba(0, 0, 0, 0.85),
            0 0 40px rgba(135, 181, 255, 0.7);
        filter: brightness(1.08);
    }

    .member-meta {
        background: radial-gradient(circle at top left,
            rgba(255, 255, 255, 0.26),
            rgba(255, 255, 255, 0.08)
        );
        border-radius: 999px;
        padding: 10px 18px;
        border: 1px solid rgba(255, 255, 255, 0.22);
        box-shadow:
            0 8px 20px rgba(0, 0, 0, 0.45),
            inset 0 0 14px rgba(255, 255, 255, 0.15);
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 80%;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
    }

    .member-name { font-weight: 700; font-size: 1.03rem; letter-spacing: 0.03em; }
    .member-role {
        margin-top: 2px;
        font-size: 0.83rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--text-soft);
    }

    @media (max-width: 900px) {
        .block-container { padding-top: 2.2rem !important; padding-left: 1.1rem !important; padding-right: 1.1rem !important; }
        .glow-title { font-size: 32px !important; margin-top: 0; }
        .member-card { max-width: 320px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ----------------
st.markdown(f"<div class='glow-title'>{c['page_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{c['subtitle']}</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- LOAD IMAGES ----------------
img1 = Image.open("assets/anggota1.jpg")
img2 = Image.open("assets/anggota2.jpg")
img3 = Image.open("assets/anggota3.jpg")

# ---------------- IMAGE TO BASE64 FUNCTION ----------------
def image_to_base64(pil_img):
    if pil_img.mode == "RGBA":
        pil_img = pil_img.convert("RGB")
    buffer = BytesIO()
    pil_img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

# ---------------- MEMBERS (NAMES FIXED, ROLES TRANSLATED) ----------------
members = [
    {"img": img1, "name": "Member 1", "role_key": "leader", "delay": "delay-1", "accent": "accent-blue"},
    {"img": img2, "name": "Member 2", "role_key": "dev",    "delay": "delay-2", "accent": "accent-pink"},
    {"img": img3, "name": "Member 3", "role_key": "rd",     "delay": "delay-3", "accent": "accent-teal"},
]

# ---------------- COLUMNS ----------------
col1, col2, col3 = st.columns(3, gap="large")
cols = [col1, col2, col3]

def show_member(column, image, name, role, delay_class, accent_class):
    encoded_img = image_to_base64(image)
    with column:
        st.markdown(
            f"""
            <div class="member-card fade-in {delay_class} {accent_class}">
                <div class="photo-frame">
                    <div class="photo-glow"></div>
                    <img src="data:image/jpeg;base64,{encoded_img}" class="member-photo" />
                </div>
                <div class="member-meta">
                    <div class="member-name">{name}</div>
                    <div class="member-role">{role}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------- RENDER MEMBERS ----------------
for col, m in zip(cols, members):
    role_text = c["roles"][m["role_key"]]
    show_member(col, m["img"], m["name"], role_text, m["delay"], m["accent"])
