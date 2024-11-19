import streamlit as st
import time
from services.error_handler import error_handler

@error_handler
def show_sidebar() -> None:

    with st.sidebar:
        profile_button = st.button("Go to profile")
        if profile_button:
            st.switch_page("pages/profile.py")