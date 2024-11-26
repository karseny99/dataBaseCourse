from models.rating_model import Rating
from models.book_model import Book
from repositories.connector import *
from services.logger import *
from datetime import datetime

def get_scored_books(user_id: int) -> list:
    '''
        Returns all scored book_ids for user_id
    '''

    with get_session(Reader) as session:
        select_query = text("""
            SELECT book_id 
            FROM ratings 
            WHERE user_id = :user_id
        """)

        book_ids = session.execute(select_query, {'user_id': user_id})

        return [book[0] for book in book_ids]


def add_or_update_rating(book_id: int, user_id: int, rating: int) -> int:
    '''
        Appends rating for book_id from user_id or updates existed
        Returns new rating_id
    '''
    with get_session(Reader) as session:
        select_query = text("""
            SELECT rating_id 
            FROM ratings 
            WHERE book_id = :book_id AND user_id = :user_id
        """)

        existing_rating_result = session.execute(select_query, {'book_id': book_id, 'user_id': user_id})
        existing_rating = existing_rating_result.fetchone()

        if existing_rating:
            rating_id = existing_rating[0]

            update_query = text("""
                UPDATE ratings 
                SET rating = :rating, rated_at = :rated_at 
                WHERE rating_id = :rating_id
            """)

            session.execute(update_query, {
                'rating': rating,
                'rated_at': datetime.now(),
                'rating_id': rating_id
            })

            logging.info(f"Old rating with id {existing_rating.rating_id} changed to {rating}")
            return rating_id
        else:
            insert_query = text("""
                INSERT INTO ratings (user_id, book_id, rating, rated_at)
                VALUES (:user_id, :book_id, :rating, :rated_at)
                RETURNING rating_id
            """)

            result = session.execute(insert_query, {
                'user_id': user_id,
                'book_id': book_id,
                'rating': rating,
                'rated_at': datetime.now()
            })
            new_rating_id = result.fetchone()[0]

            logging.info(f"New rating with id {new_rating_id} has been added to database")
            return new_rating_id



def get_book_score_from_user(book_id: int, user_id: int) -> dict:
    '''
        Finds user's score for book_id if exists
        Return rating and rated_at date
    '''

    with get_session(Reader) as session:
        select_query = text("""
            SELECT rating, rated_at 
            FROM ratings_view 
            WHERE book_id = :book_id AND user_id = :user_id
        """)
        rating = session.execute(select_query, {'book_id': book_id, 'user_id': user_id}).mappings()
        rating = rating.fetchone()

        if not rating:
            return None
        
        logging.info(f"Rating of {book_id} from user {user_id} was found")
        return rating
    

def get_book_rating_info(book_id: int) -> dict:
    '''
        Returns num of ratings and avg rating
        None if not exists
    '''

    with get_session(Reader) as session:
        select_query = text("""
            SELECT 
                COUNT(rating_id) AS ratings_count, 
                AVG(rating) AS average_rating 
            FROM ratings_view 
            WHERE book_id = :book_id
        """)

        rating = session.execute(select_query, {'book_id': book_id})
        rating = rating.fetchone()
        if rating is None:
            return None

        return dict({"ratings_count": rating[0], \
                      "average_rating": rating[1]})


# unnecessary
def get_scored_books_info(user_id: int) -> list:
    '''
        Returns list item of books rated by user_id
        item = [book_id, book's title, rating, rated_at]
    '''

    with get_session(Reader) as session:
        
        select_query = text("""
            SELECT 
                r.book_id, 
                b.title, 
                r.rating, 
                r.rated_at 
            FROM ratings r
            JOIN books b ON b.book_id = r.book_id
            WHERE r.user_id = :user_id
        """)
        
        items = session.execute(select_query, {'user_id': user_id})

        items = [
            {
                "book_id" : book_id,
                "title": title,
                "rating": rating,
                "rated_at": rated_at
            }
            for book_id, title, rating, rated_at in items
        ]

        return items