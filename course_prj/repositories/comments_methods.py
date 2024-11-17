from models.comment_model import Comment
from repositories.connector import *

from datetime import datetime

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


def get_last_comments(book_id: int, comments_n: int = 10):
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

# def get_book_score_from_user(book_id: int, user_id: int) -> Rating:
#     '''
#         Finds user's score for book_id if exists
#         Return score and scored_at date
#     '''

#     with get_session() as session:
#         rating = session.query(Rating).filter(Rating.book_id == book_id, Rating.user_id == user_id).first()
        
#         if not rating:
#             return None
        
#         print(f"Rating of {book_id} from user {user_id} was found")
#         return Rating.from_orm(rating)