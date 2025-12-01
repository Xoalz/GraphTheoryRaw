import streamlit as st

# =========================
#      THEME OPTIONS
# =========================

# Solid background themes (soft but readable)
solid_themes = {
    "Light Blue": "#E3F2FD",
    "Soft Green": "#E8F5E9",
    "Warm Beige": "#FFF3E0",
    "Ice Gray": "#ECEFF1",
    "Soft Pink": "#FCE4EC",
}

# Gradient themes
gradient_themes = {
    "Sky Blue": "linear-gradient(135deg, #c9e9ff, #81c4ff)",
    "Purple Sunset": "linear-gradient(135deg, #e3a7ff, #9b51e0)",
    "Aqua Fresh": "linear-gradient(135deg, #d5fff7, #68e2c6)",
    "Warm Flame": "linear-gradient(135deg, #ffd6a5, #ff8fab)",
}

# =========================
#   SIDEBAR CONTROLS
# =========================
st.sidebar.title("🎨 Theme Settings")

theme_type = st.sidebar.radio(
    "Select Theme Type:",
    ["Solid Color", "Gradient", "Dark Mode", "Custom Color"],
)

# =========================
#   BACKGROUND LOGIC
# =========================

def get_text_color(bg_hex):
    """Automatically decide black or white text for contrast."""
    bg_hex = bg_hex.lstrip("#")
    r, g, b = tuple(int(bg_hex[i:i+2], 16) for i in (0, 2, 4))
    brightness = (r*299 + g*587 + b*114) / 1000
    return "black" if brightness > 155 else "white"

if theme_type == "Solid Color":
    selected = st.sidebar.selectbox("Choose Background Color:", list(solid_themes.keys()))
    bg_color = solid_themes[selected]
    text_color = get_text_color(bg_color)

    background_style = f"background-color: {bg_color}; color: {text_color};"

elif theme_type == "Gradient":
    selected = st.sidebar.selectbox("Choose Gradient Theme:", list(gradient_themes.keys()))
    background_style = f"background-image: {gradient_themes[selected]}; color: black;"

elif theme_type == "Dark Mode":
    background_style = "background-color: #121212; color: white;"

elif theme_type == "Custom Color":
    custom = st.sidebar.color_picker("Pick Background Color:", "#FFFFFF")
    text_color = get_text_color(custom)
    background_style = f"background-color: {custom}; color: {text_color};"

# =========================
#   APPLY CSS
# =========================
st.markdown(
    f"""
    <style>
    .stApp {{
        {background_style}
        background-size: cover;
        background-attachment: fixed;
    }}

    .fade-in {{
        animation: fadeIn 1.2s ease-in-out;
    }}

    @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Always-readable content boxes */
    .title-box {{
        background: rgba(255, 255, 255, 0.80);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
    }}

    .content-box {{
        background: rgba(255, 255, 255, 0.75);
        padding: 20px;
        border-radius: 12px;
        margin-top: 12px;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.2);
    }}

    /* Dark mode box override */
    {" .title-box, .content-box { background: rgba(50,50,50,0.7); color: white; }" if theme_type == "Dark Mode" else ""}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
#        CONTENT
# =========================
st.markdown("<div class='title-box fade-in'>", unsafe_allow_html=True)
st.title("Welcome to Our Graph Theory Project")
st.markdown("### Interactive Learning Through Visualization")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='content-box fade-in'>", unsafe_allow_html=True)
st.subheader("📘 What is Graph Theory?")
st.markdown(
    """
Graph Theory studies **nodes (vertices)** and **connections (edges)**  
and helps analyze:

- Social networks  
- Communication systems  
- Routes & transportation  
- Data structures  
- Network analysis  

Explore graph concepts visually below!
"""
)
st.markdown("</div>", unsafe_allow_html=True)
