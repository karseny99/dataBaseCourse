
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


    