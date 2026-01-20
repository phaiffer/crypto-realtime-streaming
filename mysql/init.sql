CREATE DATABASE IF NOT EXISTS crypto_project;

USE crypto_project;

CREATE TABLE IF NOT EXISTS moving_averages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_time DATETIME,
    end_time DATETIME,
    symbol VARCHAR(10),
    average_price DECIMAL(20, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);