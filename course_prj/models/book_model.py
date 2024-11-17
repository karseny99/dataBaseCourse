from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dataclasses import dataclass

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False)
    published_year = Column(Integer, nullable=True)
    isbn = Column(String(256), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    added_at = Column(DateTime, nullable=False)
    file_path = Column(String(512), nullable=False)  
    cover_image_path = Column(String(512), nullable=True) 

    @classmethod 
    def from_orm(cls, book_orm):
        return cls(
            book_id = book_orm.book_id,
            title = book_orm.title,
            published_year = book_orm.published_year,
            isbn = book_orm.isbn,
            description = book_orm.description,
            added_at = book_orm.added_at,
            file_path = book_orm.file_path,
            cover_image_path = book_orm.cover_image_path
        )
