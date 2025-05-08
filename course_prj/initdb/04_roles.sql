DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticator') THEN
        CREATE ROLE authenticator LOGIN PASSWORD '1';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'reader') THEN
        CREATE ROLE reader LOGIN PASSWORD '1';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'admin') THEN
        CREATE ROLE admin LOGIN PASSWORD '1';
    END IF;

    GRANT USAGE, SELECT ON SEQUENCE users_user_id_seq TO authenticator;

    GRANT INSERT, SELECT ON users TO authenticator;
    GRANT SELECT ON user_roles TO authenticator;

    -- Reader's permissions
    GRANT SELECT ON books TO reader;
    GRANT SELECT ON users TO reader;
    GRANT SELECT ON authors TO reader;
    GRANT SELECT ON book_authors TO reader;
    GRANT SELECT ON categories TO reader;
    GRANT SELECT ON book_categories TO reader;

    GRANT SELECT, INSERT ON admin_requests TO reader;
    GRANT SELECT, INSERT, UPDATE ON comments TO reader;
    GRANT SELECT, INSERT, UPDATE ON downloads TO reader;
    GRANT SELECT, INSERT, UPDATE ON ratings TO reader;

    GRANT SELECT ON comments_view TO reader;
    GRANT SELECT ON downloads_view TO reader;
    GRANT SELECT ON ratings_view TO reader;
    GRANT SELECT ON books_with_authors TO reader;
    GRANT SELECT ON books_with_categories TO reader;
    GRANT SELECT ON user_roles TO reader;
    GRANT SELECT ON books_full_info TO reader;
    GRANT EXECUTE ON FUNCTION get_paginated_books(INT, INT, VARCHAR, INT, VARCHAR) TO reader;


    GRANT USAGE, SELECT ON SEQUENCE comments_comment_id_seq TO reader;
    GRANT USAGE, SELECT ON SEQUENCE downloads_download_id_seq TO reader;
    GRANT USAGE, SELECT ON SEQUENCE ratings_rating_id_seq TO reader;
    GRANT USAGE, SELECT ON SEQUENCE admin_requests_request_id_seq TO reader;

    -- Admin's permissions
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;  
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;  
    GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO admin;  
    GRANT USAGE ON SCHEMA public TO admin;

END $$;
