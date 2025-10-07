CREATE DATABASE IF NOT EXISTS bank_b;
USE bank_b;

CREATE TABLE IF NOT EXISTS accounts (
  id BIGINT PRIMARY KEY,
  owner VARCHAR(100),
  balance DECIMAL(18,2) NOT NULL DEFAULT 0.00,
  currency CHAR(3) DEFAULT 'USD',
  version INT DEFAULT 1
) ENGINE=InnoDB;

INSERT INTO accounts (id, owner, balance, currency) VALUES
(10, 'Carol', 500.00, 'USD'),
(11, 'Dave', 150.00, 'USD')
ON DUPLICATE KEY UPDATE id=id;
