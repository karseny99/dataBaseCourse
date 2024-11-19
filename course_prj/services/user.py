
from repositories.users_methods import get_user_id_info
from repositories.comments_methods import get_user_actions

import streamlit as st

def is_admin() -> bool:
    user_id = st.session_state.user_id
    user = get_user_info(user_id)

    if not user or user['role'] != 'admin':
        return False
    
    return True

def get_user_info(user_id: int) -> dict:
    '''
        Returns user-object as a dict, according to user_model
        Removes 'password_hash'
        Returns None if user_id not exists
    '''
    user_info = get_user_id_info(user_id)
    if not user_info:
        return None
    else:
        user_info = user_info.__dict__
        _ = user_info.pop('password_hash')
    
    return user_info


@st.cache_data
def get_info_actions_user(user_id: int) -> dict:
    '''
        Requests function to get user's info if exists
        Contains basics from users table and additional info such as
        all sent comments_info, ratings_info, downloads_info 
        None otherwise
    '''

    user_info = get_user_info(user_id)
    user_actions = get_user_actions(user_id)

    if user_actions:
        user_info['actions'] = user_actions 

    return user_info


