import streamlit as st
from services.search import *



def search_page() -> None:
    '''
        search page
    '''
    back_button = st.button("Back")
    if back_button:
        st.switch_page("main.py")

    if not(st.session_state.logged_in):
        st.switch_page("main.py")
    else:
        found_books_list = search(st.session_state.search_request)
        if not found_books_list:
            st.error("No books were found")
        else:
            for book in found_books_list:
                if not book: continue
                if st.button(book['title']):
                    st.session_state.book_id = book['book_id']
                    st.switch_page("pages/book.py")
                st.write(f"ISBN: {book['isbn']}")
                st.write(f"published year: {book['published_year']}")
                st.write(f"desc: {book['description']}")
                st.markdown("---")

if __name__ == "__main__":
    search_page()