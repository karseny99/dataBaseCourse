from datetime import datetime
from models.user_model import User
from models.book_model import Book

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rating:
    def __init__(self, rating_id: int, user_id: int, book_id: int, rating: int, rated_at: str):
        self.rating_id = rating_id
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
        self.rated_at = rated_at

    @classmethod
    def from_dict(cls, rating_dict):
        return cls(
            rating_id=int(rating_dict['rating_id']),
            user_id=int(rating_dict['user_id']),
            book_id=int(rating_dict['book_id']),
            rating=rating_dict['rating'],
            rated_at=rating_dict['rated_at']
        )
