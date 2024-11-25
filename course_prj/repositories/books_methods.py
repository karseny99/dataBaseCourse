from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

from repositories.connector import *
from models.book_model import Book
from repositories.authors_methods import *
from repositories.books_authors_methods import *
import repositories.book_categories 
import repositories.ratings_methods
from services.logger import logging

def search_in_column(search_value: str, column_name: str) -> list:
    '''
        Searching for given title in title column 
        Returns list of matched books
    '''

    if column_name == 'author':
        return search_by_author(search_value)

    query = text(f"""
        SELECT b.* 
        FROM books b
        WHERE b.{column_name} ILIKE :search_value
    """)

    with get_session() as session:
        matched_books = session.execute(query, {"search_value": f"%{search_value}%"}).mappings()
        matched_books = [Book.from_dict(book) for book in matched_books]
        return matched_books


def search_by_author(author_name: str) -> list:
    '''
        Calls functions for another table to find all books from given author_name
        Returns list of book items
    '''
    return get_books_from_author(author_name)


def get_book_by_id(book_id: int) -> Book:
    '''
        Returns Book for given book_id
        None if not found
    '''
    with get_session() as session:

        query = text("""
            SELECT * FROM books 
            WHERE book_id = :book_id
        """)
        
        result = session.execute(query, {"book_id": book_id}).mappings().fetchone()
        
        if result is None:
            return None 
        
        book = Book.from_dict(dict(result))
        return book

        
def get_book_categories(book_id: int) -> list:
    '''
        Calls function for another table to find all categories of the book
        Returns list of categories
    '''
    return repositories.book_categories.get_book_categories(book_id)


def get_book_ids() -> list:
    '''
        Returns list of existed book_id
    '''
    with get_session() as session:
        query = text("SELECT book_id FROM books")
        book_ids = session.execute(query)
        return [book_id[0] for book_id in book_ids]
    

def add_book(book_item: dict) -> int:
    '''
        Inserts new book to database
        Returns new book_id
    '''

    with get_session() as session:
        insert_query = text("""
            INSERT INTO books (title, published_year, isbn, description, added_at, file_path, cover_image_path) 
            VALUES (:title, :published_year, :isbn, :description, :added_at, :file_path, :cover_image_path) 
            RETURNING book_id
        """)
        new_book = session.execute(insert_query, {
            "title": book_item['title'],
            "published_year": book_item.get('published_year'),
            "isbn": book_item['isbn'],
            "description": book_item.get('description'),
            "added_at": datetime.now(),
            "file_path": book_item.get('file_path'),
            "cover_image_path": book_item.get('cover_image_path')
        })

        new_book_id = new_book.fetchone()[0]
        logging.info(f"Inserted new book_id={new_book_id} into a book-table")
        return new_book_id


def find_isbn(isbn: str) -> int:
    '''
        Returns for matched isbn book_id
        Or None if unmatched
    '''
    with get_session() as session:
        query = text("""
            SELECT book_id
            FROM books
            WHERE isbn = :isbn
        """) 

        book_id = session.execute(query, {"isbn": isbn}).mappings().fetchone()
        
        if book_id is None:
            return None 
        
        return book_id
