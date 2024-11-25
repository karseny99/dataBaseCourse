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

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticator') THEN
        CREATE USER authenticator WITH PASSWORD '1';
        GRANT authenticator TO user1;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'reader') THEN
        CREATE USER reader WITH PASSWORD '1';
        GRANT reader TO reader; 
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'admin') THEN
        CREATE USER admin WITH PASSWORD '1';
        GRANT admin TO admin;
    END IF;

    -- Auth permissions
    GRANT SELECT, INSERT ON users TO authenticator;

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

    GRANT USAGE, SELECT ON SEQUENCE comments_comment_id_seq TO reader;
    GRANT USAGE, SELECT ON SEQUENCE downloads_download_id_seq TO reader;
    GRANT USAGE, SELECT ON SEQUENCE ratings_rating_id_seq TO reader;
    GRANT USAGE, SELECT ON SEQUENCE admin_requests_request_id_seq TO reader;

    -- Admin's permissions
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;  
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;  
    GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO admin;  

END $$;
