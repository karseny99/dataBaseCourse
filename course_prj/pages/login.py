import streamlit as st
from services.auth import *
from services.error_handler import error_handler

@error_handler
def login_user() -> None:
    '''
        login page
    '''

    back_button = st.button("Back")
    if back_button:
        st.switch_page("main.py")

    if not(st.session_state.get("logged_in", None)):
        login = st.text_input("Enter a username or email").strip()
        password = st.text_input("Enter a password", type="password").strip()

        st.markdown(
            """
        <style>
            [title="Show password text"] {
                display: none;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

        login_button = st.button("Log in")
        if login_button and len(login) and len(password):
            try:
                st.session_state.user_id = Authentication.login_user(login, password)
                st.session_state.logged_in = True
                st.empty()
                st.success("Logged in successfully")
                go_searching = st.button("Go to searching page")
                if go_searching:
                    st.switch_page("main.py")
            except WrongEnterException as e:
                st.error(e.message)
            except Exception as e:
                print(f"Cannot log in user because of {e}")
                raise e
        elif login_button:
            if len(login) == 0:
                st.warning("No login?")
            if len(password) == 0:
                st.warning("No password?")

    else:
        st.switch_page("main.py")

if __name__ == "__main__":
    login_user()