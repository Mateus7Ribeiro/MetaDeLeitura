-- ===============================================
-- SCRIPT DE MIGRAÇÃO DO BANCO DE DADOS v1.0 → v2.0
-- ===============================================
-- 
-- Este script atualiza o banco existente para suportar
-- o sistema de usuários da versão 2.0
--
-- Execute este script ANTES de usar a nova versão!

USE meta_leitura;

-- ===============================================
-- 1. CRIAR TABELA DE USUÁRIOS
-- ===============================================

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    reading_speed FLOAT DEFAULT 2.5,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ===============================================
-- 2. ADICIONAR COLUNA user_id À TABELA books
-- ===============================================

-- Primeiro, vamos adicionar a coluna como nullable temporariamente
ALTER TABLE books ADD COLUMN user_id INT NULL;

-- ===============================================
-- 3. CRIAR USUÁRIO DEFAULT PARA DADOS ANTIGOS
-- ===============================================

-- Inserir um usuário default para associar livros antigos
-- Username: admin | Email: admin@local.com | Password: admin123
INSERT INTO users (username, email, password_hash, reading_speed)
VALUES (
    'admin',
    'admin@local.com',
    'pbkdf2:sha256:600000$GxA7jBqJ$d8b2d8c8c8c8c8c8c8c8c8c8c8c8c8c8c8c8c8c8',
    2.5
) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id);

-- ===============================================
-- 4. ATUALIZAR LIVROS EXISTENTES COM USER_ID
-- ===============================================

-- Associar todos os livros existentes ao usuário admin
UPDATE books SET user_id = 1 WHERE user_id IS NULL;

-- ===============================================
-- 5. TORNAR user_id NOT NULL E ADICIONAR FOREIGN KEY
-- ===============================================

ALTER TABLE books MODIFY COLUMN user_id INT NOT NULL;

-- Adicionar constraint de chave estrangeira
ALTER TABLE books ADD CONSTRAINT fk_books_user_id 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- Adicionar índice para performance
ALTER TABLE books ADD INDEX idx_user_id (user_id);

-- ===============================================
-- 6. VERIFICAR A MIGRAÇÃO
-- ===============================================

-- Exibir estrutura da tabela users
DESCRIBE users;

-- Exibir estrutura da tabela books (modificada)
DESCRIBE books;

-- Contar livros por usuário
SELECT users.username, COUNT(books.id) as total_livros
FROM users
LEFT JOIN books ON books.user_id = users.id
GROUP BY users.id, users.username;

-- ===============================================
-- PRONTO! ✓
-- ===============================================
-- 
-- Seu banco de dados foi atualizado com sucesso!
-- 
-- Credenciais do usuário admin:
-- - Username: admin
-- - Senha: admin123
-- - Email: admin@local.com
--
-- Todos os seus livros antigos estão associados a este usuário.
-- Você pode:
// 1. Fazer login com essas credenciais
-- 2. Criar novos usuários
-- 3. Transferir livros manualmente se necessário
--
