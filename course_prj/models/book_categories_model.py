from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from models.book_model import Book
from models.category_model import Category

Base = declarative_base()

class BookCategories:
    def __init__(self, book_id: int, category_id: int):
        self.book_id = book_id
        self.category_id = category_id

    @classmethod
    def from_dict(cls, category_dict):
        return cls(
            book_id=int(category_dict['book_id']),
            category_id=int(category_dict['category_id'])
        )
