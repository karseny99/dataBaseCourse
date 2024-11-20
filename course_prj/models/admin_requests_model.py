from datetime import datetime
from models.user_model import User

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AdminRequest(Base):
    __tablename__ = 'admin_requests'
    
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.user_id), primary_key=True)
    request_date = Column(DateTime, default=datetime.now())

    @classmethod 
    def from_orm(cls, request_orm):
        return cls(
            request_id=request_orm.request_id,
            user_id=request_orm.user_id,
            request_date=request_orm.request_date
        )