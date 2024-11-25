import streamlit as st
import uuid
import os
import psycopg2

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
        None if unsuccessfully
    '''

    book_id = repositories.books_methods.add_book(book_item)


    insert_authors_by_book(book_item['authors'], book_id)

    insert_categories_by_book(book_item['categories'], book_id)
    
    return book_id


def load_to_storage(upload_book, upload_cover) -> list:
    '''
        Loads .fb2 and .jpg to database, or only .fb2 if .jpg wasn't given
        Returns path list
    '''

    uploaded_pair = []

    unique_book_file_name = generate_unique_filename(upload_book.name)

    save_path = os.path.join("storage", "books", unique_book_file_name)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as book_file:
        book_file.write(upload_book.getbuffer())

    uploaded_pair.append(save_path)

    if upload_cover is not None:
        unique_cover_file_name = f"{os.path.splitext(unique_book_file_name)[0]}.jpg"
        cover_save_path = os.path.join("storage", "covers", unique_cover_file_name)

        os.makedirs(os.path.dirname(cover_save_path), exist_ok=True)

        with open(cover_save_path, "wb") as cover_file:
            cover_file.write(upload_cover.getbuffer())

        uploaded_pair.append(cover_save_path)

    return uploaded_pair
  


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