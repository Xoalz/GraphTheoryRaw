import streamlit as st
from PIL import Image
from io import BytesIO
import base64

# ---------------- CSS REFINED PREMIUM THEME ----------------
st.markdown(
    """
    <style>

    /* Global Layout Tweaks */
    .block-container {
        padding-top: 2rem !important;
    }

    /* Aesthetic Divider Line */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #ffffff66, transparent);
        margin-top: -10px;
        margin-bottom: 25px;
    }

    /* Title Styling */
    .glow-title {
        font-size: 42px !important;
        font-weight: 800 !important;
        text-align: center;
        color: #ffffff;
        text-shadow: 0 0 12px rgba(255,255,255,0.4);
        letter-spacing: 1px;
        margin-bottom: 5px;
        margin-top: -20px;
    }

    /* Base Fade-up Animation */
    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(25px) scale(0.95); filter: blur(4px); }
        70% { opacity: 0.8; transform: translateY(10px) scale(1); filter: blur(1px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }

    /* Staggered delays */
    .delay-1 { animation-delay: 0.0s; }
    .delay-2 { animation-delay: 0.25s; }
    .delay-3 { animation-delay: 0.50s; }

    .fade-in {
        opacity: 0;
        animation: fadeUp 1.2s ease-out forwards;
    }

    /* Premium Glassy Photo Frame */
    .photo-frame {
        position: relative;
        padding: 10px;
        border-radius: 22px;

        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);

        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.35),
            inset 0 0 12px rgba(255, 255, 255, 0.25);

        transition: 
            transform 0.45s ease,
            box-shadow 0.45s ease,
            filter 0.45s ease;
    }

    /* Hover Glow Lift */
    .photo-frame:hover {
        transform: scale(1.065) translateY(-8px);

        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.55),
            0 0 22px rgba(255, 255, 255, 0.75),
            inset 0 0 14px rgba(255, 255, 255, 0.35);
        filter: brightness(1.1);
    }

    /* Role Card */
    .card {
        background: rgba(255,255,255,0.88);
        padding: 14px;
        margin-top: 14px;
        border-radius: 14px;
        font-weight: 700;
        text-align: center;
        font-size: 17px;
        color: #222;

        border: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);

        opacity: 0;
        animation: fadeUp 1.2s ease-out forwards;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ----------------
st.markdown("<div class='glow-title'>👥 Group Members</div>", unsafe_allow_html=True)
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

# ---------------- COLUMNS ----------------
col1, col2, col3 = st.columns(3)

def show_member(column, image, name, role, delay_class):
    with column:
        encoded_img = image_to_base64(image)

        # Photo frame
        st.markdown(
            f"""
            <div class="photo-frame fade-in {delay_class}">
                <img src="data:image/jpeg;base64,{encoded_img}" 
                     style="width:100%; border-radius:14px;">
            </div>
            """,
            unsafe_allow_html=True
        )

        # Role Card
        st.markdown(
            f"<div class='card {delay_class}'>{name}<br><span style='font-weight:400; font-size:15px;'>{role}</span></div>",
            unsafe_allow_html=True
        )

# Display with staggered animation
show_member(col1, img1, "Member 1", "Project Leader", "delay-1")
show_member(col2, img2, "Member 2", "Research & Design", "delay-2")
show_member(col3, img3, "Member 3", "Developer", "delay-3")
