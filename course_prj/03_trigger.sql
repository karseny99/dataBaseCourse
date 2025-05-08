CREATE OR REPLACE FUNCTION cleanup_old_admin_requests() 
RETURNS TRIGGER as $$
BEGIN
    DELETE FROM admin_requests WHERE request_date < NOW() - INTERVAL '7 days';
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER delete_old_requests_on_insert
AFTER INSERT ON admin_requests
FOR EACH ROW
EXECUTE FUNCTION cleanup_old_admin_requests();