
-- create the users for each database
GRANT CREATE, ALTER, INDEX, LOCK TABLES, REFERENCES, UPDATE, DELETE, DROP, SELECT, INSERT ON `teepon_database`.* TO 'root'@'mysql';

FLUSH PRIVILEGES;

USE teepon_mysql;

INSERT INTO user (username, email) VALUES ('testuser1', 'test1@example.com');
INSERT INTO user (username, email) VALUES ('testuser2', 'test2@example.com');