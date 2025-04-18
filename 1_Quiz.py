import streamlit as st
import base64

# setup
st.set_page_config(
    page_title="About Me",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# background
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64("assets/bg_image.png")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

html, body, [data-testid="stApp"] {{
    margin: 0;
    padding: 0;
    font-family: 'Fredoka One', cursive !important;
    background: none !important;
    overflow-x: hidden;
}}

body::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-image: url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center top;
    background-attachment: fixed;
    z-index: -1;
}}

.about-text {{
    background-color: rgba(255, 255, 255, 0.75);
    padding: 2rem;
    border-radius: 20px;
    font-size: 18px;
    line-height: 1.6;
    color: #222;
    text-align: center;
    max-width: 700px;
    margin: auto;
    margin-top: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}
</style>
""", unsafe_allow_html=True)

st.image("assets/aboutme.png", width=500)

st.image("assets/textabout.png", use_container_width=True)
st.image("assets/aboutproject.png", use_container_width=True)
st.image("assets/technicalproject.png", use_container_width=True)
