import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime
from google.cloud.firestore import Client
from google.cloud import firestore
from streamlit_js_eval import streamlit_js_eval
from threading import Event
import time
import os
from annotated_text import annotated_text


st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)
st.title("TRA1LM1NE Marketplace",
         help = 'Orders will be verified by the admins',
         anchor=False)


@st.cache_resource
def get_db():
    creds_dict = {
        "type": os.environ["FIREBASE_TYPE"],
        "project_id": os.environ["FIREBASE_PROJECT_ID"],
        "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
        "private_key": os.environ["FIREBASE_PRIVATE_KEY"],
        "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
        "client_id": os.environ["FIREBASE_CLIENT_ID"],
        "auth_uri": os.environ["FIREBASE_AUTH_URI"],
        "token_uri": os.environ["FIREBASE_TOKEN_URI"],
        "auth_provider_x509_cert_url": os.environ["FIREBASE_AUTH_PROVIDER_CERT_URL"],
        "client_x509_cert_url": os.environ["FIREBASE_CLIENT_CERT_URL"],
        "universe_domain": os.environ["FIREBASE_UNIVERSE_DOMAIN"],
    }
    db = firestore.Client.from_service_account_info(creds_dict)
    return db


db = get_db()

# def get_db():
#     db =  firestore.Client.from_service_account_json("pages/firebase-key.json")
#     return db

# db = get_db()


def post_bounty(db, id, title, description, address, complexity, value, hash):
    payload = {
        "id": id,
        "title": title,
        "description": description,
        "address": address,
        "complexity": complexity,
        "value": value,
        "hash": hash,
    }
    doc_ref = db.collection("marketplace").document(str(id))
    doc_ref.set(payload)




flag = 1

col1, col2, col3 = st.columns([1, 1, 5])
with col1:

    @st.dialog("Post your question", width="large")
    def bounty_dialog():
        with st.form("bounty_form"):
            title = st.text_input("Title...")
            description = st.text_area("Description...")
            complexity = st.select_slider("Complexity", options=["Low", "Medium", "High"])
            address = st.text_input("Address")
            value = st.number_input("Value", min_value=10, max_value=1000, value=100)
            hash_value = st.text_input("Hash", placeholder="Send the value to the address and paste the transaction hash here")

            # Generate a unique ID based on complexity and date
            generated_id = datetime.now().strftime("%d%m%Y%H%M%S")

            submitted = st.form_submit_button("Submit", type='primary')

            if submitted:
                st.session_state.bounty = {
                    "id": generated_id,
                    "title": title,
                    "description": description,
                    "address": address,
                    "complexity": complexity,
                    "value": value,
                    "hash": hash_value,
                }
               
                st.rerun()

    if "bounty" not in st.session_state:
        if st.button("PLACE BOUNTY", use_container_width=True):
            bounty_dialog()
    if "bounty" in st.session_state:
        b = st.session_state.bounty
        id_sessioned = b["id"]
        post_bounty(db, b["id"], b["title"], b["description"], b["address"], b["complexity"], b["value"], b["hash"])
        flag = 0


with col2:

    @st.dialog("Publish your solution",width="large")
    def publish():
        id_pub = st.text_input("Investigation ID")
        title = st.text_input("Key Findings",placeholder="Describe within a few sentences")
        description = st.text_area("Description...", placeholder="Kindly provide a brief description of your findings")
        address = st.text_input("Your address", placeholder="Enter your polygon wallet address")

        if st.button("Submit", type='primary'):
            st.session_state.publish = {"title": title, 
                                    "address": address,
                                    "description": description,
                                    "id_pub": id_pub,
                                }
            st.rerun()

    # if "publish" not in st.session_state:
    if st.button("YOUR INTEL", use_container_width=True):
        publish()
    # else:
        # st.success(f"Title: {st.session_state.publish['title']} Address: {st.session_state.publish['address']} Description: {st.session_state.publish['description']} id_pub: {st.session_state.publish['id_pub']}")
    if "publish" in st.session_state:
        flag = 2

if(flag == 0):
    st.success("Your bounty has been placed successfully. Refresh to submit again...")
    with col1 :
        st.info(f'Unique ID: {id_sessioned}')
elif(flag == 2):
    st.success("Your Investigation details will be reviewed within 24 hours")


with col3:
    with st.expander("What is TRA1LM1NE Marketplace?"):
        st.write("TRA1LM1NE Marketplace is a platform for sharing and exchanging knowledge and data. Post a bounty to get answers to your questions or publish your findings to earn TRA1LS tokens.")
        st.caption("TRA1LS is the native token of TRA1LM1NE, a decentralized data marketplace built on the Polygon blockchain.")
        st.caption("TRA1LS : 0xxxxxxxx -> Uniswap")


def bounty_card(id, title, description, address, value, complexity):
    with st.container():
        st.markdown(f"""
            <div class="bounty-card" style="width: 100%;">
            <div class="bounty-complexity">{complexity}</div>
            <div class="bounty-title">{title}</div>
            <div class="bounty-description">{description}</div>
            <div class="bounty-address">{address}</div>
            <div class="bounty-value">{value} TRA1LS</div>
            <div class="bounty-id">Id: {id}</div>
            <div class="bounty-admin">Tra1lMines</div>
            </div>
            """, unsafe_allow_html=True)



col1, col2, col3, col4 = st.columns(4)

doc_stream = db.collection("marketplace").stream()
for i, doc in enumerate(doc_stream):
    data = doc.to_dict()
    with [col1, col2, col3, col4][i % 4]:
        bounty_card(
            data["id"], 
            data["title"], 
            data["description"], 
            data["address"], 
            data["value"], 
            data["complexity"]
        )


st.markdown("<br><br>", unsafe_allow_html=True)


st.markdown("---")


st.markdown("""
<style>

    .stButton button {
        background-color: rgba(128, 128, 128, 0.1);
        width: 100%;
        padding: 10px 24px;
        font-weight: 600;
    }

    .stButton button:hover {
        background-color: rgba(128, 128, 128, 0.1);
        
    }
            


    .bounty-card {
        background-color: var(--background-color);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;

        &:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            border-color: rgba(128, 128, 128, 0.3);
            cursor: pointer;
        }
        .bounty-description {
            font-size: 14px;
            margin-bottom: 12px;
            line-height: 1.5;
            max-height: 150px;
            overflow: hidden;
            text-overflow: auto;
            display: -webkit-box;
            -webkit-line-clamp: 6;
            -webkit-box-orient: vertical;
            color: var(--text-color);
        }
        .bounty-complexity {
            background-color: rgba(128, 128, 128, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            display: inline-block;
            margin-bottom: 8px;
        }
        .bounty-address {
            font-size: 10.5px;
            color: var(--text-color);
            opacity: 0.8;
            margin-bottom: 8px;
            font-family: monospace;
            overflow: auto;
        }
        .bounty-id {
            font-size: 12px;
            color: var(--text-color);
            opacity: 0.7;
            margin-top: 8px;
        }
        .bounty-card:active {
            transform: scale(0.98);
        }
        .bounty-card:focus {
            outline: 2px solid var(--primary-color);
            outline-offset: 2px;
        }
    }
    .bounty-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 8px;
        color: var(--text-color);
    }
    .bounty-value {
        font-size: 24px;
        font-weight: bold;
        color: var(--text-color);
    }
    .bounty-admin {
        color: var(--text-color);
        opacity: 0.7;
        font-size: 14px;
        text-align: right;
        margin-top: -27px;
    }
</style>
""", unsafe_allow_html=True)
