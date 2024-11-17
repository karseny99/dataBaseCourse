
from repositories.connector import *
from models.book_model import Book
from repositories.authors_methods import *
from models.book_authors_model import BookAuthor

def get_books_from_author(author_name: str) -> list:
    '''
        Returns all books written by author_name
    '''
    
    with get_session() as session:
        authors = session.query(Author).filter(Author.name.ilike(f"%{author_name}%")).all()
        authors = [Author.from_orm(author) for author in authors]

        if not authors:
            return [] 

        books = []

        for author in authors:
            books += session.query(Book).join(BookAuthor, Book.book_id == BookAuthor.book_id).filter(BookAuthor.author_id == author.author_id).all()
        
        books = [Book.from_orm(book) for book in books]
        return books


def get_authors_from_book(book_id: int) -> list:
    '''
        Returns list of authors for given book_id
        None if wrong book_id
    '''

    with get_session() as session:
        authors = session.query(Author).join(BookAuthor, Author.author_id == BookAuthor.author_id).filter(BookAuthor.book_id == book_id).all()
        authors = [Author.from_orm(author) for author in authors]
        return authors


    