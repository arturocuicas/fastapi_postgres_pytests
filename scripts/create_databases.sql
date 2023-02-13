-- You can substitute Users and Databases of your choice.
CREATE DATABASE transactions_db;
CREATE DATABASE test_transactions_db;

GRANT ALL PRIVILEGES ON DATABASE transactions_db to "postgres";
GRANT ALL PRIVILEGES ON DATABASE test_transactions_db to "postgres";
