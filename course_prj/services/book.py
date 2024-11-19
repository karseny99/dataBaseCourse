import streamlit as st
import uuid
import os

from repositories.books_authors_methods import *
from repositories.book_categories import insert_categories_by_book
import repositories.books_methods


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


def add_book(book_item: dict) -> int:
    '''
        Calls for book addition to database
        Also calls for authors and category insertion
        Returns book_id
    '''

    book_id = repositories.books_methods.add_book(book_item)

    insert_authors_by_book(book_item['authors'], book_id)

    insert_categories_by_book(book_item['categories'], book_id)
    
    return book_id



def generate_unique_filename(filename: str) -> str:
    '''
        Generates unique file name
    '''
    return f"{str(uuid.uuid4())}{os.path.splitext(filename)[1]}"