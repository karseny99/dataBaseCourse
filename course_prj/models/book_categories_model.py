from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from models.book_model import Book
from models.category_model import Category

Base = declarative_base()

class BookCategories(Base):
    __tablename__ = 'book_categories'
    
    book_id = Column(Integer, ForeignKey(Book.book_id), primary_key=True)
    category_id = Column(Integer, ForeignKey(Category.category_id), primary_key=True)
