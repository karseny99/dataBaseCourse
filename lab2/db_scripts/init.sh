#!/bin/bash
set -e

# Wait for PostgreSQL
timeout=30
while ! pg_isready -h localhost -U ol_user -d openlibrary -t 1; do
  sleep 1
  ((timeout--))
  if [ $timeout -le 0 ]; then
    echo "PostgreSQL not ready, giving up"
    exit 1
  fi
done

# Apply settings
psql -v ON_ERROR_STOP=1 -h localhost -U ol_user -d openlibrary <<-EOSQL
  ALTER SYSTEM SET synchronous_commit TO OFF;
  ALTER SYSTEM SET maintenance_work_mem TO '512MB';
  ALTER SYSTEM SET checkpoint_timeout TO '60min';
  ALTER SYSTEM SET max_wal_size TO '4GB';
  SELECT pg_reload_conf();
EOSQL

# Execute scripts using the db_scripts/ path they expect
SCRIPTS=(
  db_scripts/db_openlibrary.sql
  db_scripts/tbl_fileinfo.sql
  db_scripts/tbl_authors.sql
  db_scripts/tbl_works.sql
  db_scripts/tbl_author_works.sql
  db_scripts/tbl_editions.sql
  db_scripts/tbl_edition_isbns.sql
  db_scripts/openlibrary-data-loader.sql
  db_scripts/load.sql
)

for script in "${SCRIPTS[@]}"; do
  echo "Executing $script..."
  psql -v ON_ERROR_STOP=1 -h localhost -U ol_user -d openlibrary -f "/$script"
done

# Finalize
psql -v ON_ERROR_STOP=1 -h localhost -U ol_user -d openlibrary <<-EOSQL
  VACUUM ANALYZE;
  ALTER SYSTEM SET synchronous_commit TO ON;
  SELECT pg_reload_conf();
  SELECT now() AS completion_time;
EOSQL

echo "Database initialization completed successfully!"