from datetime import datetime
from models.user_model import User
from models.book_model import Book

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Download:
    def __init__(self, download_id: int, user_id: int, book_id: int, download_date: str):
        self.download_id = download_id
        self.user_id = user_id
        self.book_id = book_id
        self.download_date = download_date

    @classmethod
    def from_dict(cls, download_dict):
        return cls(
            download_id=int(download_dict['download_id']),
            user_id=int(download_dict['user_id']),
            book_id=int(download_dict['book_id']),
            download_date=download_dict['download_date']
        )

