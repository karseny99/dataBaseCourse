
from repositories.books_methods import *



def search(searh_request: list) -> dict:
    '''
        Search in fields Title, ISBN, Author, Year
        Calls function for searching in database for books
        Returns a list of matched books
    '''

    searh_value = searh_request[0]
    search_columns = searh_request[1]

    matched_books = []
    for column in search_columns:
        matched_books += search_in_column(searh_value, column)
    matched_books = [obj.__dict__ for obj in matched_books]
    return matched_books
