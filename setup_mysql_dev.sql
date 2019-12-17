-- prepares a MySQL server
-- Root user, creating a new database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- new user in localhost, password predetermined
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- all privileges to new user in the new database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- select privilege on the database performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
-- flush
FLUSH PRIVILEGES;
