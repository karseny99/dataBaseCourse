
from datetime import datetime
from repositories.connector import *
from models.user_model import User
from sqlalchemy.orm.exc import NoResultFound

from services.logger import *

def add_new_user(username: str, email: str, password_hash: str, role = 'reader') -> int:
    
    '''
        Function adds new user to a database
        Returns a distinct user_id
    '''


    with get_session(Authenticator) as session:
        insert_query = text("""
            INSERT INTO users (username, email, password_hash, role, register_date)
            VALUES (:username, :email, :password_hash, :role, :register_date)
            RETURNING user_id
        """)

        result = session.execute(insert_query, {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'role': role,
            'register_date': datetime.now()
        })

        new_user_id = result.fetchone()[0]

        logging.info(f"User with id {new_user_id} has been added to database")
        return new_user_id


def get_all_usernames() -> list:
    '''
        Returns all registered usernames
    '''
    with get_session(Authenticator) as session:
        usernames = session.execute(text("SELECT username FROM users")).fetchall()
        return [username[0] for username in usernames]


def get_all_emails() -> list:
    '''
        Returns all registered emails
    '''
    with get_session(Authenticator) as session:
        emails = session.execute(text("SELECT email FROM users")).fetchall()
        return [email[0] for email in emails]
    

def get_user_info(login: str) -> User:
    '''
        Returns info about user with given login 
    '''

    with get_session(Authenticator) as session:
        user = None
        try:
            query = text("""
                SELECT * 
                FROM users 
                WHERE username = :login
            """)

            user = session.execute(query, {'login': login}).mappings().one()
            return User.from_dict(user)
        except NoResultFound:
            logging.info(f"User with login {login} not found in usernames, will try to find in emails")
        
        try:
            query = text("""
                SELECT * 
                FROM users 
                WHERE email = :login
            """)
            user = session.execute(query, {'login': login}).mappings().one()
            return User.from_dict(dict(zip(user.keys(), user)))

        except NoResultFound:
            logging.info(f"User with login {login} not found in database")
            return None
    

def get_user_id_info(user_id: int) -> User:
    '''
        Returns info about user with given user_id 
    '''

    with get_session(Reader) as session:
        query = text("""
            SELECT * 
            FROM users 
            WHERE user_id = :user_id
        """)
        user = session.execute(query, {'user_id': user_id}).mappings().fetchone()

        if not user:
            return None

        return User.from_dict(user)


def get_user_ids() -> list:
    '''
        Returns list of existed user_ids
    '''
    with get_session(Reader) as session:
        query = text("SELECT user_id FROM users")

        user_ids = session.execute(query).fetchall()
        return [user_id[0] for user_id in user_ids]
    

def set_user_admin(user_id: int) -> int:
    '''
        Returns for new admin user_id if successfully changed
        None otherwise
    '''

    with get_session(Admin) as session:
        query = text("""
            SELECT user_id 
            FROM users 
            WHERE user_id = :user_id
        """)

        user = session.execute(query, {'user_id': user_id}).one_or_none()

        if not user:
            return None
        
        update_query = text("""
            UPDATE users SET role = 'admin' 
            WHERE user_id = :user_id
        """)
        
        session.execute(update_query, {'user_id': user_id})
        return user_id