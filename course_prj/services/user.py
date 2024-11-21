
from repositories.users_methods import get_user_id_info, set_user_admin
from repositories.comments_methods import get_user_actions
from repositories.requests_methods import get_admin_requested_users, remove_from_requests
from psycopg2 import OperationalError, connect

import streamlit as st
import os
import json
from datetime import datetime

def is_admin() -> bool:
    if 'user_id' not in st.session_state:
        return False

    user_id = st.session_state.user_id
    user = get_user_info(user_id)

    if not user or user['role'] != 'admin':
        return False
    
    return True


def get_user_info(user_id: int) -> dict:
    '''
        Returns user-object as a dict, according to user_model
        Removes 'password_hash'
        Returns None if user_id not exists
    '''
    user_info = get_user_id_info(user_id)
    if not user_info:
        return None
    else:
        user_info = user_info.__dict__
        _ = user_info.pop('password_hash')
    
    return user_info


@st.cache_data
def get_info_actions_user(user_id: int) -> dict:
    '''
        Requests function to get user's info if exists
        Contains basics from users table and additional info such as
        all sent comments_info, ratings_info, downloads_info 
    '''

    user_info = get_user_info(user_id)
    user_actions = get_user_actions(user_id)

    if user_actions:
        user_info['actions'] = user_actions 

    return user_info


def get_info_data_file() -> str:
    '''
        Creates a txt file with data & actions for each user who sent admin-requst
    '''
    users_requested = get_admin_requested_users()

    filename = "data.txt"
    save_path = os.path.join("storage", filename)

    try:
        remove_file(filename)
    except:
        pass

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "a") as data_file:

        for user_id in users_requested:
            info_data = get_info_actions_user(user_id[0])

            # Cleaning given dict for json dump
            info_data.pop('_sa_instance_state', None)
            info_data['register_date'] = info_data['register_date'].isoformat()
                        
            for action in info_data.get('actions', []):
                if action['rated_at'] is not None:
                    action['rated_at'] = action['rated_at'].isoformat()
                if action['last_download_date'] is not None:
                    action['last_download_date'] = action['last_download_date'].isoformat()

            if 'actions' not in info_data:
                info_data['actions'] = 'No actions'

            json_data = json.dumps(info_data, ensure_ascii=False, indent=4)
            data_file.write(json_data + "\n\n")

    return save_path


def remove_file(filename: str) -> None:
    os.remove(filename)


def set_admin_role(user_id: int) -> int:
    '''
        Removes from request list
        Calls for changing user's role by user_id
        Returns user_id if successfully
        None otherwise
    '''

    if not remove_from_requests(user_id):
        return None

    return set_user_admin(user_id)


import subprocess

def create_database_dump(db_name, user, password):
    '''
        Creates dump of database,
        Returns created dump file
        None if auth data is wrong
    '''

    filename = 'storage/db.dump'

    try:
        os.environ['PGPASSWORD'] = password

        command = [
            'pg_dump',
            '-d', db_name,
            '-U', user,
            '-h', 'localhost',
            '-p', '5432',
            '-F', 'c', 
            '-f', filename
        ]

        subprocess.run(command, capture_output=True, check=True, text=True)
    except subprocess.CalledProcessError as e:
        # print(f"Cannot create dump of database, because of {e}")

        if "authentication failed" in e.stderr.lower():
            return None
        elif "connection" in e.stderr.lower():
            print(f"Cannot create dump of database, because of {e}")
            raise OperationalError("Database connection error")
    finally:
        del os.environ['PGPASSWORD']

    return filename
# create_database_dump('postgres', 'postgres', 'localhost', '5432', 'file', '1')
        
def restore_database_dump(db_name, user, password, input_file) -> int:
    '''
        Restore of database by given dump file
        Returns number if successfully dumped
        None otherwise
    '''
    try:

        save_path = os.path.join("storage", "books", input_file)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as dump_file:
            dump_file.write(input_file.getbuffer())

        os.environ['PGPASSWORD'] = password
        
        command = [
            'pg_restore',
            '-d', db_name,
            '-U', user,
            '-h', 'localhost',
            '-p', '5432',
            dump_file
        ]
        
        subprocess.run(command, capture_output=True, check=True, text=True)
    except Exception as e:
        if "connection" in e.stderr.lower():
            print(f"Cannot create dump of database, because of {e}")
            raise OperationalError("Database connection error")
        else:
            return None

    finally:
        del os.environ['PGPASSWORD']
    
    return 2**4

# restore_database_dump('postgres', 'postgres', 'localhost', 5432, 'file', '1')

def check_database_connection(db_name, user, password) -> bool:
    '''
        Check if given data is valid
        Returns true or false
    '''
    try:
        connection = connect(
            dbname=db_name,
            user=user,
            password=password,
            host='localhost', 
            port='5432'       
        )
        connection.close()
        return True
    except OperationalError as e:
        return False
