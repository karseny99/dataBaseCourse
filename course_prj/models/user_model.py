from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dataclasses import dataclass

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(10), default='reader', nullable=False)
    register_date = Column(DateTime, default=datetime.now)

    @classmethod 
    def from_orm(cls, user_orm):
        return cls(
            user_id = user_orm.user_id,
            username = user_orm.username,
            email = user_orm.email,
            password_hash = user_orm.password_hash,
            role = user_orm.role,
            register_date = user_orm.register_date
        )
