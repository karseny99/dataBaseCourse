
from repositories.connector import *

from models.author_model import Author

def get_authors_by_name(authors_name: str) -> list:
    '''
        For given author's name getting all fit authors
        Returns a list of author objects
    '''
    with get_session() as session:

        query = text("""
            SELECT * FROM authors 
            WHERE name ILIKE :name
        """)

        authors = session.execute(query, {"name": f"%{authors_name}%"}).mappings()
        authors = [Author.from_dict(dict(obj)) for obj in authors]
        return authors