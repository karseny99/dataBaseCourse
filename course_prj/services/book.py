
from repositories.books_authors_methods import *

import repositories.books_methods

import streamlit as st


def get_book_info(book_id: int) -> dict:
    '''
        Returns dict with book_info
        None if book_id does not exists
    '''

    book_item = repositories.books_methods.get_book_by_id(book_id)
    if not book_item:
        return None

    book_info = book_item.__dict__

    book_authors = get_authors_from_book(book_id)
    book_categories = repositories.books_methods.get_book_categories(book_id)

    if book_authors:
        book_authors = [author.name for author in book_authors]
        book_info['authors'] = book_authors

    if book_categories:
        book_categories = [book.category_name for book in book_categories]
        book_info['categories'] = book_categories

    
        
    return book_info
