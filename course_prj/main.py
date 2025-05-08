import pandas as pd
import psycopg2
import psycopg2.extras
import streamlit as st
from streamlit_searchbox import st_searchbox

from typing import Any, List

from services.error_handler import error_handler
from services.search import *
from pages.sidebar import show_sidebar

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'search_request' not in st.session_state:
    st.session_state.search_request = ""

if 'last_query' not in st.session_state:
    st.session_state.last_query = ["", []]

def redirect_to_book_page(submit_value: list):
    st.session_state.book_id = submit_value[1]
    st.switch_page("pages/book.py")

@error_handler
def main() -> None:

    if not(st.session_state.logged_in):
        st.title("You need to log in")
        st.session_state.logged_in = False

        reg_button = st.button("Register")
        login_button = st.button("log in")

        if reg_button:
            st.switch_page("pages/register.py")
        if login_button:
            st.switch_page("pages/login.py")

    else:
        show_sidebar()
        
        st.title("Open Library")

        search_request = st_searchbox(
            update_suggestions,
            placeholder="Search Book... ",
            key="my_key",
            clear_on_submit=True,
            submit_function=redirect_to_book_page,
        )

        # search_button = st.button("🔎")

        # if search_button and search_request is not None:
        #     st.session_state.search_request = search_request
        #     st.switch_page("pages/search.py")


        all_books_button = st.button("See all books")
        if all_books_button:
            st.switch_page("pages/books.py")


if __name__ == "__main__":
    main()
    