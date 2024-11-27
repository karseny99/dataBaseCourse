

import streamlit as st
from services.user import *
from services.error_handler import error_handler
from services.user import get_last_dump_file_date
import os

@error_handler
def admin_panel() -> None:

    go_back = st.button("Back")

    st.title("Restoring page")

    if not(is_admin()) or go_back:
        st.switch_page("main.py")
    restore_database_file = st.button("Restore database")
    st.info(f"Dump's date is {os.path.basename(get_last_dump_file_date())}")
    if restore_database_file:
        filename = restore_database_dump()
        st.success(f"Database successfully restored from {filename}")


if __name__ == "__main__":
    admin_panel()