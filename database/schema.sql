CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    available INT DEFAULT 1
);

CREATE TABLE issued_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    user_name VARCHAR(100),
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);