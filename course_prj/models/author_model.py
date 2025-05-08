from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

class Author():
    __tablename__ = 'authors'
    
    def __init__(self, author_id: int, name: str, bio: str):
       self.author_id = author_id
       self.name = name
       self.bio = bio

    @classmethod 
    def from_dict(cls, author_dict):
        return cls(
            author_id=int(author_dict['author_id']),
            name=author_dict['name'],
            bio=author_dict['bio']
        )
