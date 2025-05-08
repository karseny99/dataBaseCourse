from repositories.connector import *
from db_backup import *
from settings import DB_CONFIG
from psycopg2 import OperationalError
from sqlalchemy import text

def restore_database_from_file(filename: str) -> None:
    '''
        Deletes all tables & triggers, then calls for recovery
        If unsuccessfully then rollbacks db
    '''
    with get_session(Admin) as session:
        db_recovery(filename)

def db_recovery(filename: str) -> None:

    '''
        Restoring database from <filename>
    '''

    db_name = DB_CONFIG['dbname']
    db_user = DB_CONFIG['user']
    db_password = DB_CONFIG['password']
    db_host = DB_CONFIG['host']
    db_port = DB_CONFIG['port']

    os.environ['PGPASSWORD'] = db_password
    command = [
        'pg_restore',
        '--clean',
        '-d', db_name,
        '-U', db_user,
        '-h', db_host,
        '-p', db_port,
        '--no-owner',
        filename
    ]

    try:
        subprocess.run(command, capture_output=True, check=True, text=True)
    except subprocess.CalledProcessError as e:
        raise OperationalError("Error output:" + e.stderr)  # Выводим текст ошибки
    except Exception as e:
        raise OperationalError(f"Database connection error: {str(e)}")
    finally:
        del os.environ['PGPASSWORD']
