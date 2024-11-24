from datetime import datetime
from models.user_model import User
from models.book_model import Book

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base


class Comment:
    def __init__(self, comment_id: int, user_id: int, book_id: int, comment: str, commented_at: str):
        self.comment_id = comment_id
        self.user_id = user_id
        self.book_id = book_id
        self.comment = comment
        self.commented_at = commented_at

    @classmethod
    def from_dict(cls, comment_dict):
        return cls(
            comment_id=int(comment_dict['comment_id']),
            user_id=int(comment_dict['user_id']),
            book_id=int(comment_dict['book_id']),
            comment=comment_dict['comment'],
            commented_at=comment_dict['commented_at']
        )
