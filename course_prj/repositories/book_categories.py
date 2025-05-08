
from repositories.connector import *
from models.book_model import Book
from models.category_model import Category
from models.book_categories_model import BookCategories
from services.logger import *

def add_category(new_category: str) -> int:
    '''
        Returns category_id if success
        None otherwise
    '''

    query_validate = text("""
        SELECT category_id
        FROM categories
        WHERE category_name = :category_name
    """)

    insert_query = text("""
        INSERT INTO categories (category_name) 
        VALUES (:category_name) 
        RETURNING category_id
    """)

    with get_session(Admin) as session:
        category_id = session.execute(query_validate, {"category_name": new_category}).fetchone()

        if category_id:
            return None
        
        new_category_id = session.execute(insert_query, {"category_name": new_category}).fetchone() 
        new_category_id = new_category_id[0]

        logging.info(f"New category inserted: {new_category}")
        return new_category_id


def get_categories() -> list:
    '''
        Returns list of all categories
    '''

    with get_session(Reader) as session:
        query = text("""
            SELECT category_name
            FROM categories
        """)

        categories = session.execute(query).scalars().all()
        return categories


def get_book_categories(book_id: str) -> list:
    '''
        Returns all book's categories
    '''
    
    with get_session(Reader) as session:

        query = text("""
            SELECT category_name
            FROM books_with_categories
            WHERE book_id = :book_id
        """)

        categories = session.execute(query, {"book_id": book_id}).scalars().all()
        return [category[0] for category in categories]

def insert_categories_by_book(categories: list, book_id: int) -> None:
    '''
        Inserts a list of categories related to book_id
    '''

    with get_session(Admin) as session:
        for category in categories:
            query = text("""
                SELECT category_id 
                FROM categories 
                WHERE category_name = :category_name
            """)

            category_obj = session.execute(query, {"category_name": category}).fetchone()

            if not category_obj:
                insert_query = text("""
                    INSERT INTO categories (category_name) 
                    VALUES (:category_name) 
                    RETURNING category_id
                """)
                category_obj = session.execute(insert_query, {"category_name": category}).fetchone()  

            category_id = category_obj[0]

            insert_relation_query = text("""
                INSERT INTO book_categories (book_id, category_id) 
                VALUES (:book_id, :category_id)
            """)
            session.execute(insert_relation_query, {"book_id": book_id, "category_id": category_id})

        logging.info(f"{categories} was inserted to book-category table")