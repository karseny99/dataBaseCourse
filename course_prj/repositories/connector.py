from contextlib import contextmanager
from settings import DB_CONFIG, POOL_SIZE, POOL_MAX_SIZE
import atexit

from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
engine = create_engine(DATABASE_URL, pool_size=POOL_SIZE, max_overflow=POOL_MAX_SIZE)
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
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
    if engine:
        engine.dispose()


def on_exit():
    print("Closing session pool")
    close_session_pool()


# Регистрируем функцию для выполнения при завершении программы
atexit.register(on_exit)