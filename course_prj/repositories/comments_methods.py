from models.comment_model import Comment
from models.book_model import Book
from models.user_model import User
from models.rating_model import Rating
from models.download_model import Download
from repositories.connector import *

from sqlalchemy import exists

from datetime import datetime

def delete_comment(comment_id: int) -> int:
    '''
        Removes comment from db by comment_id
        Returns comment_id if successfully deleted
        None otherwise
    '''

    with get_session() as session:
        deletion_request = session.query(Comment).filter(Comment.comment_id == comment_id).one_or_none()
        
        if not deletion_request:
            return None

        session.delete(deletion_request)
        session.commit()

        return comment_id


def add_comment(book_id: int, user_id: int, comment: str) -> int:
    '''
        Appends new comment of book_id from user_id to database
        Returns new comment_id
    '''
    with get_session() as session:
        new_comment = Comment(
            user_id=user_id,
            book_id=book_id,
            comment=comment,
            commented_at=datetime.now()
        )

        session.add(new_comment)
        session.commit()

        print(f"New comment with id {new_comment.comment_id} from {user_id}-user to {book_id}-book")
        return new_comment.comment_id


def get_last_comments(book_id: int, comments_n: int = 10) -> list:
    '''
        Returns last 10 comments from book_id
    '''

    with get_session() as session:
        comments = session.query(Comment).filter(Comment.book_id == book_id) \
            .order_by(Comment.commented_at.desc()).limit(comments_n).all()

        if not comments:
            return []
    
        comments = [Comment.from_orm(comm) for comm in comments]
        return comments

# unnecessary
def get_user_comments_info(user_id: int) -> list:
    '''
        Returns a list of comments sent by user_id
        returns item is [comment_id, comment, commented_at, book_id, book's title]
    '''

    with get_session() as session:
        items = session.query(
            Comment.comment_id, 
            Comment.comment,
            Comment.commented_at,
            Book.book_id,
            Book.title
        ).join(Book, Book.book_id == Comment.book_id) \
            .filter(Comment.user_id == user_id).all()
    
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

    with get_session() as session:


        items = session.query(
            Book.book_id,
            Book.title,
            func.max(Rating.rating),
            func.max(Rating.rated_at),
            func.count(Comment.comment).label("comment_count"),
            func.max(Download.download_date).label("last_download_date")
        ) \
            .outerjoin(Rating, (Rating.book_id == Book.book_id) & (Rating.user_id == user_id)) \
            .outerjoin(Comment, (Comment.book_id == Book.book_id) & (Comment.user_id == user_id)) \
            .outerjoin(Download, (Download.book_id == Book.book_id) & (Download.user_id == user_id)) \
        .group_by(Book.book_id, Book.title).all()


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
