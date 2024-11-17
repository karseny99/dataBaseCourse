from models.rating_model import Rating
from repositories.connector import *

from datetime import datetime

def get_scored_books(user_id: int) -> list:
    '''
        Returns all scored book_ids for user_id
    '''

    with get_session() as session:
        book_ids = session.query(Rating.book_id).filter_by(Rating.user_id==user_id).all()
        return [book[0] for book in book_ids]


def add_or_update_rating(book_id: int, user_id: int, rating: int) -> int:
    '''
        Appends rating for book_id from user_id or updates existed
        Returns new rating_id
    '''
    with get_session() as session:
        existing_rating = session.query(Rating).filter(Rating.book_id == book_id, Rating.user_id == user_id).first()
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.rated_at = datetime.now()

            session.commit()
            print(f"Old rating with id {existing_rating.rating_id} changed to {rating}")
            return existing_rating.rating_id
        
        else:
            new_rating = Rating(
                user_id=user_id,
                book_id=book_id,
                rating=rating,
                rated_at=datetime.now()
            )

            session.add(new_rating)
            session.commit()

            print(f"New rating with id {new_rating.rating_id} has been added to database")
            return new_rating.rating_id



def get_book_score_from_user(book_id: int, user_id: int) -> Rating:
    '''
        Finds user's score for book_id if exists
        Return score and scored_at date
    '''

    with get_session() as session:
        rating = session.query(Rating).filter(Rating.book_id == book_id, Rating.user_id == user_id).first()
        
        if not rating:
            return None
        
        print(f"Rating of {book_id} from user {user_id} was found")
        return Rating.from_orm(rating)