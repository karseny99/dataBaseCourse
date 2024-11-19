import logging
from sqlalchemy.exc import OperationalError

from pages.error import display_error_page

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
    if isinstance(e, OperationalError):
        display_error_page("Cannot load from database ...")
    else:
        print("else")

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return handle_error(e)
    return wrapper
