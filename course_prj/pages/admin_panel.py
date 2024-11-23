

import streamlit as st
from services.user import *
from services.error_handler import error_handler

@error_handler
def admin_panel() -> None:

    if not(is_admin()) or st.button("Back"):
        st.switch_page("main.py")


    # db_name = st.session_state.db_name
    # user = st.session_state.user_db
    # password = st.session_state.password_db
    
    # filename = create_database_dump(db_name, user, password)
    # if not filename:
    #     st.error("Wrong entered data")
    # else:
    #     with open(filename, 'rb') as db_dump:
    #         if st.download_button(
    #                 label="Download db_dump",
    #                 data=db_dump,
    #                 file_name=f"{os.path.basename(filename)}",
    #                 mime="application/octet-stream"
    #             ) :
    #             st.success("Downloaded")
    
    restore_database_file = st.file_uploader("Choose db_dump file", type=["dump"], accept_multiple_files=False)
    if restore_database_file is not None:
        st.success(f"File {restore_database_file.name} uploaded")
        submit_button = st.button("Submit database restore")

        if submit_button:
            restore_database_dump(restore_database_file)
            st.success("Database successfully restored")


if __name__ == "__main__":
    admin_panel()