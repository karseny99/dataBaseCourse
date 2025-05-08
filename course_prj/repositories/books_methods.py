from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

from repositories.connector import *
from models.book_model import Book
from repositories.authors_methods import *
from repositories.books_authors_methods import *
import repositories.book_categories 
import repositories.ratings_methods
from services.logger import logging


def get_publishing_years() -> list:
    '''
        Returns list of all publishing years
    '''

    with get_session(Reader) as session:
        query = text("""
            SELECT published_year
            FROM books
        """)

        years = session.execute(query).scalars().all()
        return years

def get_books(offset: int, limit: int) -> list:
    '''
        Returns by offset limit books with authors and categories
    '''

    query = text("""
        SELECT                 
                book_id, 
                title, 
                published_year, 
                isbn, 
                description,
                array_agg(DISTINCT author_name) AS authors,
                array_agg(DISTINCT category_name) AS categories
        FROM books_full_info
        GROUP BY book_id, title, published_year, isbn, description
        ORDER BY book_id
        LIMIT :limit OFFSET :offset
    """)

    with get_session(Reader) as session:
        books = session.execute(query, {"limit": limit, "offset": offset}).mappings().all()
        return books

def get_books_count(category_filter: str = None, author_filter: str = None, published_year_filter: int = None) -> int:
    '''
        Returns amount of books in database by filter
    '''
    query = text("""
        SELECT COUNT(DISTINCT book_id) AS book_amount
        FROM books_full_info b
        WHERE 1=1
    """)
    
    if category_filter:
        query = text(query.text + " AND b.category_name = :category")
    if author_filter:
        query = text(query.text + " AND b.author_name = :author")
    if published_year_filter:
        query = text(query.text + " AND b.published_year = :published_year")

    with get_session(Reader) as session:
        amount = session.execute(query, {"category": category_filter, "author": author_filter, "published_year": published_year_filter}).scalar()
        return amount

def search_book(search_value: str) -> list:
    '''
        Searching for books by given search value 
        In authors, titles, ISBNs
        Returns list of matched books
    '''

    query = text(f"""
        SELECT                 
                book_id, 
                title, 
                published_year, 
                isbn, 
                description,
                file_path,
                cover_image_path,
                array_agg(DISTINCT author_name) AS authors,
                array_agg(DISTINCT category_name) AS categories
        FROM books_full_info
        WHERE title ILIKE :search_value or author_name ILIKE :search_value or isbn ILIKE :search_value
        GROUP BY book_id, title, published_year, isbn, description, file_path, cover_image_path      
    """)

    with get_session(Reader) as session:
        matched_books = session.execute(query, {"search_value": f"%{search_value}%"}).mappings().all()
        return matched_books


def search_by_author(author_name: str) -> list:
    '''
        Calls functions for another table to find all books from given author_name
        Returns list of book items
    '''
    return get_books_from_author(author_name)


def get_book_info_by_id(book_id: int) -> dict:
    '''
        Returns book info with authors and categories as a list
        None if unexisted
    '''

    query = text("""
    SELECT                 
            book_id, 
            title, 
            published_year, 
            isbn, 
            description,
            file_path,
            cover_image_path,
            array_agg(DISTINCT author_name) AS authors,
            array_agg(DISTINCT category_name) AS categories
    FROM books_full_info
    WHERE book_id = :book_id
    GROUP BY book_id, title, published_year, isbn, description, file_path, cover_image_path
    """)

    with get_session(Reader) as session:
        book = session.execute(query, {"book_id": book_id}).mappings().fetchone()
        return book

def get_book_by_id(book_id: int) -> Book:
    '''
        Returns Book for given book_id
        None if not found
    '''
    with get_session(Reader) as session:

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
    with get_session(Reader) as session:
        query = text("SELECT book_id FROM books")
        book_ids = session.execute(query)
        return [book_id[0] for book_id in book_ids]
    

def add_book(book_item: dict) -> int:
    '''
        Inserts new book to database
        Returns new book_id
    '''

    with get_session(Admin) as session:
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
    with get_session(Reader) as session:
        query = text("""
            SELECT book_id
            FROM books
            WHERE isbn = :isbn
        """) 

        book_id = session.execute(query, {"isbn": isbn}).mappings().fetchone()
        
        if book_id is None:
            return None 
        
        return book_id


from sqlalchemy import text

def get_paginated_books(page_number, page_size, author_name_filter=None, 
                        published_year_filter=None, 
                        category_name_filter=None) -> list:
    
    '''
        Returns books for pagination by filters
    '''

    query = text("""
        SELECT *
        FROM get_paginated_books(
            :page_number, 
            :page_size, 
            :author_name_filter, 
            :published_year_filter, 
            :category_name_filter
        ) AS result;
    """)

    with get_session(Reader) as session:
        books = session.execute(query, {
            'page_number': page_number,
            'page_size': page_size,
            'author_name_filter': author_name_filter,
            'published_year_filter': published_year_filter,
            'category_name_filter': category_name_filter
        }).mappings().fetchall()

        return books
