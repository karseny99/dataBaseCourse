from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from models.author_model import Author
from models.book_model import Book


Base = declarative_base()

class BookAuthor:
    def __init__(self, author_id: int, book_id: int):
        self.author_id = author_id
        self.book_id = book_id

    @classmethod
    def from_dict(cls, book_author_dict):
        return cls(
            author_id=int(book_author_dict['author_id']),
            book_id=int(book_author_dict['book_id'])
        )