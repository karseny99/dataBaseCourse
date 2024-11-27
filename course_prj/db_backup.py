import os
import subprocess
import schedule
import time
from datetime import datetime

from services.logger import *

DUMP_RETENTION_DAYS = 1
DUMP_DIR = os.getenv('SAVE_PATH')

def dump_db(dump_file, db_name, db_user, db_password, db_host, db_port):

    os.environ['PGPASSWORD'] = db_password

    dump_command = [
        'pg_dump',
        '--no-owner',
        '-Fc',
        '-h', db_host,
        '-p', db_port,
        '-U', db_user,
        db_name,
        '-f', dump_file
    ]

    try:
        subprocess.run(dump_command, check=True)
        logging.info(f"Backup successful: {dump_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during backup: {e}")


def backup_database() -> None:
    '''
        Backups database every 24h
    '''
    save_path = os.getenv('SAVE_PATH')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')

    dump_file = save_path + f"backup_{db_name}_{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}.dump"

    dump_db(dump_file, db_name, db_user, db_password, db_host, db_port)


def delete_old_dumps():
    now = time.time()
    cutoff = now - (DUMP_RETENTION_DAYS * 86400) 
    save_path = DUMP_DIR
    for filename in os.listdir(save_path):
        file_path = os.path.join(DUMP_DIR, filename)
        if os.path.isfile(file_path) and "recover" not in filename :
            file_creation_time = os.path.getctime(file_path)
            if file_creation_time < cutoff:
                os.remove(file_path)
                logging.info(f"Deleted old dump: {file_path}")


schedule.every().minute.do(backup_database)
schedule.every().minute.do(delete_old_dumps)


if __name__ == "__main__":
    while True:
        print(time.time())
        schedule.run_pending()
        time.sleep(60)