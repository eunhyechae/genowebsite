import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64

st.set_page_config(
    page_title="BMI Health Explorer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# background
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64("assets/bg_image.png")

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    html, body, [data-testid="stApp"] {{
        margin: 0;
        padding: 0;
        height: 100%;
        background: none;
        font-family: 'Fredoka One', cursive !important;
        overflow-x: hidden;
    }}

    body::before {{
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100vw;
        height: 100vh;
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center top;
        background-attachment: fixed;
        z-index: -1;
    }}

    .block-container {{
        padding-top: 100px;
        background-color: rgba(0, 0, 0, 0);
    }}

    h1, h2, h3, p {{
        color: white !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# setup
st.image("assets/graphtitle.png", use_container_width=True)
st.image("assets/graphintro.png", use_container_width=True)


# data
@st.cache_data
def load_data():
    df = pd.read_csv("EPID_521_lab_data.csv")

    df = df.rename(columns={
        'BMXBMI': 'BMI',
        'DMDEDUC2': 'Education',
        'DIQ010': 'Diabetes',
        'RIDRETH1': 'Race',
        'DBQ700': 'SelfRatedHealth'
    })

    return df 

df = load_data()

df = df.dropna(subset=['BMI', 'Education', 'Diabetes', 'Race', 'SelfRatedHealth'])
st.success(f"✅ Final rows after dropping nulls: {len(df)}")

# bmi cutoff
bmi_cutoff = 30
bmi_max = df['BMI'].max()
if pd.isna(bmi_max) or bmi_max <= bmi_cutoff:
    bmi_max = bmi_cutoff + 10
df['BMI_Group'] = pd.cut(df['BMI'], bins=[0, bmi_cutoff, bmi_max], labels=['Lower BMI', 'High BMI'])

# education
st.markdown("""
<div style="font-size: 30px; color: black; font-family: 'Fredoka One', cursive; margin-top: 1rem;">
🎓 Education Distribution by BMI Group
</div>
""", unsafe_allow_html=True)


edu_order = ['NoHighSchool', 'SomeHighSchool', 'HighSchool', 'SomeCollege', 'College']
df['Education'] = pd.Categorical(df['Education'], categories=edu_order, ordered=True)
edu_counts = df.groupby(['BMI_Group', 'Education']).size().unstack().fillna(0)

col1, col2 = st.columns([2, 2], gap="large")

with col1:
    if not edu_counts.empty:
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        edu_counts.T.plot(kind='bar', ax=ax1)
        ax1.set_ylabel("Number of People")
        ax1.set_xlabel("Education Level")
        ax1.set_title("Education vs. BMI Group")
        ax1.legend(title="BMI Group", bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig1)
    else:
        st.warning("Not enough data to show Education vs. BMI.")

with col2:
    st.image("assets/educationnote1.png", use_container_width=True)


# diabetes
st.markdown("""
<div style="font-size: 30px; color: black; font-family: 'Fredoka One', cursive; margin-top: 2rem;">
BMI by Diabetes Status
</div>
""", unsafe_allow_html=True)

valid_diabetes = ['Yes', 'No', 'Borderline']
df = df[df['Diabetes'].isin(valid_diabetes)]
df['Diabetes'] = pd.Categorical(df['Diabetes'], categories=['No', 'Yes', 'Borderline'], ordered=True)

diab_df = df[['BMI', 'Diabetes']].dropna()

# columns
col1, col2 = st.columns([2, 2], gap="large")

with col1:
    if not diab_df.empty:
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=diab_df, x='Diabetes', y='BMI', palette='Set2', ax=ax2)
        ax2.set_ylim(0, 60)
        ax2.set_ylabel("BMI")
        ax2.set_title("BMI Distribution by Diabetes Status")
        st.pyplot(fig2)
    else:
        st.warning("no data for Diabetes vs. BMI.")

with col2:
    st.image("assets/diabetesnote.png", use_container_width=True)  # You can swap in width=700 if needed


# race/ethncity 
st.markdown("""
<div style="font-size: 30px; color: black; font-family: 'Fredoka One', cursive; margin-top: 2rem;">
BMI by Race/Ethnicity
</div>
""", unsafe_allow_html=True)

race_order = ['White', 'Other', 'MexicanAmerican', 'OtherHispanic', 'Black']
df['Race'] = pd.Categorical(df['Race'], categories=race_order, ordered=True)
race_df = df[['Race', 'BMI']].dropna()

col1, col2 = st.columns([2, 2], gap="large")

with col1:
    if not race_df.empty:
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=race_df, x='Race', y='BMI', palette='Set2', ax=ax3)
        ax3.set_ylim(0, 60)
        ax3.set_ylabel("BMI")
        ax3.set_xlabel("Race/Ethnicity")
        ax3.set_title("BMI Distribution by Race/Ethnicity")
        st.pyplot(fig3)
    else:
        st.warning("no data for Race vs. BMI.")

with col2:
    st.image("assets/racenote.png", use_container_width=True)


# set rate
st.markdown("""
<div style="font-size: 30px; color: black; font-family: 'Fredoka One', cursive; margin-top: 2rem;">
BMI by Self-Rated Health
</div>
""", unsafe_allow_html=True)

health_order = ['Poor', 'Fair', 'Good', 'VeryGood', 'Excellent']
df['SelfRatedHealth'] = pd.Categorical(df['SelfRatedHealth'], categories=health_order, ordered=True)
health_df = df[['SelfRatedHealth', 'BMI']].dropna()

col1, col2 = st.columns([2, 2], gap="large")

with col1:
    if not health_df.empty:
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=health_df, x='SelfRatedHealth', y='BMI', palette='Spectral', ax=ax4)
        ax4.set_ylim(0, 60)
        ax4.set_ylabel("BMI")
        ax4.set_xlabel("Self-Rated Health")
        ax4.set_title("BMI vs. Self-Rated Health")
        st.pyplot(fig4)
    else:
        st.warning("No data for Self-Rated Health vs. BMI.")

with col2:
    st.image("assets/healthnote.png", use_container_width=True)


