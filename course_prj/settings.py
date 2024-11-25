import os

# Without docker
# from dotenv import load_dotenv

# load_dotenv("env.env")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "authenticator": os.getenv("AUTHENTICATOR_USER"),
    "authenticator_password": os.getenv("AUTHENTICATOR_PASSWORD"),
    "reader": os.getenv("READER_USER"),
    "reader_password": os.getenv("READER_PASSWORD"),
    "admin": os.getenv("ADMIN_USER"),
    "admin_password": os.getenv("ADMIN_PASSWORD"),
}

POOL_SIZE = int(os.getenv("POOL_SIZE", 10))
POOL_MAX_SIZE = int(os.getenv("POOL_MAX_SIZE", 20))