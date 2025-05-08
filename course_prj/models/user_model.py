from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dataclasses import dataclass

Base = declarative_base()

class User:
    def __init__(self, user_id: int, username: str, email: str, password_hash: str, role: str, register_date: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.register_date = register_date

    @classmethod
    def from_dict(cls, user_dict):
        return cls(
            user_id=int(user_dict['user_id']),
            username=user_dict['username'],
            email=user_dict['email'],
            password_hash=user_dict['password_hash'],
            role=user_dict['role'],
            register_date=user_dict['register_date']
        )
