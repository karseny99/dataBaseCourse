-- Таблица для хранения информации о пользователях
create table users (
    user_id serial primary key,
    username varchar(50) unique,
    email varchar(100) unique,
    password_hash varchar(256),
    role varchar(10), -- admin or reader
    register_date timestamp
);

CREATE INDEX idx_users_username ON users(username);

CREATE INDEX idx_users_email ON users(email);

COMMENT ON TABLE users IS 'Инaформация о пользователях';

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
    isbn varchar(256) unique,
    description TEXT,
    added_at timestamp,
    file_path VARCHAR(512),  
    cover_image_path VARCHAR(512) 
);

CREATE INDEX idx_books_title ON books(title);

CREATE INDEX idx_books_isbn ON books(isbn);

CREATE INDEX idx_books_published_year ON books(published_year);


COMMENT ON TABLE books IS 'Информация о книгах';

COMMENT ON COLUMN books.book_id IS 'Уникальный идентификатор книги';

COMMENT ON COLUMN books.title IS 'Название книги';

COMMENT ON COLUMN books.published_year IS 'Дата публикации';

COMMENT ON COLUMN books.isbn IS 'ISBN';

COMMENT ON COLUMN books.description IS 'Описание книги';

COMMENT ON COLUMN books.added_at IS 'Дата добавления книги на сайт';

COMMENT ON COLUMN books.file_path IS 'Путь к файлу кинги в хранилище';

COMMENT ON COLUMN books.cover_image_path IS 'Путь к обложке книги в хранилище';

-- Таблица для хранения информации об авторах
create table authors (
    author_id serial primary key,
    name varchar(100),
    bio TEXT
);   

CREATE INDEX idx_authors_name ON authors(name);


COMMENT ON TABLE authors IS 'Информация об авторах';

COMMENT ON COLUMN authors.author_id IS 'Уникальный идентификатор автора';

COMMENT ON COLUMN authors.name IS 'Имя автора';

COMMENT ON COLUMN authors.bio IS 'Информация об авторе';

-- Таблица для связи книг и авторов
create table book_authors (
    author_id serial references authors(author_id) on delete cascade,
    book_id serial references books(book_id) on delete cascade,
    primary key (author_id, book_id)
);

CREATE INDEX idx_book_authors_author_book ON book_authors(author_id, book_id);

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
    category_id serial references categories(category_id) on delete cascade,
    primary key (book_id, category_id)
);

CREATE INDEX idx_book_categories_book_category ON book_categories(book_id, category_id);


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

CREATE INDEX idx_downloads_user_id ON downloads(user_id);

CREATE INDEX idx_downloads_book_id ON downloads(book_id);


COMMENT ON TABLE downloads IS 'Информация о загрузках';

COMMENT ON COLUMN downloads.download_id IS 'Уникальный идентификатор загрузки';

COMMENT ON COLUMN downloads.user_id IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN downloads.book_id IS 'Уникальный идентификатор книги';

COMMENT ON COLUMN downloads.download_date IS 'Дата скачивания';

create table ratings (
    rating_id serial primary key,
    user_id serial references users(user_id) on delete cascade,
    book_id serial references books(book_id) on delete cascade,
    rating int not null,
    rated_at timestamp default current_timestamp
);

CREATE INDEX idx_ratings_user_id ON ratings(user_id);

CREATE INDEX idx_ratings_book_id ON ratings(book_id);


COMMENT ON TABLE ratings IS 'Информация об оценках';

COMMENT ON COLUMN ratings.rating_id IS 'Уникальный идентификатор оценки';

COMMENT ON COLUMN ratings.user_id IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN ratings.book_id IS 'Уникальный идентификатор книги';

COMMENT ON COLUMN ratings.rating IS 'Балл';

COMMENT ON COLUMN ratings.rated_at IS 'Дата оценки';

create table comments (
    comment_id serial primary key,
    user_id serial references users(user_id) on delete cascade,
    book_id serial references books(book_id) on delete cascade,
    comment TEXT not null,
    commented_at timestamp default current_timestamp
);

CREATE INDEX idx_comments_user_id ON comments(user_id);

CREATE INDEX idx_comments_book_id ON comments(book_id);


COMMENT ON TABLE comments IS 'Информация о комментариях';

COMMENT ON COLUMN comments.comment_id IS 'Уникальный идентификатор комментария';

COMMENT ON COLUMN comments.user_id IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN comments.book_id IS 'Уникальный идентификатор книги';

COMMENT ON COLUMN comments.comment IS 'Текст комментария';

COMMENT ON COLUMN comments.commented_at IS 'Дата комментария';


create table admin_requests (
    request_id serial primary key,
    user_id serial references users(user_id) on delete cascade,
    request_date timestamp default current_timestamp
);

CREATE INDEX idx_admin_requests_user_id ON admin_requests(user_id);

COMMENT ON COLUMN admin_requests.request_id IS 'Уникальный идентификатор запроса';

COMMENT ON COLUMN admin_requests.user_id IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN admin_requests.request_date IS 'Дата запроса';
