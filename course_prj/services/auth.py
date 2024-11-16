
import re
import bcrypt

from repositories.users_methods import *
from models.user_model import User

class LoginException(Exception):
    '''Base class for login exception'''
    pass

class WrongEnterException(LoginException):
    '''Exception thrown when wrong data entered'''
    def __init__(self, message="Wrong data entered"):
        self.message = message
        super().__init__(self.message)




class Authentication:

    def login_user(login: str, password: str) -> int:
        '''
            Calls function for checking if there is existed login password in database
            Returns distinct user_id 
        '''
        user_info = get_user_info(login.strip().lower())

        if user_info is None:
            print(f"There is no such user in database")
            raise WrongEnterException

        if bcrypt.checkpw(password.encode('utf-8'), user_info.password_hash.encode('utf-8')):
            return user_info.user_id
        else:
            print(f"User {login} was found in database but password is wrong!")
            raise WrongEnterException
