import streamlit as st
import uuid
import os
import psycopg2
import ebookmeta
from PIL import Image
import io

from repositories.books_authors_methods import *
from repositories.book_categories import insert_categories_by_book, get_categories, add_category
import repositories.books_methods
import repositories.authors_methods

def add_category(new_category: str) -> int:
    '''
        Inserts new category
        Returns category_id if successfully
        None otherwise
    '''

    return repositories.book_categories.add_category(new_category)


@st.cache_data
def get_publishing_years():
    '''
        Returns all piblishing years
    '''
    return repositories.books_methods.get_publishing_years()


@st.cache_data
def get_categories():
    '''
        Returns all category names
    '''
    return repositories.book_categories.get_categories()


def get_books(offset: int, limit: int) -> list:
    '''
        Returns by offset limit books 
    '''
    return repositories.books_methods.get_books(offset, limit)


def get_total_books_count(category_filter: str = None, author_filter: str = None, published_year_filter: int = None) -> int:
    '''
        Returns num of books in database
    '''
    return repositories.books_methods.get_books_count(category_filter, author_filter, published_year_filter)


def get_book_info(book_id: int) -> dict:
    '''
        Returns dict with book_info
        None if book_id does not exists
    '''

    return repositories.books_methods.get_book_info_by_id(book_id)   


@st.cache_data
def get_authors():
    '''
        Returns all author's names from database
    '''
    return repositories.authors_methods.get_all_authors()

def add_book(upload_book, categories) -> int:
    '''
        Calls for book addition to database
        Also calls for authors and category insertion
        Returns book_id
        None if unsuccessfully
    '''

    book_item = load_to_storage(upload_book, categories)


    book_id = repositories.books_methods.add_book(book_item)


    insert_authors_by_book(book_item['authors'], book_id)

    insert_categories_by_book(book_item['categories'], book_id)
    
    return book_id


def load_to_storage(upload_book, categories) -> list:
    '''
        Loads .fb2 database
        Returns book's info dict
    '''

    unique_book_file_name = generate_unique_filename(upload_book.name)

    save_path = os.path.join("storage", "books", unique_book_file_name)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as book_file:
        book_file.write(upload_book.getbuffer())

    meta = ebookmeta.get_metadata(save_path)

    byte_array_cover = meta.cover_image_data
    cover_path = None
    if byte_array_cover is not None:
        cover_image = Image.open(io.BytesIO(byte_array_cover))
        unique_cover_file_name = f"{os.path.splitext(unique_book_file_name)[0]}.jpg"
        cover_path = os.path.join("storage", "covers", unique_cover_file_name)
        cover_image.save(cover_path, "JPEG")
        
    book_item = {
        "title": meta.title,
        "published_year": meta.publish_info.year if meta.publish_info.year else None,
        "isbn": meta.publish_info.isbn if meta.publish_info.isbn else None,
        "description": meta.description[:50] + "..." if meta.description is not None else None,
        "file_path": save_path,
        "cover_image_path": cover_path,
        "authors": meta.author_list if meta.author_list is not None else None,
        "categories": categories if categories is not None else None
    }

    return book_item
  


def generate_unique_filename(filename: str) -> str:
    '''
        Generates unique file name
    '''
    return f"{str(uuid.uuid4())}{os.path.splitext(filename)[1]}"


def validate_isbn(isbn: str) -> bool:
    '''
        True if isbn valid
        False otherwise
    '''
    return repositories.books_methods.find_isbn(isbn) == None



def get_paginated_books(page_number, page_size, author_name_filter=None, published_year_filter=None, category_name_filter=None):
    '''
        Returns list of books for pagination
    '''
    return repositories.books_methods.get_paginated_books(page_number, page_size, author_name_filter, published_year_filter, category_name_filter)