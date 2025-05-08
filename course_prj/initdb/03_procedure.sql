CREATE OR REPLACE FUNCTION cleanup_old_admin_requests() 
RETURNS TRIGGER as $$
BEGIN
    DELETE FROM admin_requests WHERE request_date < NOW() - INTERVAL '7 days';
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;

CREATE TRIGGER delete_old_requests_on_insert
AFTER INSERT ON admin_requests
FOR EACH ROW
EXECUTE FUNCTION cleanup_old_admin_requests() ;

CREATE OR REPLACE FUNCTION get_paginated_books(
    page_number INT,
    page_size INT,
    author_name_filter VARCHAR DEFAULT NULL,
    published_year_filter INT DEFAULT NULL,
    category_name_filter VARCHAR DEFAULT NULL
)
RETURNS TABLE(
    book_id INT,
    title VARCHAR,
    published_year INT,
    isbn VARCHAR,
    description TEXT,
    authors TEXT[], 
    categories TEXT[],  
    file_path VARCHAR,
    cover_image_path VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        b.book_id,
        b.title,
        b.published_year,
        b.isbn,
        b.description,
        array_agg(DISTINCT b.author_name::text) AS authors,  
        array_agg(DISTINCT b.category_name::text) AS categories,  
        b.file_path,
        b.cover_image_path
    FROM 
        books_full_info b
    WHERE 
        (author_name_filter IS NULL OR b.author_name ILIKE '%' || author_name_filter || '%')
        AND (published_year_filter IS NULL OR b.published_year = published_year_filter)
        AND (category_name_filter IS NULL OR b.category_name ILIKE '%' || category_name_filter || '%')
    GROUP BY 
        b.book_id, b.title, b.published_year, b.isbn, b.description, b.file_path, b.cover_image_path
    ORDER BY 
        b.book_id
    LIMIT 
        page_size OFFSET (page_number - 1) * page_size;
END;
$$ LANGUAGE plpgsql;
