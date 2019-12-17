-- prepares a MySQL server
-- Root user, creating a new database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- new user in localhost, password predetermined
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- all privileges to new user in the new database
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- select privilege on the database performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
-- flush
FLUSH PRIVILEGES;
