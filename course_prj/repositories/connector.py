from contextlib import contextmanager
from settings import DB_CONFIG, POOL_SIZE, POOL_MAX_SIZE
import atexit
from services.logger import logging

from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker

engines = {}
SessionMakers = {}
Authenticator = "authenticator"
Reader = "reader"
Admin = "admin"

def get_database_url(role: str) -> str:
    DATABASE_URL = f"postgresql://{DB_CONFIG[role]}:{DB_CONFIG[f'{role}_password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    return DATABASE_URL


def initialize_engines():
    global engines, SessionMakers, Authenticator, Reader, Admin
    roles = [Authenticator, Reader, Admin]
    
    for role in roles:
        database_url = get_database_url(role)
        engines[role] = create_engine(database_url, pool_size=POOL_SIZE, max_overflow=POOL_MAX_SIZE)
        SessionMakers[role] = sessionmaker(bind=engines[role])


@contextmanager
def get_session(role):
    Session = SessionMakers[role]
    session = Session()
    
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def close_session_pool():
    for engine in engines.values():
        engine.dispose()


def on_exit():
    logging.info("Closing session pool")
    close_session_pool()

atexit.register(on_exit)

initialize_engines()
