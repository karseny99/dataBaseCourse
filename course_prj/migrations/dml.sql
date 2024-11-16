-- Вставка пользователей
INSERT INTO users (username, email, password_hash, role, register_date) VALUES
('admin_user', 'admin@example.com', 'hashed_password_1', 'admin', NOW()),
('reader_user', 'reader@example.com', 'hashed_password_2', 'reader', NOW());

-- Вставка авторов
INSERT INTO authors (name, bio) VALUES
('Автор 1', 'Биография автора 1'),
('Автор 2', 'Биография автора 2');

-- Вставка книг
INSERT INTO books (title, published_year, isbn, description, added_at) VALUES
('Книга 1', 2021, '978-3-16-148410-0', 'Описание книги 1', NOW()),
('Книга 2', 2022, '978-1-23-456789-7', 'Описание книги 2', NOW());

-- Вставка жанров
INSERT INTO categories (category_name) VALUES
('Фантастика'),
('Научная литература');

-- Связывание книг и авторов
INSERT INTO book_authors (author_id, book_id) VALUES
(1, 1),  -- Автор 1 написал Книгу 1
(2, 2);  -- Автор 2 написал Книгу 2

-- Связывание книг и жанров
INSERT INTO book_categories (book_id, category_id) VALUES
(1, 1),  -- Книга 1 относится к жанру Фантастика
(2, 2);  -- Книга 2 относится к жанру Научная литература

-- Вставка загрузок
INSERT INTO downloads (user_id, book_id, download_date) VALUES
(1, 1, NOW()),  -- Пользователь 1 скачал Книгу 1
(2, 2, NOW());  -- Пользователь 2 скачал Книгу 2

-- Вставка отзывов
INSERT INTO reviews (user_id, book_id, rating, comment, reviewed_at) VALUES
(1, 1, 5, 'Отличная книга!', NOW()),  -- Пользователь 1 оставил отзыв на Книгу 1
