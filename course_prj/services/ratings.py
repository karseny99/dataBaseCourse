from repositories.ratings_methods import *
import streamlit as st


def add_rating(book_id: int, user_id: int, rating: int) -> int:
    '''
        Appends new rating of book_id from user_id to database or updates old
        Returns rating_id if successfully added
    '''

    return add_or_update_rating(book_id, user_id, rating)


@st.cache_data
def get_book_personal_rating(book_id: int, user_id: int) -> dict:
    '''
        Calls function to find a book's score from user
        Returns date and score as a dict
    '''

    rating_info = get_book_score_from_user(book_id, user_id)

    if not rating_info:
        return None

    return rating_info.__dict__
