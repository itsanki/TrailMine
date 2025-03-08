import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Redirecting to Bitcoin Analysis...", page_icon="🔗")

external_url = "http://localhost:5005"

st.markdown(
    f"""
    <meta http-equiv="refresh" content="0; url={external_url}" />
    Loading Bitcoin Analysis Dashboard, click <a href="{external_url}">here</a>.
    """,
    unsafe_allow_html=True
)

# components.iframe("http://localhost:80", width=1920, height=1080) 
