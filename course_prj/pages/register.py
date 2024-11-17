import streamlit as st
from services.register import *

def regsiter_user() -> None:
    '''
        Registration page
    '''

    back_button = st.button("Back")
    if back_button:
        st.switch_page("main.py")

    if not(st.session_state.logged_in):

        username = st.text_input("Enter a username").strip()
        email = st.text_input("Enter a email").strip()
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

        register_button = st.button("Register")
        if register_button:
            if not(Validation.validate_username(username)):
                st.write("Username must consist of letters and digits or only letters")
            elif not(Validation.validate_email(email)):
                st.write("Incorrect email")
            elif not(Validation.validate_password(password)):
                st.write("Password must have at least one capital letter, at least one special symbol and its size has to be at least 8 symbols")
            else:
                try:
                    st.session_state.user_id = Registration.register_user(username, email, password)
                    st.session_state.logged_in = True
                    st.empty()
                    st.success("Registered successfully")
                    go_searching = st.button("Go to searching page")
                    if go_searching:
                        st.switch_page("main.py")
                except (UsernameExistsException, EmailExistsException) as e:
                    st.error(e.message)
                except Exception as e:
                    print(f"Cannot register user because of {e}")
                    raise e

    else:
        st.switch_page("main.py")

if __name__ == "__main__":
    regsiter_user()