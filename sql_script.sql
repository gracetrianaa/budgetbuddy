CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(10) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date DATETIME NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);

CREATE TABLE transactions_archive (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(10) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date DATETIME NOT NULL,
    balance DECIMAL(10, 2) NOT NULL 
);