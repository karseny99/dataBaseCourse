from models.book_model import Book
from models.download_model import Download
from repositories.connector import *
from services.logger import * 
from datetime import datetime


def add_download_event(user_id: int, book_id: int) -> int:
    '''
        Appending download event to database
        Returns new download_id
    '''

    with get_session() as session:

        insert_query = text("""
            INSERT INTO downloads (user_id, book_id, download_date)
            VALUES (:user_id, :book_id, :download_date)
            RETURNING download_id
        """)

        new_download_event = session.execute(insert_query, {
            'user_id': user_id,
            'book_id': book_id,
            'download_date': datetime.now()
        })

        new_download_id = new_download_event.fetchone()[0]

        logging.info(f"Download event with id {new_download_id} has been added to database")
        return new_download_id
    
# unnecessary
def get_downloads_info(user_id: int) -> list:
    '''
        Returns list item of downloads info
        item = [download_id, download_date, book_id, book's title]
    '''

    with get_session() as session:
        select_query = text("""
            SELECT 
                d.download_id, 
                d.download_date, 
                b.book_id, 
                b.title
            FROM downloads d
            JOIN books b ON b.book_id = d.book_id
            WHERE d.user_id = :user_id
        """)
        items = session.execute(select_query, {'user_id': user_id})

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

