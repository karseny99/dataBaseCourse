from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

class Category():
    __tablename__ = 'categories'
    
    def __init__(self, category_id: int, category_name: str):
        self.category_id = category_id
        self.category_name = category_name

    @classmethod 
    def from_dict(cls, category_dict):
        return cls(
            category_id=int(category_dict['category_id']),
            category_name=category_dict['category_name']
        )
