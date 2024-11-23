-- Вставка пользователей
INSERT INTO users (username, email, password_hash, role, register_date) VALUES
('user1', 'user1@example.com', 'hashed_password1', 'reader', NOW()),
('user2', 'user2@example.com', 'hashed_password2', 'admin', NOW());

-- Вставка авторов
INSERT INTO authors (name, bio) VALUES
('Автор 1', 'Биография автора 1'),
('Автор 2', 'Биография автора 2');

-- Вставка категорий
INSERT INTO categories (category_name) VALUES
('Фантастика'),
('Научная литература'),
('Детская литература');

-- Вставка книг
INSERT INTO books (title, published_year, isbn, description, added_at, file_path, cover_image_path) VALUES
('Книга 1', 2021, '978-3-16-148410-0', 'Описание книги 1', NOW(), 'storage/books/book1.fb2', 'storage/covers/book1_cover.jpg'),
('Книга 2', 2020, '978-1-23-456789-7', 'Описание книги 2', NOW(), 'storage/books/book2.fb2', 'storage/covers/book2_cover.jpg');

-- Вставка связей книг и авторов
INSERT INTO book_authors (author_id, book_id) VALUES
(1, 1),  -- Автор 1 написал Книгу 1
(2, 2);  -- Автор 2 написал Книгу 2

-- Вставка жанров книг
INSERT INTO book_categories (book_id, category_id) VALUES
(1, 1),  -- Книга 1 относится к жанру Фантастика
(2, 2),  -- Книга 2 относится к жанру Научная литература
(1, 2);

-- Вставка информации о загрузках
INSERT INTO downloads (user_id, book_id, download_date) VALUES
(1, 1, NOW()),  -- Пользователь 1 скачал Книгу 1
(2, 2, NOW());  -- Пользователь 2 скачал Книгу 2

-- Вставка оценок
INSERT INTO ratings (user_id, book_id, rating, rated_at) VALUES
(1, 1, 5, DEFAULT),  -- Пользователь 1 оценил книгу 1 на 5
(2, 1, 4, DEFAULT),  -- Пользователь 2 оценил книгу 1 на 4
(1, 2, 3, DEFAULT);  -- Пользователь 1 оценил книгу 2 на 3


-- Вставка комментариев
INSERT INTO comments (user_id, book_id, comment, commented_at) VALUES
(1, 1, 'Отличная книга! Рекомендую всем.', DEFAULT),  -- Пользователь 1 оставил комментарий к книге 1
(2, 1, 'Хорошая, но немного затянутая.', DEFAULT),   -- Пользователь 2 оставил комментарий к книге 1
(1, 2, 'Не понравилась, слишком скучная.', DEFAULT);  -- Пользователь 1 оставил комментарий к книге 2
