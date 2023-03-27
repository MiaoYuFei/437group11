DROP USER IF EXISTS 'stocknews'@'localhost';

CREATE USER 'stocknews'@'localhost' IDENTIFIED BY 'Cse@437s';

DROP DATABASE IF EXISTS stocknews;

CREATE DATABASE stocknews;

GRANT ALL PRIVILEGES ON stocknews.* TO 'stocknews'@'localhost';

FLUSH PRIVILEGES;
