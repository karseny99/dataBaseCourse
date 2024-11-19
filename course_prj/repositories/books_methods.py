from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

from repositories.connector import *
from models.book_model import Book
from repositories.authors_methods import *
from repositories.books_authors_methods import *
import repositories.book_categories 
import repositories.ratings_methods

def search_in_column(search_value: str, column_name: str) -> list:
    '''
        Searching for given title in title column 
        Returns list of matched books
    '''

    if column_name == 'author':
        return search_by_author(search_value)

    column = getattr(Book, column_name)

    with get_session() as session:
        matched_books = session.query(Book).filter(column.ilike(f"%{search_value}%")).all()
        matched_books = [Book.from_orm(obj) for obj in matched_books]
        print(matched_books, column_name)
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
        try:
            book = Book.from_orm(session.query(Book).filter_by(book_id=book_id).one())
            return book
        except NoResultFound:
            return None
        

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
        book_ids = session.query(Book.book_id).all()
        return [book_id[0] for book_id in book_ids]
    

def add_book(book_item: dict) -> int:
    '''
        Inserts new book to database
        Returns new book_id
    '''

    with get_session() as session:
        new_book = Book(
            title=book_item['title'],
            published_year=book_item.get('published_year'),
            isbn=book_item['isbn'],
            description=book_item.get('description'),
            added_at=datetime.now(),
            file_path=book_item.get('file_path'),
            cover_image_path=book_item.get('cover_image_path')
        )

        session.add(new_book)
        session.commit()
        print(f"Inserted new book_id={new_book.book_id} into a book-table")
        return new_book.book_id
