
from repositories.connector import *
from models.book_model import Book
from repositories.authors_methods import *
from models.book_authors_model import BookAuthor
from services.logger import logging

def get_books_from_author(author_name: str) -> list:
    '''
        Returns all books written by author_name
    '''
    
    with get_session() as session:
        query = text("SELECT author_id FROM authors WHERE name ILIKE :author_name")

        authors = session.execute(query, {"author_name": f"%{author_name}%"})
        author_ids = [author[0] for author in authors]

        if not author_ids:
            return [] 

        query = text("""
            SELECT b.* 
            FROM books b
            JOIN book_authors ba ON b.book_id = ba.book_id
            WHERE ba.author_id IN :author_ids
        """)

        books = session.execute(query, {"author_ids": tuple(author_ids)}).mappings()
        books = [Book.from_dict(dict(book)) for book in books]

        return books


def get_authors_from_book(book_id: int) -> list:
    '''
        Returns list of authors for given book_id
        None if wrong book_id
    '''

    with get_session() as session:

        query = text("""
            SELECT a.* 
            FROM authors a
            JOIN book_authors ba ON a.author_id = ba.author_id
            WHERE ba.book_id = :book_id
        """)

        authors = session.execute(query, {"book_id": book_id}).mappings()

        authors = [Author.from_dict(dict(author)) for author in authors]
        return authors


def insert_authors_by_book(authors: list, book_id: int) -> None:
    '''
        Inserts a list of authors related to book_id
    '''

    with get_session() as session:

        for author in authors:

            query = text("""
                SELECT author_id 
                FROM authors    
                WHERE name ILIKE :author_name
            """)


            author_obj = session.execute(query, {"author_name": author}).fetchone()

            if not author_obj:
                insert_query = text("""
                    INSERT INTO authors (name, bio) 
                    VALUES (:name, :bio) 
                    RETURNING author_id
                """)

                author_obj = session.execute(insert_query, {"name": author, "bio": None}).fetchone()
        
            insert_relation_query = text("""
                INSERT INTO book_authors (book_id, author_id) 
                VALUES (:book_id, :author_id)
            """)
            session.execute(insert_relation_query, {"book_id": book_id, "author_id": author_obj[0]})

        logging.info(f"{authors} was inserted to book-author table")
    