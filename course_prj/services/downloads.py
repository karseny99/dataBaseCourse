
from repositories.users_methods import *
from repositories.books_methods import *
from repositories.downloads_methods import *

class DownloadException(Exception):
    '''Base class for download exception'''
    pass

class UnknownUserException(DownloadException):
    '''Exception thrown when wrong user_id entered'''
    def __init__(self, message="Wrong user_id entered"):
        self.message = message
        super().__init__(self.message)

class UnknownBookException(DownloadException):
    '''Exception thrown when wrong book_id entered'''
    def __init__(self, message="Wrong book_id entered"):
        self.message = message
        super().__init__(self.message)



def add_download(user_id: int, book_id: int) -> int:
    '''
        Calls for insertion of download event
        Returns download_id
    '''

    user_ids = get_user_ids()
    if user_id not in user_ids:
        raise UnknownUserException()
    
    book_ids = get_book_ids()
    if book_id not in book_ids:
        raise UnknownBookException()
    
    return add_download_event(user_id, book_id)