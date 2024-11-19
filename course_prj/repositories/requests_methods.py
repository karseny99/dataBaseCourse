
from repositories.connector import *
from models.request_model import Request

from datetime import datetime, timedelta

def add_request(user_id: int) -> int:
    '''
        Returns new request_id if last request not exists or expired  
        None if request date was not expired
    '''

    with get_session() as session:
        seven_days_ago = datetime.now() - timedelta(days=7)
        old_request = session.query(Request).filter((Request.user_id == user_id) \
                & (Request.request_date >= seven_days_ago)).one_or_none()

        if old_request:
            return None 

        new_request = Request(
            user_id=user_id,
            request_date=datetime.now()
        )

        session.add(new_request)
        session.commit()

        return new_request.request_id



    