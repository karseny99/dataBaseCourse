
from repositories.connector import *
from models.author_model import Author
from sqlalchemy.orm.exc import NoResultFound


def get_authors_by_name(authors_name: str) -> list:
    '''
        For given author's name getting all fit authors
        Returns a list of author objects
    '''
    with get_session() as session:
        authors = session.query(Author).filter(Author.name.ilike(f"%{authors_name}%")).all()
        authors = [Author.from_orm(obj) for obj in authors]
        return authors