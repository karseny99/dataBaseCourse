from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from models.author_model import Author
from models.book_model import Book


Base = declarative_base()

class BookAuthor(Base):
    __tablename__ = 'book_authors'
    
    author_id = Column(Integer, ForeignKey(Author.author_id), primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.book_id), primary_key=True)

