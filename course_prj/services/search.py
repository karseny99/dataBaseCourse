
from repositories.books_methods import *
from repositories.books_authors_methods import get_authors_from_book
from typing import Any, List
import streamlit as st

def search(searh_request: str) -> list:
    '''
        Search in fields Title, ISBN, Author, Year
        Calls function for searching in database for books
        Returns a list of matched books
    '''

    return search_book(searh_request)


def update_suggestions(searchterm: str) -> List[tuple[str, Any]]:
    last = st.session_state.last_query[0]
    suggestions = st.session_state.last_query[1]
    
    if abs(len(searchterm) - len(last)) < 2:
            return [
                    (
                    book['title'],
                    [book['title'], book['book_id']],
                    )
                    for book in suggestions
                ]
    
    if last != "" and suggestions and searchterm.startswith(last) :
        suggestions = [book for book in suggestions if searchterm in book['title']]
    else:
        suggestions = search(searchterm)
        
    st.session_state.last_query[0] = searchterm
    st.session_state.last_query[1] = suggestions
    return [
        (
        book['title'],
        [str(book['title']), book['book_id']],
        )
        for book in suggestions
    ]