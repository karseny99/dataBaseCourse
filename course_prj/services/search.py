
from repositories.books_methods import *
from repositories.books_authors_methods import get_authors_from_book


def search(searh_request: list) -> list:
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
    
    # Drop duplicates
    unique_matched_books = []
    unique_ids = set()
    for book in matched_books:
        if book['book_id'] not in unique_ids:
            unique_ids.add(book['book_id'])
            unique_matched_books.append(book)
    matched_books = unique_matched_books

    for i in range(len(matched_books)):
        matched_books[i]['authors'] = [author.__dict__['name'] for author in get_authors_from_book(matched_books[i]['book_id'])]
        
    return matched_books
