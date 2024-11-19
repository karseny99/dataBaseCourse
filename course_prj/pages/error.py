import streamlit as st


def display_error_page(message: str) -> None:
    st.empty()
    st.title("Error occured")
    st.error(message)

