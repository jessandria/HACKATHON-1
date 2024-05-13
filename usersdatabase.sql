CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    surname TEXT,
    card_number TEXT UNIQUE,
    password TEXT
);

CREATE TABLE savings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    amount REAL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (name, surname, card_number, password) VALUES
('Anna', 'Arnauld', '123456', 'anna123'),
('Barry', 'Dupont', '234567', 'bar_pwd'),
('Cedric', 'Smith', '345678', 'cedcard'),
('Daniel', 'Johnson', '456789', 'incorrectpwd'),
('Emma', 'Brown', '567890', 'pwd123'),
('Francesca', 'Davis', '678901', 'FDcard'),
('George', 'Miller', '789012', 'passwordG');

INSERT INTO savings (user_id, amount) VALUES
(1, 1000),  
(2, 1500),  
(3, 2000),  
(4, 2500),  
(5, 3000),  
(6, 3500),  
(7, 4000);
