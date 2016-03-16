CREATE DATABASE mails;
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL
);

CREATE TYPE mail_status AS ENUM ('draft', 'sent');

CREATE TABLE mails(
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES users(id),
    recipient_id INT REFERENCES users(id),
    title VARCHAR(1024),
    text TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status mail_status NOT NULL,
    viewed BOOLEAN DEFAULT FALSE
);