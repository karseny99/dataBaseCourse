
import re
import bcrypt

from repositories.users_methods import *
from repositories.users_methods import add_new_user


class RegistrationException(Exception):
    '''Base class for registration exception'''
    pass

class UsernameExistsException(RegistrationException):
    '''Exception thrown when username already exists in db'''
    def __init__(self, message="Username already exists"):
        self.message = message
        super().__init__(self.message)

class EmailExistsException(RegistrationException):
    '''Exception thrown when email already exists in db'''
    def __init__(self, message="Email already exists"):
        self.message = message
        super().__init__(self.message)


class Validation:

    def validate_email(email: str) -> bool:
        '''
            Validates input email
        '''
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        return bool(re.match(email_regex, email))


    def validate_password(password: str) -> bool:
        '''
            Validates input password
            password contains 
                at least one capital letter
                at least one digit
                size of password at least 8 symbols
        '''
        password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}$$$$:;"\'<>,.?/~`-]).{8,}$'

        return bool(re.match(password_regex, password))
    
    def validate_username(username: str) -> bool:
        '''
            Validates input username
        '''
        username_regex = r'^[A-Za-z0-9]{3,20}$'

        return bool(re.match(username_regex, username))


class Registration:

    def register_user(username: str, email: str, password: str) -> int:
        '''
            Checks if user has not registered already
            Calls function for insertion in database
            Returns a user_id in db
        '''
        
        registered_usernames = get_all_usernames()
        if username in registered_usernames:
            raise UsernameExistsException()

        registered_emails = get_all_emails()
        if email in registered_emails:
            raise EmailExistsException()

        # Hashing password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return add_new_user(username, email, hashed_password)
