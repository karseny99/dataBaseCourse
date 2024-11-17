from datetime import datetime
from models.user_model import User
from models.book_model import Book

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rating(Base):
    __tablename__ = 'ratings'
    
    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.book_id), primary_key=True)
    rating = Column(Integer, nullable=False)
    rated_at = Column(DateTime)

    @classmethod 
    def from_orm(cls, rating_orm):
        return cls(
            rating_id=rating_orm.rating_id,
            user_id=rating_orm.user_id,
            book_id=rating_orm.book_id,
            rating=rating_orm.rating,
            rated_at=rating_orm.rated_at
        )