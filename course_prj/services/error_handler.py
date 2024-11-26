
from sqlalchemy.exc import OperationalError
import psycopg2
from pages.error import call_display_page
from services.logger import *

def handle_error(e):
    logging.error(e)
    # print(f"\n\n {e} \n\n{type(e)} \n\n")
    if isinstance(e, OperationalError) or isinstance(e, psycopg2.OperationalError):
        call_display_page("Cannot load from database ...")
    else:
        print(f"else: {e}")

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return handle_error(e)
    return wrapper
