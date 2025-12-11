import streamlit as st

# =========================
#   PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Graph Theory Project",
    page_icon="🧠",
    layout="wide",
)

# =========================
#      THEME OPTIONS
# =========================

solid_themes = {
    "Light Blue": "#E3F2FD",
    "Soft Green": "#E8F5E9",
    "Warm Beige": "#FFF3E0",
    "Ice Gray": "#ECEFF1",
    "Soft Pink": "#FCE4EC",
}

gradient_themes = {
    "Sky Blue": "linear-gradient(135deg, #c9e9ff, #81c4ff)",
    "Purple Sunset": "linear-gradient(135deg, #e3a7ff, #9b51e0)",
    "Aqua Fresh": "linear-gradient(135deg, #d5fff7, #68e2c6)",
    "Warm Flame": "linear-gradient(135deg, #ffd6a5, #ff8fab)",
}

# =========================
#   SIDEBAR CONTROLS
# =========================

st.sidebar.title("🎨 Background Settings")

# DEFAULT MODE = DARK MODE
theme_type = st.sidebar.selectbox(
    "Choose Theme Mode:",
    ["Dark Mode", "Light Mode", "Solid Color", "Gradient", "Color Picker"],
    index=0  # THIS MAKES DARK MODE THE DEFAULT
)

# =========================
#   HELPER FUNCTIONS
# =========================

def get_text_color(bg_hex: str) -> str:
    """Automatically choose black or white text based on brightness."""
    bg_hex = bg_hex.lstrip("#")
    if len(bg_hex) != 6:
        return "black"
    r, g, b = tuple(int(bg_hex[i:i+2], 16) for i in (0, 2, 4))
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "black" if brightness > 155 else "white"


def build_css(background_style: str, bg_is_dark: bool) -> str:
    """Generate CSS for background and card components with safe contrast."""
    card_bg = "rgba(255,255,255,0.95)" if not bg_is_dark else "rgba(24,24,24,0.92)"
    card_text = "black" if not bg_is_dark else "white"
    subtle = "rgba(30,30,30,0.8)" if not bg_is_dark else "rgba(220,220,220,0.8)"

    return f"""
<style>
body, .stApp {{
    {background_style}
    background-size: cover;
    background-attachment: fixed;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

.card {{
    background: {card_bg};
    color: {card_text};
    padding: 20px 24px;
    border-radius: 16px;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.25);
    margin-bottom: 1.1rem;
}}

.card p, .card li {{
    color: {subtle};
    font-size: 0.95rem;
}}

.card h1, .card h2, .card h3 {{
    margin-top: 0;
    color: {card_text};
}}

.badge {{
    display: inline-block;
    padding: 5px 12px;
    font-size: 0.75rem;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    background: rgba(0,0,0,0.15);
    color: {card_text};
}}
</style>
"""


# =========================
#   BACKGROUND LOGIC
# =========================

bg_is_dark = False  # used to determine text color inside cards

if theme_type == "Dark Mode":
    background_style = "background-color: #0B0F19; color: white;"
    bg_is_dark = True

elif theme_type == "Light Mode":
    background_style = "background-color: #F4F4F5; color: black;"
    bg_is_dark = False

elif theme_type == "Solid Color":
    pick = st.sidebar.selectbox("Choose Solid Background:", list(solid_themes.keys()))
    bg = solid_themes[pick]
    text_color = get_text_color(bg)
    bg_is_dark = (text_color == "white")
    background_style = f"background-color: {bg}; color: {text_color};"

elif theme_type == "Gradient":
    pick = st.sidebar.selectbox("Choose Gradient:", list(gradient_themes.keys()))
    gradient_css = gradient_themes[pick]
    background_style = f"background-image: {gradient_css}; color: black;"
    bg_is_dark = False  # gradients assumed light

elif theme_type == "Color Picker":
    custom = st.sidebar.color_picker("Pick Background Color:", "#FFFFFF")
    text_color = get_text_color(custom)
    bg_is_dark = (text_color == "white")
    background_style = f"background-color: {custom}; color: {text_color};"


# =========================
#   APPLY CSS
# =========================
st.markdown(build_css(background_style, bg_is_dark), unsafe_allow_html=True)


# =========================
#        PAGE CONTENT
# =========================

# Hero Section
st.markdown(
    """
<div class="card">
    <span class="badge">Graph Theory</span>
    <h1>Introduction to Graph Theory</h1>
    <p>
        Graph theory is a branch of mathematics that studies structures made of 
        <strong>vertices (nodes)</strong> and <strong>edges (connections)</strong>. 
        It provides a powerful framework for analyzing and modeling networks in real-world systems.
    </p>
    <p>
        Examples include social networks, computer networks, transportation routes, 
        biological networks, and many more.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Basic concepts
st.markdown(
    """
<div class="card">
    <h2>Basic Concepts</h2>
    <ul>
        <li><strong>Vertex (Node):</strong> The basic unit in a graph.</li>
        <li><strong>Edge:</strong> A connection between two vertices.</li>
        <li><strong>Degree:</strong> Number of edges connected to a vertex.</li>
        <li><strong>Path:</strong> A sequence of connected vertices.</li>
        <li><strong>Cycle:</strong> A path that begins and ends at the same vertex.</li>
        <li><strong>Connected Graph:</strong> Every pair of vertices is reachable.</li>
    </ul>
</div>
""",
    unsafe_allow_html=True,
)

# Applications
st.markdown(
    """
<div class="card">
    <h2>Applications of Graph Theory</h2>
    <ul>
        <li><strong>Social Networks:</strong> Modeling friendships and community structures.</li>
        <li><strong>Logistics & Routing:</strong> Shortest paths, delivery routes, and optimization.</li>
        <li><strong>Computer Networks:</strong> Understanding connections between servers and devices.</li>
        <li><strong>Machine Learning:</strong> Graph embeddings, clustering, and recommendation systems.</li>
    </ul>
</div>
""",
    unsafe_allow_html=True,
)
