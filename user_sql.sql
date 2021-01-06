USE battles;

DROP TABLE IF EXISTS users;


CREATE TABLE users(
   username           VARCHAR(100) NOT NULL PRIMARY KEY
  ,password           VARCHAR(20)  NOT NULL
  );
  
INSERT INTO users(username,password) VALUES ('admin','admin');

SELECT * FROM users;