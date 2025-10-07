CREATE DATABASE IF NOT EXISTS bank_a;
USE bank_a;

CREATE TABLE IF NOT EXISTS accounts (
  id BIGINT PRIMARY KEY,
  owner VARCHAR(100),
  balance DECIMAL(18,2) NOT NULL DEFAULT 0.00,
  currency CHAR(3) DEFAULT 'USD',
  version INT DEFAULT 1
) ENGINE=InnoDB;

INSERT INTO accounts (id, owner, balance, currency) VALUES
(1, 'Alice', 1000.00, 'USD'),
(2, 'Bob', 200.00, 'USD')
ON DUPLICATE KEY UPDATE id=id;
