
from datetime import datetime
from repositories.connector import *
from models.user_model import User
from sqlalchemy.orm.exc import NoResultFound

def add_new_user(username: str, email: str, password_hash: str, role = 'reader') -> int:
    
    '''
        Function adds new user to a database
        Returns a distinct user_id
    '''

    new_user = User(
                    username=username,
                    email=email,
                    password_hash=password_hash,
                    role=role,
                    register_date=datetime.now()
    )

    with get_session() as session:
        session.add(new_user)
        session.commit()

        print(f"User with id {new_user.user_id} has been added to database")
        return new_user.user_id


def get_all_usernames() -> list:
    '''
        Returns all registered usernames
    '''
    with get_session() as session:
        usernames = [name[0] for name in session.query(User.username).all()]
        return usernames


def get_all_emails() -> list:
    '''
        Returns all registered emails
    '''
    with get_session() as session:
        email = [email[0] for email in session.query(User.email).all()]
        return email
    
def get_user_info(login: str) -> User:
    '''
        Returns info about user with given login 
    '''

    with get_session() as session:
        user = None
        try:
            user = User.from_orm(session.query(User).filter_by(username=login).one())
            return user
        except NoResultFound:
            print(f"User with login {login} not found in usernames, will try to find in emails")
        
        try:
            user = User.from_orm(session.query(User).filter_by(email=login).one())
            return user
        except NoResultFound:
            print(f"User with login {login} not found in database")
            return None
    
