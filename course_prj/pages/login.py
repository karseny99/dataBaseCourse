import streamlit as st
from services.auth import *

def login_user() -> None:
    '''
        login page
    '''

    back_button = st.button("Back")
    if back_button:
        st.switch_page("main.py")

    if not(st.session_state.logged_in):
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
        if login_button:
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
    else:
        st.switch_page("main.py")

if __name__ == "__main__":
    login_user()