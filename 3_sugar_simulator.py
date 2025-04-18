import streamlit as st
import base64

st.set_page_config(
    page_title="Genes Don't Eat Sugar",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def set_page(new_page):
    st.session_state.page = new_page
    st.rerun()

def restart_app():
    st.session_state.clear()
    st.rerun()

if "page" not in st.session_state:
    st.session_state.page = "home"
    st.session_state.character = None

def get_base64_img(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def display_character():
    c = st.session_state.character
    if c == "Grace":
        st.image("assets/grace_icon.png", width=150)
    elif c == "Brian":
        st.image("assets/brian_icon.png", width=150)

# background
bg = get_base64_img("assets/bg_image.png")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    html, body, [data-testid="stApp"] {{
      margin:0; padding:0; height:100%;
      background:none;
      font-family:'Fredoka One',cursive!important;
      overflow-x:hidden;
    }}
    body::before {{
      content:""; position:fixed; top:0; left:0;
      width:100vw; height:100vh;
      background-image:url("data:image/png;base64,{bg}");
      background-size:cover;
      background-repeat:no-repeat;
      background-position:center top;
      background-attachment:fixed;
      z-index:-1;
    }}
    .block-container {{ padding-top:150px; background-color:rgba(0,0,0,0); }}
    h1,h2,h3,h4,h5,h6,p,div {{ color:black!important; text-align:center; }}
    .stButton>button {{
      border-radius:12px;
      background-color:transparent;
      border:2px solid black;
      color:black;
      font-weight:bold;
    }}
    label, .stRadio>div>label {{ color:black!important; font-weight:500; }}
    </style>
""", unsafe_allow_html=True)

page = st.session_state.page

# home screen
if page == "home":
    title_gif   = get_base64_img("assets/simulatortitle.gif")
    welcome_png = get_base64_img("assets/welcome_text.png")
    st.markdown(f"""
      <div style="text-align:center; margin-top:-60px">
        <img src="data:image/gif;base64,{title_gif}" style="width:500px;max-width:90%"/>
        <br><br>
        <img src="data:image/png;base64,{welcome_png}" style="width:800px;max-width:100%"/>
      </div>
    """, unsafe_allow_html=True)
    if st.button("Start Exploring"):
        set_page("character")

 # character selection
elif page == "character":
    choose_png = get_base64_img("assets/choose.png")
    st.markdown(f"""
      <div style="text-align:center; margin-top:-30px">
        <img src="data:image/png;base64,{choose_png}" style="width:500px;max-width:90%"/>
      </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.image("assets/grace_icon.png", width=200)
    with c2: st.image("assets/brian_icon.png", width=200)

    sel = st.radio("Select a character:", ["-- Choose one --", "Grace", "Brian"])
    if st.button("Next"):
        if sel == "-- Choose one --":
            st.error("Please pick Grace or Brian!")
        else:
            st.session_state.character = sel
            set_page("morning")


elif page == "morning":
    display_character()
    st.markdown(f"<h4>How does <em>{st.session_state.character}</em> start their morning?</h4>", unsafe_allow_html=True)
    morning_opts = ["-- Pick one --",
                    "Wake up early and go walk outside for 10 minutes",
                    "Scroll on TikTok for hours"]
    choice = st.radio("", morning_opts)

    if choice == "Wake up early and go walk outside for 10 minutes":
        st.image("assets/grace_walking.gif" if st.session_state.character=="Grace" else "assets/brian_walk.gif")
    elif choice == "Scroll on TikTok for hours":
        st.image("assets/grace_tiktok.gif" if st.session_state.character=="Grace" else "assets/brian_tiktok.gif")

    if st.button("Next"):
        if choice.startswith("--"):
            st.error("You have to choose!")
        else:
            st.session_state.morning_choice = choice
            set_page("food")


elif page == "food":
    display_character()
    st.markdown(f"<p>What does <em>{st.session_state.character}</em> eat for breakfast?</p>", unsafe_allow_html=True)
    food_opts = ["-- Pick one --",
                 "Healthy smoothie with fruits and greens",
                 "Sugary cereal"]
    choice = st.radio("", food_opts)

    if choice == "Healthy smoothie with fruits and greens":
        st.image("assets/grace_smoothie.gif" if st.session_state.character=="Grace" else "assets/brian_smoothie.gif")
    elif choice == "Sugary cereal":
        st.image("assets/grace_cereal.gif" if st.session_state.character=="Grace" else "assets/brian_cereal.gif")

    if st.button("Next"):
        if choice.startswith("--"):
            st.error("Choose a breakfast!")
        else:
            st.session_state.food_choice = choice
            set_page("stress")


elif page == "stress":
    display_character()
    st.markdown(f"*{st.session_state.character}*'s homework is stressing them out! How do they respond?")
    stress_opts = ["-- Pick one --",
                   "Take a short break and read a couple pages in their book",
                   "Eat a bag of salty chips"]
    choice = st.radio("", stress_opts)

    if choice == "Take a short break and read a couple pages in their book":
        st.image("assets/grace_read.gif" if st.session_state.character=="Grace" else "assets/brian_read.gif")
    elif choice == "Eat a bag of salty chips":
        st.image("assets/grace_chips.gif" if st.session_state.character=="Grace" else "assets/brian_chips.gif")

    if st.button("Next"):
        if choice.startswith("--"):
            st.error("Pick a stress reliever!")
        else:
            st.session_state.stress_choice = choice
            set_page("social")


elif page == "social":
    display_character()
    st.markdown(f"How does *{st.session_state.character}* spend time with friends?")
    social_opts = ["-- Pick one --",
                   "Play tennis or eat a fulfilling meal",
                   "Scroll on social media"]
    choice = st.radio("", social_opts)

    if choice == "Play tennis or eat a fulfilling meal":
        st.image("assets/grace_tennis.gif" if st.session_state.character=="Grace" else "assets/brian_tennis.gif")
    elif choice == "Scroll on social media":
        st.image("assets/grace_scroll.gif" if st.session_state.character=="Grace" else "assets/brian_scroll.gif")

    if st.button("Next"):
        if choice.startswith("--"):
            st.error("Pick something fun!")
        else:
            st.session_state.social_choice = choice
            set_page("evening")


elif page == "evening":
    display_character()
    st.markdown(f"How does *{st.session_state.character}* wind down in the evening?")
    evening_opts = ["-- Pick one --",
                    "Journal their thoughts and relax with their family",
                    "Stay up till 2am on their phone"]
    choice = st.radio("", evening_opts)

    if choice == "Journal their thoughts and relax with their family":
        st.image("assets/grace_journal.gif" if st.session_state.character=="Grace" else "assets/brian_journal.gif")
    elif choice == "Stay up till 2am on their phone":
        st.image("assets/grace_phone.gif" if st.session_state.character=="Grace" else "assets/brian_phone.gif")

    if st.button("Next"):
        if choice.startswith("--"):
            st.error("Pick an evening routine!")
        else:
            st.session_state.evening_choice = choice
            set_page("result")


elif page == "result":
    display_character()

    POINTS = {
      "morning_choice": {
        "Wake up early and go walk outside for 10 minutes": 2,
        "Scroll on TikTok for hours": -2,
      },
      "food_choice": {
        "Healthy smoothie with fruits and greens": 2,
        "Sugary cereal": -1,
      },
      "stress_choice": {
        "Take a short break and read a couple pages in their book": 1,
        "Eat a bag of salty chips": -1,
      },
      "social_choice": {
        "Play tennis or eat a fulfilling meal": 3,
        "Scroll on social media": -3,
      },
      "evening_choice": {
        "Journal their thoughts and relax with their family":1,
        "Stay up till 2am on their phone": -2,
      },
    }

    picks = {
      "morning_choice": st.session_state.morning_choice,
      "food_choice": st.session_state.food_choice,
      "stress_choice": st.session_state.stress_choice,
      "social_choice": st.session_state.social_choice,
      "evening_choice": st.session_state.evening_choice,
    }

    # compute
    breakdown = {k: POINTS[k][picks[k]] for k in picks}
    total = sum(breakdown.values())


    if total >= 6:
        st.image("assets/result_excellent.gif")
    elif total >= 0:
        st.image("assets/result_okay.gif")
    else:
        st.image("assets/result_oof.gif")

    if st.button("Start Over!"):
        restart_app()
