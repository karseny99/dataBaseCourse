import streamlit as st


def call_display_page(message: str) -> None:
    if 'error_message' not in st.session_state:
        st.session_state.error_message = message
    st.switch_page("pages/error.py")


def display_error_page() -> None:
    st.empty()
    if st.button("Back"):
        st.switch_page("main.py")
    st.title("Something went wrong")
    message = 'Dunno what'
    if 'error_message' in st.session_state:
        message = st.session_state.error_message
    st.error(message)

if __name__ == "__main__":
    display_error_page()