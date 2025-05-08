import streamlit as st
from services.search import *

from services.error_handler import error_handler

def show_book_info(book: dict) -> None:
    if st.button(book['title'], key=book['book_id']):
        st.session_state.book_id = book['book_id']
        st.switch_page("pages/book.py")
    st.markdown(f"author(s): `{', '.join(map(str, book['authors']))}`")
    st.markdown(f"categories: `{', '.join(map(str, book['categories']))}`")
    st.markdown(f"ISBN: `{book['isbn']}`")
    st.markdown(f"published year: `{book['published_year']}`")
    st.write(f"desc: `{book['description']}`")
    st.markdown("---")

@error_handler
def search_page() -> None:
    '''
        search page
    '''

    back_button = st.button("Back")

    if not(st.session_state.get("logged_in", None)) or back_button:
        st.switch_page("main.py")
    else:
        
        st.header("Search results")
        st.markdown("---")
        found_books_list = st.session_state.last_query[1]

        if not found_books_list:
            st.error("No books were found")
        else:
            for book in found_books_list:
                if not book: continue
                show_book_info(book)


if __name__ == "__main__":
    search_page()