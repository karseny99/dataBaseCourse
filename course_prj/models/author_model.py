from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)

    @classmethod 
    def from_orm(cls, author_orm):
        return cls(
            author_id=author_orm.author_id,
            name=author_orm.name,
            bio=author_orm.bio
        )
