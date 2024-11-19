
import repositories.requests_methods 

import streamlit as st

@st.cache_data
def add_request(user_id: int) -> int:
    '''
        Returns new request_id 
        None if last request was added less than 7 days ago 
    '''
    return repositories.requests_methods.add_request(user_id)
