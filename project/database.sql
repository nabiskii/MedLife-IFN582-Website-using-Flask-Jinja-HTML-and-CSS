CREATE DATABASE medlife;

USE medlife;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user'
);

INSERT INTO users (username, password, role) VALUES ('owner', 'scrypt:32768:8:1$eJ4xPDgOsfFx7RmU$4ae65df32371b5dc37945e2068961f65287b495dc7714cc2efc9876df7787b57e3c2647ef3febbe82feeb1cbf7d248b93d54a1a2820aaf4fe3dc64a445664200', 'admin')
