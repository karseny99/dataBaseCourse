from models.comment_model import Comment
from models.book_model import Book
from models.user_model import User
from models.rating_model import Rating
from models.download_model import Download
from repositories.connector import *

from sqlalchemy import exists
from services.logger import *
from datetime import datetime

def delete_comment(comment_id: int) -> int:
    '''
        Removes comment from db by comment_id
        Returns comment_id if successfully deleted
        None otherwise
    '''

    with get_session(Admin) as session:
        query = text("""
            SELECT * FROM comments 
            WHERE comment_id = :comment_id
        """)

        deletion_request = session.execute(query, {"comment_id": comment_id}).fetchone()
        
        if not deletion_request:
            return None
        
        delete_query = text("""
            DELETE FROM comments 
            WHERE comment_id = :comment_id
        """)
        session.execute(delete_query, {"comment_id": comment_id})

        return comment_id


def add_comment(book_id: int, user_id: int, comment: str) -> int:
    '''
        Appends new comment of book_id from user_id to database
        Returns new comment_id
    '''
    with get_session(Reader) as session:

        insert_query = text("""
            INSERT INTO comments (user_id, book_id, comment, commented_at)
            VALUES (:user_id, :book_id, :comment, :commented_at)
            RETURNING comment_id
        """)

        new_comment = session.execute(insert_query, {
            'user_id': user_id,
            'book_id': book_id,
            'comment': comment,
            'commented_at': datetime.now()
        })

        new_comment_id = new_comment.fetchone()[0]

        logging.info(f"New comment with id {new_comment_id} from {user_id}-user to {book_id}-book")
        return new_comment_id


def get_last_comments(book_id: int, comments_n: int = 10) -> list:
    '''
        Returns last 10 comments from book_id
    '''

    with get_session(Reader) as session:
        select_query = text("""
            SELECT * 
            FROM comments_view 
            WHERE book_id = :book_id
            ORDER BY commented_at DESC
            LIMIT :comments_n
        """)

        comments = session.execute(select_query, {
            'book_id': book_id,
            'comments_n': comments_n
        }).mappings()

        comments = [dict(comm) for comm in comments]
        return comments


# unnecessary
def get_user_comments_info(user_id: int) -> list:
    '''
        Returns a list of comments sent by user_id
        returns item is [comment_id, comment, commented_at, book_id, book's title]
    '''

    with get_session(Reader) as session:
        select_query = text("""
            SELECT c.comment_id, c.comment, c.commented_at, b.book_id, b.title
            FROM comments c
            JOIN books b ON b.book_id = c.book_id
            WHERE c.user_id = :user_id
        """)

        items = session.execute(select_query, {'user_id': user_id})

        items = [
            {
                "comment_id": comment_id,
                "comment": comment,
                "commented_at": commented_at,
                "book_id": book_id,
                "title": title
            }
            for comment_id, comment, commented_at, book_id, title in items
        ]

        return items
    

def get_user_actions(user_id: int) -> list:
    '''
        Returns a list of book's actions made by user_id
        returns item is [book_id, title, rating, rated_at, comment_count, last_download_date]
    '''

    with get_session(Reader) as session:

        select_query = text("""
            SELECT 
                b.book_id,
                b.title,
                MAX(r.rating) AS rating,
                MAX(r.rated_at) AS rated_at,
                COUNT(c.comment) AS comment_count,
                MAX(d.download_date) AS last_download_date
            FROM books b
            LEFT JOIN ratings_view r ON r.book_id = b.book_id AND r.user_id = :user_id
            LEFT JOIN comments_view c ON c.book_id = b.book_id AND c.user_id = :user_id
            LEFT JOIN downloads_view d ON d.book_id = b.book_id AND d.user_id = :user_id
            GROUP BY b.book_id, b.title
            HAVING 
                MAX(r.rating) IS NOT NULL OR 
                COUNT(c.comment) > 0 OR 
                MAX(d.download_date) IS NOT NULL
        """)
        items = session.execute(select_query, {'user_id': user_id})

        items = [
            {
                "book_id": book_id,
                "title": title,
                "rating": rating,
                "rated_at": rated_at,
                "comment_count": comment_count,
                "last_download_date": last_download_date,
            }
            for book_id, title, rating, rated_at, comment_count, last_download_date in items
        ]

        return items
