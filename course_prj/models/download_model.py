from datetime import datetime
from models.user_model import User
from models.book_model import Book

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Download(Base):
    __tablename__ = 'downloads'
    
    download_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.book_id), primary_key=True)
    download_date = Column(DateTime, default=datetime.now())

    @classmethod 
    def from_orm(cls, download_orm):
        return cls(
            download_id=download_orm.download_id,
            book_id=download_orm.book_id,
            user_id=download_orm.user_id,
            download_date=download_orm.download_date
        )
