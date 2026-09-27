CREATE DATABASE IF NOT EXISTS expense_management;

USE expense_management;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'EMPLOYEE',
    active TINYINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS funding_claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    claim_id VARCHAR(30) UNIQUE NOT NULL,
    claim_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(12,2) DEFAULT 0,
    funding_status VARCHAR(30) DEFAULT 'Pending payment',
    submission_date DATETIME NULL,
    payment_date DATETIME NULL,
    payment_reference VARCHAR(150),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_id VARCHAR(30) UNIQUE NOT NULL,
    employee_id INT NOT NULL,
    employee_name VARCHAR(100) NOT NULL,
    project VARCHAR(150) NOT NULL,
    date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    receipt_url VARCHAR(500),
    approval_status VARCHAR(20) DEFAULT 'Pending',
    approval_note TEXT,
    employee_payment_status VARCHAR(20) DEFAULT 'Pending',
    employee_payment_date DATETIME NULL,
    employee_payment_reference VARCHAR(150),
    claim_id INT NULL,
    funding_status VARCHAR(30),
    funding_payment_date DATETIME NULL,
    funding_payment_reference VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (employee_id) REFERENCES users(id),
    FOREIGN KEY (claim_id) REFERENCES funding_claims(id)
);

INSERT IGNORE INTO users
(name, email, password, role, active)
VALUES
('Administrator', 'admin@themindcreater.com', 'admin2013', 'ADMIN', 1);

INSERT IGNORE INTO users
(name, email, password, role, active)
VALUES
('Demo Employee', 'employee@themindcreater.com', 'employee2013', 'EMPLOYEE', 1);