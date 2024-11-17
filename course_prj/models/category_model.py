from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), nullable=False)

    @classmethod 
    def from_orm(cls, category_orm):
        return cls(
            category_id=category_orm.category_id,
            category_name=category_orm.category_name
        )
