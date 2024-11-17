from models.user_model import User
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