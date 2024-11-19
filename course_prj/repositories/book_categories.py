
from repositories.connector import *
from models.book_model import Book
from models.category_model import Category
from models.book_categories_model import BookCategories


def get_book_categories(book_id: str) -> list:
    '''
        Returns all book's categories
    '''
    
    with get_session() as session:
        categories = session.query(Category) \
            .join(BookCategories, Category.category_id == BookCategories.category_id) \
                .filter(BookCategories.book_id == book_id).all()
        categories = [Category.from_orm(category) for category in categories]
        return categories


def insert_categories_by_book(categories: list, book_id: int) -> None:

    '''
        Inserts a list of categories related to book_id
    '''

    with get_session() as session:

        for category in categories:
            category_obj = session.query(Category).filter(Category.category_name == category).one_or_none()

            if not category_obj:
                category_obj = Category(
                    category_name=category,
                )
                session.add(category_obj)
                session.commit()
            
            new_book_category_relation = BookCategories(
                category_id=category_obj.category_id,
                book_id=book_id
            )
            session.add(new_book_category_relation)
        print(f"{categories} was inserted to book-category table")
        session.commit()
    