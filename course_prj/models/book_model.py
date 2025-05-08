from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dataclasses import dataclass


class Book():
    __tablename__ = 'books'

    def __init__(self, book_id: int, title: str, published_year: int, isbn: str, 
                 description: str, added_at: str, file_path: str, cover_image_path: str):
        self.book_id = book_id
        self.title = title
        self.published_year = published_year
        self.isbn = isbn
        self.description = description
        self.added_at = added_at
        self.file_path = file_path
        self.cover_image_path = cover_image_path

    @classmethod
    def from_dict(cls, book_dict):
        return cls(
            book_id=int(book_dict['book_id']),
            title=book_dict['title'],
            published_year=book_dict['published_year'],
            isbn=book_dict['isbn'],
            description=book_dict['description'],
            added_at=book_dict['added_at'],
            file_path=book_dict['file_path'],
            cover_image_path=book_dict.get('cover_image_path')  # Используем get для обработки возможного отсутствия
        )
