from datetime import datetime
from models.user_model import User
from models.book_model import Book

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comments'
    
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.book_id), primary_key=True)
    comment = Column(Text, nullable=False)
    commented_at = Column(DateTime, default=datetime.now)

    @classmethod 
    def from_orm(cls, comment_orm):
        return cls(
            comment_id=comment_orm.comment_id,
            user_id=comment_orm.user_id,
            book_id=comment_orm.book_id,
            comment=comment_orm.comment,
            commented_at=comment_orm.commented_at
        )