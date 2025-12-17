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

# Language toggle
lang = st.sidebar.selectbox("Language:", ["English", "Bahasa Indonesia"], index=0)

# Theme mode
theme_type = st.sidebar.selectbox(
    "Choose Theme Mode:",
    ["Dark Mode", "Light Mode", "Solid Color", "Gradient", "Color Picker"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("🧩 Card Options")

# NEW: Additional sidebar options (card styling)
card_radius = st.sidebar.slider("Card Radius", min_value=10, max_value=30, value=16, step=1)
card_opacity = st.sidebar.slider("Card Opacity", min_value=0.75, max_value=1.00, value=0.95, step=0.01)
shadow_strength = st.sidebar.slider("Shadow Strength", min_value=0.10, max_value=0.45, value=0.25, step=0.01)

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
    # Card opacity controlled by sidebar
    if bg_is_dark:
        card_bg = f"rgba(24,24,24,{card_opacity})"
        card_text = "white"
        subtle = "rgba(220,220,220,0.82)"
    else:
        card_bg = f"rgba(255,255,255,{card_opacity})"
        card_text = "black"
        subtle = "rgba(30,30,30,0.78)"

    return f"""
<style>
body, .stApp {{
    {background_style}
    background-size: cover;
    background-attachment: fixed;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

.block-container {{
    max-width: 1100px;
}}

.card {{
    background: {card_bg};
    color: {card_text};
    padding: 20px 24px;
    border-radius: {card_radius}px;
    box-shadow: 0px 4px 18px rgba(0,0,0,{shadow_strength});
    margin-bottom: 1.1rem;
}}

.card p, .card li {{
    color: {subtle};
    font-size: 0.95rem;
    line-height: 1.6;
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
bg_is_dark = False

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
    bg_is_dark = False

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
#   CONTENT (BILINGUAL)
# =========================
content = {
    "English": {
        "badge": "Graph Theory",
        "title": "Introduction to Graph Theory",
        "p1": """Graph theory is a branch of mathematics that studies structures made of
                 <strong>vertices (nodes)</strong> and <strong>edges (connections)</strong>.
                 It provides a powerful framework for analyzing and modeling networks in real-world systems.""",
        "p2": """Examples include social networks, computer networks, transportation routes,
                 biological networks, and many more.""",
        "basic_title": "Basic Concepts",
        "basic_list": [
            "<strong>Vertex (Node):</strong> The basic unit in a graph.",
            "<strong>Edge:</strong> A connection between two vertices.",
            "<strong>Degree:</strong> Number of edges connected to a vertex.",
            "<strong>Path:</strong> A sequence of connected vertices.",
            "<strong>Cycle:</strong> A path that begins and ends at the same vertex.",
            "<strong>Connected Graph:</strong> Every pair of vertices is reachable.",
        ],
        "app_title": "Applications of Graph Theory",
        "app_list": [
            "<strong>Social Networks:</strong> Modeling friendships and community structures.",
            "<strong>Logistics & Routing:</strong> Shortest paths, delivery routes, and optimization.",
            "<strong>Computer Networks:</strong> Understanding connections between servers and devices.",
            "<strong>Machine Learning:</strong> Graph embeddings, clustering, and recommendation systems.",
        ],
    },
    "Bahasa Indonesia": {
        "badge": "Teori Graf",
        "title": "Pengenalan Teori Graf",
        "p1": """Teori graf adalah cabang matematika yang mempelajari struktur yang terdiri dari
                 <strong>simpul (vertex/node)</strong> dan <strong>sisi (edge/hubungan)</strong>.
                 Teori ini menjadi kerangka yang kuat untuk menganalisis dan memodelkan jaringan pada sistem nyata.""",
        "p2": """Contohnya antara lain jejaring sosial, jaringan komputer, rute transportasi,
                 jaringan biologis, dan masih banyak lagi.""",
        "basic_title": "Konsep Dasar",
        "basic_list": [
            "<strong>Simpul (Vertex/Node):</strong> Unit dasar dalam graf.",
            "<strong>Sisi (Edge):</strong> Hubungan yang menghubungkan dua simpul.",
            "<strong>Derajat (Degree):</strong> Jumlah sisi yang terhubung ke sebuah simpul.",
            "<strong>Lintasan (Path):</strong> Urutan simpul yang saling terhubung.",
            "<strong>Siklus (Cycle):</strong> Lintasan yang berawal dan berakhir pada simpul yang sama.",
            "<strong>Graf Terhubung (Connected Graph):</strong> Setiap pasangan simpul dapat dicapai.",
        ],
        "app_title": "Penerapan Teori Graf",
        "app_list": [
            "<strong>Jejaring Sosial:</strong> Memodelkan pertemanan dan struktur komunitas.",
            "<strong>Logistik & Rute:</strong> Jalur terpendek, rute pengiriman, dan optimasi.",
            "<strong>Jaringan Komputer:</strong> Memahami koneksi antar server dan perangkat.",
            "<strong>Pembelajaran Mesin:</strong> Graph embedding, clustering, dan sistem rekomendasi.",
        ],
    },
}

lang = "English"  # atau "Bahasa Indonesia"
c = content[lang]

# =========================
#        PAGE CONTENT
# =========================
st.markdown(
    f"""
<div class="card">
    <span class="badge">{c["badge"]}</span>
    <h1>{c["title"]}</h1>
    <p>{c["p1"]}</p>
    <p>{c["p2"]}</p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="card">
    <h2>{c["basic_title"]}</h2>
    <ul>
        {''.join([f'<li>{item}</li>' for item in c["basic_list"]])}
    </ul>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="card">
    <h2>{c["app_title"]}</h2>
    <ul>
        {''.join([f'<li>{item}</li>' for item in c["app_list"]])}
    </ul>
</div>
""",
    unsafe_allow_html=True,
)
