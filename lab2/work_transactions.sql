Добавление нового произведения с проверкой автора
BEGIN;

-- Проверяем существование автора или создаем нового
WITH author_data AS (
    SELECT key FROM authors WHERE name = 'Лев Толстой' LIMIT 1
),
new_author AS (
    INSERT INTO authors (key, name, created_at)
    SELECT '/authors/OL' || (random()*1000000)::int || 'A', 'Лев Толстой', NOW()
    WHERE NOT EXISTS (SELECT 1 FROM author_data)
    RETURNING key
),
-- Добавляем новое произведение
new_work AS (
    INSERT INTO works (key, title, published_year, added_at)
    VALUES (
        '/works/OL' || (random()*1000000)::int || 'W',
        'Война и мир',
        1869,
        NOW()
    )
    RETURNING key
)
-- Связываем автора и произведение
INSERT INTO author_works (author_key, work_key)
SELECT 
    COALESCE((SELECT key FROM author_data), (SELECT key FROM new_author)),
    (SELECT key FROM new_work);

COMMIT;








Перемещение произведения к другому автору
BEGIN ISOLATION LEVEL REPEATABLE READ;

-- Блокируем строки для изменения
SELECT * FROM author_works 
WHERE work_key = '/works/OL2076996W' 
FOR UPDATE;

-- Удаляем старую связь
DELETE FROM author_works 
WHERE work_key = '/works/OL2076996W' 
AND author_key = '/authors/OL121938A';

-- Добавляем новую связь
INSERT INTO author_works (author_key, work_key)
VALUES ('/authors/OL12193903A', '/works/OL2076996W');

COMMIT;








Удаление автора и всех его произведений
BEGIN;

-- Блокируем автора и все его связи
SELECT * FROM authors 
WHERE key = '/authors/OL12193928A' 
FOR UPDATE;

SELECT * FROM author_works 
WHERE author_key = '/authors/OL12193928A' 
FOR UPDATE;

-- Удаляем связи с произведениями
DELETE FROM author_works 
WHERE author_key = '/authors/OL12193928A';

-- Удаляем автора
DELETE FROM authors 
WHERE key = '/authors/OL12193928A';

COMMIT;







Неповторяющееся чтение (Repeatable Read)
-- Сессия 1
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT COUNT(*) FROM author_works 
WHERE author_key = '/authors/OL12193912A';

-- Сессия 2 
INSERT INTO author_works (author_key, work_key)
VALUES ('/authors/OL12193912A', '/works/OL20770138W');
COMMIT;

-- Сессия 1 
SELECT COUNT(*) FROM author_works 
WHERE author_key = '/authors/OL12193912A';
COMMIT;



-----------------------------------------------------------
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT COUNT(*) FROM author_works
WHERE author_key = '/authors/OL12193912A';
BEGIN
 count
-------
     0
(1 row)

openlibrary=*# SELECT COUNT(*) FROM author_works
WHERE author_key = '/authors/OL12193912A';
COMMIT;
 count
-------
     0
(1 row)

COMMIT
-------------------PARALLEL---------------------------------
INSERT INTO author_works (author_key, work_key)
VALUES ('/authors/OL12193912A', '/works/OL20770138W');
COMMIT;
INSERT 0 1
WARNING:  there is no transaction in progress
COMMIT
------------------THEN-------------------------------------
openlibrary=# BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT COUNT(*) FROM author_works
WHERE author_key = '/authors/OL12193912A';
BEGIN
 count
-------
     1
(1 row)
---------------------------------------------------




Тест 2: Фантомное чтение (Serializable)
-- session1
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT count(*) FROM works where published_year = 2025;
BEGIN
 count
-------
     6
(1 row)

openlibrary=*# INSERT INTO works (key, title, published_year) VALUES ('/works/OL919954543210909090009099339W', 'Новая кн
ига', 2025);
INSERT 0 1

------------------- session2 -------------------
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT count(*) FROM works where published_year = 2025;
BEGIN
 count
-------
     6
(1 row)

openlibrary=*# INSERT INTO works (key, title, published_year) VALUES ('/works/OL9109996454321090909000909991W', 'Новая к
нига', 2025);
INSERT 0 1
-------------------------------------

openlibrary=*# commit;
COMMIT

------------------- session2 -------------------
commit;
ERROR:  could not serialize access due to read/write dependencies among transactions
DETAIL:  Reason code: Canceled on identification as a pivot, during commit attempt.
HINT:  The transaction might succeed if retried.
-------------------------------------




Аномалия 1: Потерянное обновление
-- Сессия 1
BEGIN;
SELECT title FROM works WHERE key = '/works/OL20770131W'; -- 'Старое название'
                                                title
-----------------------------------------------------------------------------------------------------
 Reading Critically, Writing Well 9e & Easy Writer 4e with 2009 MLA and 2010 APA Updates & CompClass

-- Сессия 2
BEGIN;
UPDATE works SET title = 'Новое название 1' WHERE key = '/works/OL20770131W';
COMMIT;
BEGIN
UPDATE 1
COMMIT

-- Сессия 1
UPDATE works SET title = 'Новое название 2' WHERE key = '/works/OL20770131W';
COMMIT;

SELECT title FROM works WHERE key = '/works/OL20770131W';
      title
------------------
 Новое название 2
------------------







Аномалия 2: Неповторяющееся чтение
-- Сессия 1
BEGIN;
SELECT AVG(published_year) FROM works 
WHERE key IN (
    SELECT work_key FROM author_works 
    WHERE author_key = '/authors/OL10000003A'
);          
        avg
-----------------------
 2021.2857142857142857
-----------------------

-- Сессия 2
INSERT INTO works (key, title, published_year)
VALUES ('/works/OL29926563042W', 'Новая книга', 2023);
INSERT INTO author_works (author_key, work_key)
VALUES ('/authors/OL10000003A', '/works/OL29926563042W');
COMMIT;
INSERT 0 1
INSERT 0 1


-- Сессия 1
SELECT AVG(published_year) FROM works 
WHERE key IN (
    SELECT work_key FROM author_works 
    WHERE author_key = '/authors/OL10000003A'
); 
COMMIT;
          avg
-----------------------
 2021.6666666666666667
-----------------------








Аномалия 3: Фантомное чтение
-- Сессия 1
BEGIN;
SELECT COUNT(*) FROM author_works 
WHERE author_key = '/authors/OL10000003A';
 count
-------
     9
-------

-- Сессия 2
INSERT INTO author_works (author_key, work_key)
VALUES ('/authors/OL10000003A', '/works/OL20770128W');
COMMIT;
INSERT 0 1

-- Сессия 1
SELECT COUNT(*) FROM author_works 
WHERE author_key = '/authors/OL10000003A'; 
COMMIT;
 count
-------
    10
-------