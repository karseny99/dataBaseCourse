import logging
from sqlalchemy.exc import OperationalError
import psycopg2
from pages.error import call_display_page

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logging.getLogger().addHandler(console_handler)

def handle_error(e):
    logging.error(e)
    # print(f"\n\n {e} \n\n{type(e)} \n\n")
    if isinstance(e, OperationalError) or isinstance(e, psycopg2.OperationalError):
        # print("HERE")
        call_display_page("Cannot load from database ...")
    else:
        print("else")

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return handle_error(e)
    return wrapper
