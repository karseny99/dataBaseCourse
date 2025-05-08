import psycopg2
import time

DB_CONFIG = {
    'host': 'localhost',
    'database': 'openlibrary',
    'user': 'ol_user',
    'password': 'ol_password'
}

BATCH_SIZE = 10000
SECRET_KEY = 'key'  

def encrypt_existing_users():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE encrypted_email IS NULL;")
        total_users = cursor.fetchone()[0]
        processed = 0

        print(f'Начало шифрования данных. Всего записей для обработки: {total_users}')

        while processed < total_users:
            try:
                cursor.execute("BEGIN;")
                
                cursor.execute(f"""
                    WITH batch AS (
                        SELECT user_id, email
                        FROM users 
                        WHERE encrypted_email IS NULL
                        ORDER BY user_id
                        LIMIT {BATCH_SIZE}
                        FOR UPDATE SKIP LOCKED
                    )
                    UPDATE users u
                    SET encrypted_email = pgp_sym_encrypt(b.email, %s)
                    FROM batch b
                    WHERE u.user_id = b.user_id
                    RETURNING u.user_id;
                """, (SECRET_KEY,))

                updated_users = cursor.fetchall()
                batch_count = len(updated_users)
                processed += batch_count

                print(f'Обработано {batch_count} записей (всего {processed}/{total_users})')

                connection.commit()
            except Exception as e:
                print(f'Ошибка при обработке пачки: {e}')
                connection.rollback()  

    except Exception as e:
        print(f'Ошибка подключения к базе данных: {e}')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    encrypt_existing_users()
