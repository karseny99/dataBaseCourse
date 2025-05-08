import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
from psycopg2.extras import execute_batch

DB_CONFIG = {
    'host': 'localhost',
    'database': 'openlibrary',
    'user': 'ol_user',
    'password': 'ol_password'
}

BATCH_SIZE = 10000  
TOTAL_USERS = 5_000_000 

def generate_users():
    fake = Faker()
    conn = None
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print(f"Starting generation of {TOTAL_USERS} users...")
        start_time = datetime.now()
        
        for batch_num in range(0, TOTAL_USERS, BATCH_SIZE):
            batch = []
            for _ in range(BATCH_SIZE):
                first_name = fake.first_name()
                last_name = fake.last_name()
                username = f"{first_name.lower()}.{last_name.lower()}"
               
                email = random.choice([username, f"{last_name.lower()}.{first_name.lower()}"])
                batch.append((
                    username,
                    f"{email + random.choice([str(random.randint(1, 999)), str(random.randint(1999, 2025))])}@{fake.free_email_domain()}",
                    f"{first_name} {last_name}",
                    fake.password(length=12),
                    fake.date_time_between(start_date='-5y', end_date='now')
                ))
            
            execute_batch(cursor, """
                INSERT INTO users (
                    username, 
                    email, 
                    full_name, 
                    password_hash,
                    register_date
                ) VALUES (
                    %s, %s, %s, 
                    crypt(%s, gen_salt('bf')), 
                    %s
                ) ON CONFLICT DO NOTHING
            """, batch)
            
            conn.commit()
            
            # Прогресс
            if batch_num % (10 * BATCH_SIZE) == 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                print(f"Inserted {batch_num + BATCH_SIZE:,} users ({elapsed:.2f} sec)")
        
        total_time = (datetime.now() - start_time).total_seconds()
        print(f"Done! Inserted {TOTAL_USERS:,} users in {total_time:.2f} seconds")
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    generate_users()