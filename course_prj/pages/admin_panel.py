

import streamlit as st
from services.user import *
from services.error_handler import error_handler

@error_handler
def admin_panel() -> None:

    go_back = st.button("Back")

    if not(is_admin()) or go_back:
        st.switch_page("main.py")
    restore_database_file = st.button("Restore database")
    # restore_database_file = st.file_uploader("Choose db_dump file", type=["dump"], accept_multiple_files=False)
    if restore_database_file:
        # st.success(f"File {restore_database_file.name} uploaded")
        # submit_button = st.button("Submit database restore")

        # if submit_button:
        filename = restore_database_dump()
        st.success(f"Database successfully restored from {filename}")


if __name__ == "__main__":
    admin_panel()