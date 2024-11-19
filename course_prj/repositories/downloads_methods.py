from models.book_model import Book
from models.download_model import Download
from repositories.connector import *

from datetime import datetime


def add_download_event(user_id: int, book_id: int) -> int:
    '''
        Appending download event to database
        Returns new download_id
    '''
    new_download_event = Download(
        book_id=book_id,
        user_id=user_id,
        download_date=datetime.now()
    )

    with get_session() as session:
        session.add(new_download_event)
        session.commit()

        print(f"Download event with id {new_download_event.download_id} has been added to database")
        return new_download_event.download_id
    
# unnecessary
def get_downloads_info(user_id: int) -> list:
    '''
        Returns list item of downloads info
        item = [download_id, download_date, book_id, book's title]
    '''

    with get_session() as session:
        items = session.query(
            Download.download_id, 
            Download.download_date,
            Book.book_id,
            Book.title
        ).join(Book, Book.book_id == Download.book_id) \
            .filter(Download.user_id == user_id).all()
    
        items = [
            {
                "download_id": download_id,
                "download_date": download_date,
                "book_id": book_id,
                "title": title
            }
            for download_id, download_date, book_id, title in items
        ]

        return items

