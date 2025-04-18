import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline
import torch 
import base64
import os  

# dont show actual token
hf_token = st.secrets["HF_TOKEN"]


# hugging face ?

@st.cache_resource
def load_geno_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    return tokenizer, model

tokenizer, model = load_geno_model()


query_params = st.query_params
if "page" in query_params:
    st.switch_page(query_params["page"])

def set_page(new_page):
    st.session_state.page = new_page
    st.rerun()

# page set
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

# all the pngs , etc
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64("assets/bg_image.png")
slides = [
    "assets/geno1.png",
    "assets/geno2.png",
    "assets/geno3.png",
    "assets/geno5.png",
]
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
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    background-image: url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center top;
    background-attachment: fixed;
    z-index: -1;
}}

.title-corner {{
    position: fixed;
    top: 10px;
    left: 10px;
    font-size: 12px;
    color: black;
    z-index: 10;
}}

.stButton > button {{
    background-color: transparent !important;
    border: 2px solid black !important;
    color: black !important;
    font-weight: bold;
    border-radius: 12px !important;
    padding: 0.6rem 1.4rem !important;
    font-family: 'Fredoka One', cursive !important;
    box-shadow: none !important;
}}

.right-block-buttons .stButton > button {{
    display: block !important;
    width: 100% !important;
    background-color: #b2d8d8 !important;
    border: none !important;
    padding: 1rem !important;
    margin-bottom: 1rem !important;
    color: black !important;
    font-weight: bold;
    border-radius: 8px !important;
}}

.stTextInput input, .stTextArea textarea {{
    font-family: 'Fredoka One', cursive !important;
    font-size: 16px !important;
    color: black !important;
    background-color: white !important;
}}

div[data-testid="stMarkdownContainer"] *, 
div[data-testid="stMarkdownContainer"] p,
.stMarkdown p,
p {{
    color: black !important;
    background-color: transparent !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 16px !important;
    margin: 0 0 10px 0 !important;
    padding: 0 !important;
}}
</style>
""", unsafe_allow_html=True)


# title
st.markdown('<div class="title-corner">Genetics and Games</div>', unsafe_allow_html=True)

# slideshow
if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# layout
left_col, right_col = st.columns([3,2])

with left_col:
    slide_path = slides[st.session_state.slide_index]
    slide_b64 = get_base64_image(slide_path)
    st.markdown(f"""
    <div style="width: 650px; height: 650px; border-radius: 16px; background-color: white;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1); display: flex;
                justify-content: center; align-items: center; margin-bottom: 1rem;">
        <img src="data:image/png;base64,{slide_b64}" style="width:100%; height:100%; object-fit:contain;" />
    </div>
    """, unsafe_allow_html=True)

# slideshow nav?
prev_col, next_col = st.columns(2)
with prev_col:
    if st.button("←"):
        st.session_state.slide_index = (st.session_state.slide_index - 1) % len(slides)
with next_col:
    if st.button("→"):
        st.session_state.slide_index = (st.session_state.slide_index + 1) % len(slides)

# movie
if "show_movie" not in st.session_state:
    st.session_state.show_movie = False
if st.button("Watch Movie"):
    st.session_state.show_movie = not st.session_state.show_movie
if st.session_state.show_movie:
    st.markdown("""
    <div style="display: flex; justify-content: flex-start; margin-top:1rem;">
        <iframe width="800" height="550" src="https://www.youtube.com/embed/8m6hHRlKwxY"
                frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    st.image("assets/MeetGeno.png", width=500)

    def image_button(image_path, link, width="210px"):
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"""
        <a href="{link}">
            <img src="data:image/png;base64,{encoded}" style="width:{width}; margin-bottom: 1rem;" />
        </a>
        """
    st.markdown(image_button("assets/about.png", "?page=pages/1_Quiz.py"), unsafe_allow_html=True)
    st.markdown(image_button("assets/graphs.png", "?page=pages/2_NHANES_DataExplorer.py"), unsafe_allow_html=True)
    st.markdown(image_button("assets/simulations.png", "?page=pages/3_sugar_simulator.py"), unsafe_allow_html=True)
    st.markdown(image_button("assets/worksheet.png", "https://www.amoebasisters.com/uploads/2/1/9/0/21902384/video_recap_of_dna_chromosomes_genes_proteins_by_amoeba_sisters_2018.pdf"), unsafe_allow_html=True)
    st.markdown(image_button("assets/videos.png", "https://www.youtube.com/playlist?list=PLz2ukDu2AKNNU1D3DIndtsdClynfVX6GT"), unsafe_allow_html=True)

import requests

# geno chat
st.image("assets/askgeno.png", width=300)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "", key="user_input")

if st.button("Send", key="send_button"):
    if user_input:
        st.session_state.chat_history.append(("You", user_input))

        system_prompt = (
            "You are Geno, a friendly and knowledgeable chatbot who explains genetics, "
            "DNA, heredity, and health to kids in a simple, kind, and positive way."
        )

        full_prompt = system_prompt + "\n\n"
        for speaker, msg in st.session_state.chat_history:
            full_prompt += f"{speaker}: {msg}\n"
        full_prompt += "Geno:"

        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
            headers={"Authorization": f"Bearer {os.environ['HF_TOKEN']}"},
            json={"inputs": full_prompt, "parameters": {"max_new_tokens": 100}}
        )

        if response.status_code == 200:
            bot_reply = response.json()[0]["generated_text"].split("Geno:")[-1].strip()
            st.session_state.chat_history.append(("Geno", bot_reply))
        else:
            st.session_state.chat_history.append(("Geno", "Oops! Geno’s feeling shy today 😔"))

# chat history
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"<div style='background:#ffffff;padding:0.6rem;border-radius:10px;margin-bottom:0.4rem'><strong>{speaker}:</strong> {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background:#d8f3dc;padding:0.6rem;border-radius:10px;margin-bottom:0.4rem'><strong>{speaker}:</strong> {msg}</div>", unsafe_allow_html=True)
