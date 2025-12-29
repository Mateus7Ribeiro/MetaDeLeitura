#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    # Adicionar coluna user_hash se não existir
    try:
        db.session.execute(text('''
            ALTER TABLE users 
            ADD COLUMN user_hash VARCHAR(12) UNIQUE
        '''))
        db.session.commit()
        print('✅ Coluna user_hash criada')
    except Exception as e:
        if '1060' in str(e):  # Coluna já existe
            print('ℹ️ Coluna user_hash já existe')
        else:
            print(f'❌ Erro: {e}')
    
    # Criar tabela user_followers se não existir
    try:
        db.session.execute(text('''
            CREATE TABLE IF NOT EXISTS user_followers (
                id INT PRIMARY KEY AUTO_INCREMENT,
                follower_id INT NOT NULL,
                following_id INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_follow (follower_id, following_id),
                CONSTRAINT cannot_follow_self CHECK (follower_id != following_id),
                FOREIGN KEY (follower_id) REFERENCES users(id),
                FOREIGN KEY (following_id) REFERENCES users(id)
            )
        '''))
        db.session.commit()
        print('✅ Tabela user_followers criada')
    except Exception as e:
        if '1050' in str(e):  # Tabela já existe
            print('ℹ️ Tabela user_followers já existe')
        else:
            print(f'❌ Erro: {e}')
