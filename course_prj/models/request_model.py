from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

from models.user_model import User

from datetime import datetime

class Request:
    def __init__(self, request_id: int, user_id: int, request_date: str):
        self.request_id = request_id
        self.user_id = user_id
        self.request_date = request_date

    @classmethod
    def from_dict(cls, request_dict):
        return cls(
            request_id=int(request_dict['request_id']),
            user_id=int(request_dict['user_id']),
            request_date=request_dict['request_date']
        )