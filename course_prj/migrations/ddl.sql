-- Таблица для хранения информации о пользователях
create table users (
    user_id serial primary key,
    username varchar(50),
    email varchar(100),
    password_hash varchar(256),
    role varchar(10), -- admin or reader
    register_date timestamp
);

COMMENT ON TABLE users IS 'Информация о пользователях';

COMMENT ON COLUMN users.user_id IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN users.username IS 'Имя пользователя';

COMMENT ON COLUMN users.email IS 'Почта пользователя';

COMMENT ON COLUMN users.password_hash IS 'Хэш пароля пользователя';

COMMENT ON COLUMN users.role IS 'Роль пользователя на сайте(admin/reader)';

COMMENT ON COLUMN users.register_date IS 'Дата регистрации';

-- Таблица для хранения информации о книгах
create table books (
    book_id serial primary key,
    title varchar(256),
    published_year int,
    isbn varchar(256),
    description TEXT,
    added_at timestamp
);

COMMENT ON TABLE books IS 'Информация о книгах';

COMMENT ON COLUMN books.book_id IS 'Уникальный идентификатор книги';

COMMENT ON COLUMN books.title IS 'Название книги';

COMMENT ON COLUMN books.published_year IS 'Дата публикации';

COMMENT ON COLUMN books.isbn IS 'ISBN';

COMMENT ON COLUMN books.description IS 'Описание книги';

COMMENT ON COLUMN books.added_at IS 'Дата добавления книги на сайт';

-- Таблица для хранения информации об авторах
create table authors (
    author_id serial primary key,
    name varchar(100),
    bio TEXT
);   

COMMENT ON TABLE authors IS 'Информация об авторах';

COMMENT ON COLUMN authors.author_id IS 'Уникальный идентификатор автора';

COMMENT ON COLUMN authors.name IS 'Имя автора';

COMMENT ON COLUMN authors.bio IS 'Информация об авторе';

-- Таблица для связи книг и авторов
create table book_authors (
    author_id serial references authors(author_id) on delete cascade,
    book_id  serial references books(book_id) on delete cascade
);   

COMMENT ON TABLE book_authors IS 'Информация о связи книг и авторов';

COMMENT ON COLUMN book_authors.author_id IS 'Уникальный идентификатор автора';

COMMENT ON COLUMN book_authors.book_id IS 'Уникальный идентификатор книги';

-- Таблица для хранения различных жанров книг
create table categories (
    category_id serial primary key,
    category_name varchar(100)
);

COMMENT ON TABLE categories IS 'Жанры книг';

COMMENT ON COLUMN categories.category_id IS 'Уникальный идентификатор жанра';

COMMENT ON COLUMN categories.category_name IS 'Название жанра';


-- Таблица для хранения жанра книги
create table book_categories (
    book_id serial references books(book_id) on delete cascade,
    category_id serial references categories(category_id) on delete cascade
);

COMMENT ON TABLE book_categories IS 'Жанры конкретных книг';

COMMENT ON COLUMN book_categories.book_id IS 'Уникальный идентификатор книги';

COMMENT ON COLUMN book_categories.category_id IS 'Уникальный идентификатор жанра';

-- Таблица для хранения информации о загрузках
create table downloads (
    download_id serial primary key,
    user_id serial references users(user_id) on delete cascade,
    book_id serial references books(book_id) on delete cascade,
    download_date timestamp
);

COMMENT ON TABLE downloads IS 'Информация о загрузках';

COMMENT ON COLUMN downloads.download_id IS 'Уникальный идентификатор загрузки';

COMMENT ON COLUMN downloads.user_id IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN downloads.book_id IS 'Уникальный идентификатор книги';

COMMENT ON COLUMN downloads.download_date IS 'Дата скачивания';

-- Таблица для хранения информации об отзывах
create table reviews (
    review_id serial primary key,
    user_id serial references users(user_id) on delete cascade,
    book_id serial references books(book_id) on delete cascade,
    rating int,
    comment TEXT,
    reviewed_at timestamp
);

COMMENT ON TABLE reviews IS 'Информация об отзывах';

COMMENT ON COLUMN reviews.review_id IS 'Уникальный идентификатор отзыва';

COMMENT ON COLUMN reviews.user_id IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN reviews.book_id IS 'Уникальный идентификатор книги';

COMMENT ON COLUMN reviews.rating IS 'Оценка книги (1 - 5)';

COMMENT ON COLUMN reviews.comment IS 'Комментарий';

COMMENT ON COLUMN reviews.reviewed_at IS 'Дата отзыва';
