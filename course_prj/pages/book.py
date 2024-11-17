import streamlit as st
from services.book import *
from services.downloads import *
from services.ratings import *
from services.comments import *
import time

DelaySubmission = 5

if 'last_submit_time' not in st.session_state:
    st.session_state.last_submit_time = -10


def download_interface(book: dict, book_id: int) -> None:
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


def rating_interface(book_id: int) -> None:
    rate_info = get_book_personal_rating(book_id, st.session_state.user_id)
    default_score = 3

    if rate_info:
        default_score = rate_info['rating']
        st.write(f"Rated last time at {rate_info['rated_at'].strftime('%d.%m.%Y')}")

    rating = st.slider("Rate the book!", min_value=1, max_value=5, value=default_score)

    current_time = time.time()
    if st.button("Submit rating") and (current_time - st.session_state.last_submit_time) > DelaySubmission:
        add_rating(book_id, st.session_state.user_id, rating)
        st.success("Submited")
        st.session_state.last_submit_time = time.time()
    else:
        if current_time - st.session_state.last_submit_time <= DelaySubmission:
            st.error("Not so fast! Go cool yourself")


def last_comments(book_id: int):
    comments = get_last_comments(book_id)

    if not comments:
        st.write("No comments yet")
    
    for comm in comments:
        if not comm: continue

        st.markdown("---")
        st.write(f"{comm['comment']}")



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

            '''
                Main info about the book
            '''
            st.header(book['title'])
            st.image(book['cover_image_path'])
            st.write(f"ISBN {book['isbn']}")
            st.write(f"Published in {book['published_year']}")
            authors = "".join(f"{author}," for author in book['authors'])[:-1]
            st.markdown(f"Author(s) - {authors}")
            categories = "".join(f" {category}," for category in book['categories'])[:-1]
            st.markdown(f"Categories - {categories}")
            st.write(f"desc:")
            st.write(f"{book['description']}")
            st.markdown("---")

            '''
                Download interface
            '''
            download_interface(book, book_id)

            '''
                Rating interface
            '''
            rating_interface(book_id)

            '''
                Comment interface
            '''
            comment = st.text_input("Leave a comment")
            
            if st.button("Send a comment"):

                if len(comment) == 0:
                    st.error("Cannot send an empty comment")
                else:
                    add_comment(book_id, st.session_state.user_id, comment)
                    st.success("Comment sent")

            '''
                Last comments
            '''
            last_comments(book_id)


if __name__ == "__main__":
    book_page()