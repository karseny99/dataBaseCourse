import streamlit as st
import time
import os

from services.book import *
from services.downloads import *
from services.ratings import *
from services.comments import *
from services.user import get_info_actions_user, is_admin
from services.error_handler import error_handler

DelaySubmission = 5

if 'last_rating_submit_time' not in st.session_state:
    st.session_state.last_rating_submit_time = -10

if 'last_comment_submit_time' not in st.session_state:
    st.session_state.last_comment_submit_time = -10

if 'unrated_book' not in st.session_state:
    st.session_state.unrated_book = False


def show_main_info(book: dict) -> None:
    st.header(book['title'])

    book_rating = get_book_rating_info(book['book_id'])
    if book_rating['average_rating']:
        st.write(f"{book_rating['average_rating']:.1f}/5 \
                  based on {book_rating['ratings_count']} score(s)")
    else:
        st.session_state.unrated_book = True
        st.warning("No one rated book, be the first!")

    try:
        st.image(book['cover_image_path'])
    except:
        pass

    st.write(f"ISBN {book['isbn']}")

    st.write(f"Published in {book.get('published_year', 'Unknown')}")

    authors = "".join(f"{author}," for author in book.get('authors', ''))[:-1]

    st.markdown(f"Author(s) - {authors}")

    categories = "".join(f" {category}," for category in book.get('categories', ''))[:-1]

    st.markdown(f"Categories - {categories}")

    st.write(f"description - {book.get('description', '')}")

    st.markdown("---")


def download_interface(book: dict) -> None:
    if book['file_path']:
        try:
            with open(book['file_path'], 'rb') as book_file:
                if st.download_button(
                            label="Download book (fb2)",
                            data=book_file,
                            file_name=f"{book['title']}.fb2",
                            mime="application/x-fictionbook"
                        ) :
                    st.success("Downloaded")
                    try:
                        user_id = st.session_state.user_id
                    except:
                        st.switch_page("main.py")
                    add_download(user_id, book['book_id'])
                    get_info_actions_user.clear()
        except FileNotFoundError as e:
            st.error("Book file was lost")
    else:
        st.error("Book file was lost")


def rating_interface(book_id: int) -> None:
    rate_info = get_book_personal_rating(book_id, st.session_state.user_id)
    default_score = 3

    if rate_info:
        default_score = rate_info['rating']
        st.write(f"Rated last time at {rate_info['rated_at'].strftime('%d.%m.%Y')}")

    rating = st.slider("Rate the book!", min_value=1, max_value=5, value=default_score)

    current_time = time.time()
    if st.button("Submit rating") and (current_time - st.session_state.last_rating_submit_time) > DelaySubmission:
        add_rating(book_id, st.session_state.user_id, rating)
        # After rating added need to update old cache
        get_book_personal_rating.clear()
        get_info_actions_user.clear()
        if st.session_state.unrated_book: get_book_rating_info.clear()

        st.success("Submited")
        st.session_state.last_rating_submit_time = time.time()
    else:
        if current_time - st.session_state.last_rating_submit_time <= DelaySubmission:
            st.error("Not so fast! Go cool yourself")


def adding_comment_interface(book_id: int) -> None:
    comment = st.text_input("Leave a comment")

    current_time = time.time()

    if st.button("Send a comment") and (current_time - st.session_state.last_comment_submit_time) > DelaySubmission: 
        if len(comment) == 0:
            st.error("Cannot send an empty comment")
        else:
            add_comment(book_id, st.session_state.user_id, comment)
            # After adding a comm deleting old cache
            get_last_comments.clear()
            get_info_actions_user.clear()
            st.success("Comment sent")
        st.session_state.last_comment_submit_time = time.time()
    else:
        if current_time - st.session_state.last_comment_submit_time <= DelaySubmission:
            st.error("Not so fast! Go cool yourself")


def last_comments(book_id: int) -> None:
    comments = get_last_comments(book_id)

    if not comments:
        st.write("No comments yet")
        return
    else:
        st.markdown("---")
        st.subheader("Comments")

    isAdmin = is_admin()
    
    for comm in comments:
        if not comm: continue
        st.markdown("---")

        if isAdmin:
            if st.button(f"🗑️", key=comm['comment_id']):
                delete_comment(comm['comment_id'])
                get_last_comments.clear()
        st.write(f"{comm['comment']}")
        comment_date = comm['commented_at'].strftime('%d.%m.%Y') 
        st.markdown(f"<small>Commented by {comm['username']} at {comment_date}</small>", unsafe_allow_html=True)
   

  
@error_handler
def book_page() -> None:
    '''
        book's page
    '''
    book_id = st.session_state.get("book_id", None)
    if not book_id or not(st.session_state.get("logged_in", None)):
        st.switch_page("main.py")

    else:
        back_button = st.button("Back") 
        if back_button:
            st.switch_page("main.py")   

        book = get_book_info(book_id)

        if not book:
            st.error("Book did not found")
        else:

            # '''
            #     Main info about the book
            # '''
            show_main_info(book)

            # '''
            #     Download interface
            # '''
            download_interface(book)

            # '''
            #     Rating interface
            # '''
            rating_interface(book_id)

            # '''
            #     Comment interface
            # '''
            adding_comment_interface(book_id)

            # '''
            #     Last comments
            # '''
            last_comments(book_id)


if __name__ == "__main__":
    book_page()