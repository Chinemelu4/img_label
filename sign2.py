import pickle
from pathlib import Path
import os
from PIL import Image
import random

import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# --- USER AUTHENTICATION ---
names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker", "rmiller"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {
    "usernames":{
        "pparker":{
            "name":"Peter Parker",
            "password":hashed_passwords[0]
            },
        "rmiller":{
            "name":"Rebecca Miller",
            "password":hashed_passwords[1]
            }            
        }
    }
authenticator = stauth.Authenticate(credentials, "sales_dashboard", "auth", cookie_expiry_days=0)

#BASE_PATH = st.text_input("num")
name, authentication_status, username = authenticator.login("Login", "main")


if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")




if authentication_status:
    state = st.session_state
    c= st.file_uploader('ff')
    bp = st.text_input("PATH")

    if (not bp):
        st.info('The annotation will begin, once you entered the folder path.')
        st.stop()
    
    BASE_PATH = bp
    OPTIONS = ["Nystagmus", "Meniere's Disease", "BPPV"]

    if "annotations" not in state:
        state.annotations = {}
        state.files = os.listdir(BASE_PATH)
        state.current_file = state.files[0]


    def annotate(label):
        state.annotations[state.current_file] = label
        if state.files:
            state.current_file = random.choice(state.files)
            state.files.remove(state.current_file)


    st.header("Dataset annotation")

    if state.files:
        selected_file = state.current_file
        filename = os.path.join(BASE_PATH, selected_file)
        st.write(f"Current file: {selected_file}")
        image = Image.open(filename)
        st.image(image)

        c = st.columns(len(OPTIONS))
        for idx, option in enumerate(OPTIONS):
            c[idx].button(f"{option}", on_click=annotate, args=(option,))

    else:
        st.info("Everything annotated.")

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")

    st.info(f"Annotated: {len(state.annotations)}, Remaining: {len(state.files)}")

    st.sidebar.write([f"{k},{v}" for k, v in state.annotations.items()])



    st.download_button(
        "Download annotations as CSV",
        "\n".join([f"{k},{v}" for k, v in state.annotations.items()]),
        file_name="export.csv",
    )
    

    # ---- SIDEBAR ----
    

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 450px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 500px;
            margin-left: -500px;
            }
            </style>
            """,
            unsafe_allow_html=True)

    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
