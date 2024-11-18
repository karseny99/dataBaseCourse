import repositories.ratings_methods 
import repositories.books_methods
import streamlit as st

@st.cache_data
def get_book_rating_info(book_id: int) -> dict:
    '''
        Dict fields are 'average_rating' and 'ratings_count'

        Returns a dict with nums of scores and average rating of book_id
        None if there is no ratings for book_id
    '''
    book_rating_info = repositories.ratings_methods.get_book_rating_info(book_id)
    return book_rating_info

def add_rating(book_id: int, user_id: int, rating: int) -> int:
    '''
        Appends new rating of book_id from user_id to database or updates old
        Returns rating_id if successfully added
    '''

    return repositories.ratings_methods.add_or_update_rating(book_id, user_id, rating)


@st.cache_data
def get_book_personal_rating(book_id: int, user_id: int) -> dict:
    '''
        Calls function to find a book's score from user
        Returns date and score as a dict
    '''

    rating_info = repositories.ratings_methods.get_book_score_from_user(book_id, user_id)

    if not rating_info:
        return None

    return rating_info.__dict__
