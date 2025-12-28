-- Script SQL para criar o banco de dados e tabelas
-- Execute este arquivo no MySQL se preferir criar manualmente

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS meta_leitura;

-- Usar o banco de dados
USE meta_leitura;

-- Criar tabela de livros
CREATE TABLE IF NOT EXISTS books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    total_pages INT NOT NULL,
    current_page INT DEFAULT 0 NOT NULL,
    current_percentage FLOAT DEFAULT 0.0 NOT NULL,
    target_date DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_completed BOOLEAN DEFAULT FALSE,
    INDEX idx_created_at (created_at),
    INDEX idx_is_completed (is_completed)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserir alguns dados de exemplo (opcional)
INSERT INTO books (name, total_pages, current_page, target_date) VALUES
('O Hobbit', 310, 150, DATE_ADD(NOW(), INTERVAL 30 DAY)),
('1984', 328, 100, DATE_ADD(NOW(), INTERVAL 45 DAY)),
('Dom Casmurro', 256, 0, DATE_ADD(NOW(), INTERVAL 60 DAY));

-- Verificar dados
SELECT * FROM books;
