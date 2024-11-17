import streamlit as st
from services.book import *
from services.downloads import *

def book_page() -> None:
    '''
        book's page
    '''
    book_id = st.session_state.get("book_id", None)

    if book_id is None or not(st.session_state.logged_in):
        st.switch_page("main.py")

    else:
        back_button = st.button("Back")
        if back_button:
            st.switch_page("main.py")   

        book = get_book_info(book_id)

        if not book:
            st.error("Book did not found")
        else:
            st.header(book['title'])
            st.image(book['cover_image_path'])
            st.write(f"ISBN: {book['isbn']}")
            st.write(f"published year: {book['published_year']}")
            authors = "".join(f"{author}," for author in book['authors'])[:-1]
            st.markdown(f"Authors: {authors}")
            categories = "".join(f" {category}," for category in book['categories'])[:-1]
            st.markdown(f"Categories:{categories}")
            st.write(f"desc: {book['description']}")
            st.markdown("---")

            if book['file_path']:
                with open(book['file_path'], 'rb') as book_file:
                    if st.download_button(
                        label="Download book (fb2)",
                        data=book_file,
                        file_name=f"{book['title']}.fb2",
                        mime="application/x-fictionbook"
                    ): 
                        st.success("Downloaded")
                        add_download(st.session_state.user_id, book_id)
            else:
                st.write("Book file ran away")


if __name__ == "__main__":
    book_page()