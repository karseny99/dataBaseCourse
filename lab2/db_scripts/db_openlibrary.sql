-- Проверяем существование БД
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'openlibrary') THEN
    CREATE DATABASE openlibrary;
  END IF;
END $$;

-- Подключаемся к БД
\c openlibrary
