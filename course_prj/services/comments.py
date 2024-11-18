import repositories.comments_methods 
import repositories.users_methods

import streamlit as st

comments_n = 10

def add_comment(book_id: int, user_id: int, comment: str) -> int:
    '''
        Appends new comment of book_id from user_id to database
        Returns comment_id if successfully added
    '''
    return repositories.comments_methods.add_comment(book_id, user_id, comment)

@st.cache_data
def get_last_comments(book_id: int) -> list:
    '''
        Calls for a function to get a list of comms 
        Returns last comms if existed
        Otherwise returns empty list
    '''

    comments = repositories.comments_methods.get_last_comments(book_id, comments_n)

    if not comments:
        return []

    comments = [comm.__dict__ for comm in comments]
    return comments

@st.cache_data
def get_username_by_commentid(user_id: int) -> str:
    '''
        Calls for a function to get user's name
        Returns username of user if existed
        None otherwise
    '''

    username = repositories.users_methods.get_user_id_info(user_id)
    if username:
        username = username.username
    return username
    