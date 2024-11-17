import repositories.comments_methods 

comments_n = 10

def add_comment(book_id: int, user_id: int, comment: str) -> int:
    '''
        Appends new comment of book_id from user_id to database
        Returns comment_id if successfully added
    '''
    return repositories.comments_methods.add_comment(book_id, user_id, comment)


def get_last_comments(book_id: int) -> list:
    '''
        Calls for a function to get a list of comms 
        Returns last comms if existed
        Otherwise returns empty list
    '''

    comments = repositories.comments_methods.get_last_comments(book_id, comments_n)

    if not comments:
        return []

    comments = [comm.__dict__ for comm in comments]
    return comments
