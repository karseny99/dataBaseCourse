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
-- Таблица для хранения информации об авторах
create table authors (
    author_id serial primary key,
    name varchar(100),
    bio TEXT
);   
CREATE INDEX idx_authors_name ON authors(name);
-- Таблица для связи книг и авторов
create table book_authors (
    author_id serial references authors(author_id) on delete cascade,
    book_id  serial references books(book_id) on delete cascade
);   
CREATE INDEX idx_book_authors_author_book ON book_authors(author_id, book_id);
-- Таблица для хранения различных жанров книг
create table categories (
    category_id serial primary key,
    category_name varchar(100)
);
-- Таблица для хранения жанра книги
create table book_categories (
    book_id serial references books(book_id) on delete cascade,
    category_id serial references categories(category_id) on delete cascade
);
CREATE INDEX idx_book_categories_book_category ON book_categories(book_id, category_id);
-- Таблица для хранения информации о загрузках
create table downloads (
    download_id serial primary key,
    user_id serial references users(user_id) on delete cascade,
    book_id serial references books(book_id) on delete cascade,
    download_date timestamp
);
CREATE INDEX idx_downloads_user_id ON downloads(user_id);
CREATE INDEX idx_downloads_book_id ON downloads(book_id);
create table ratings (
    rating_id serial primary key,
    user_id serial references users(user_id) on delete cascade,
    book_id serial references books(book_id) on delete cascade,
    rating int not null,
    rated_at timestamp default current_timestamp
);
CREATE INDEX idx_ratings_user_id ON ratings(user_id);
CREATE INDEX idx_ratings_book_id ON ratings(book_id);
create table comments (
    comment_id serial primary key,
    user_id serial references users(user_id) on delete cascade,
    book_id serial references books(book_id) on delete cascade,
    comment TEXT not null,
    commented_at timestamp default current_timestamp
);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_book_id ON comments(book_id);
create table admin_requests (
    request_id serial primary key,
    user_id serial references users(user_id) on delete cascade,
    request_date timestamp default current_timestamp
);
CREATE INDEX idx_admin_requests_user_id ON admin_requests(user_id);
