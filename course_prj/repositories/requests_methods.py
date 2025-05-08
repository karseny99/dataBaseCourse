
from repositories.connector import *
from models.request_model import Request

from datetime import datetime, timedelta

def add_request(user_id: int) -> int:
    '''
        Returns new request_id if last request not exists or expired  
        None if request date was not expired
    '''

    with get_session(Reader) as session:
        seven_days_ago = datetime.now() - timedelta(days=7)
        select_query = text("""
            SELECT request_id 
            FROM admin_requests 
            WHERE user_id = :user_id AND request_date >= :seven_days_ago
        """)

        old_request = session.execute(select_query, {
            'user_id': user_id,
            'seven_days_ago': seven_days_ago
        }).fetchone()

        if old_request:
            return None 

        insert_query = text("""
            INSERT INTO admin_requests (user_id, request_date)
            VALUES (:user_id, :request_date)
            RETURNING request_id
        """)

        new_request = session.execute(insert_query, {
            'user_id': user_id,
            'request_date': datetime.now()
        })

        new_request_id = new_request.fetchone()[0]
        return new_request_id


def get_admin_requested_users() -> list:
    '''
        Returns list of user_ids who sent admin request
    '''

    with get_session(Admin) as session:
        select_query = text("""
            SELECT user_id 
            FROM admin_requests
        """)
        users = session.execute(select_query)
        user_ids = [user[0] for user in users]
        return user_ids
    

def remove_from_requests(user_id: int) -> int:
    '''
        Removes user_id from admin_requests
        Returns request_id if user_id exists
        None otherwise
    '''

    with get_session(Admin) as session:
        select_query = text("""
            SELECT request_id 
            FROM admin_requests 
            WHERE user_id = :user_id
        """)

        result = session.execute(select_query, {'user_id': user_id})
        request = result.fetchone()

        if not request:
            return None
        
        request_id = request[0]

        delete_query = text("""
            DELETE FROM admin_requests 
            WHERE request_id = :request_id
        """)
        session.execute(delete_query, {'request_id': request_id})
        
        return request_id