"""
Script de Migração de Banco de Dados v1.0 → v2.0
Execute com: python migrate_db.py

Este script automatiza a migração do banco de dados existente
para adicionar suporte a usuários e reading_speed.
"""

import sys
import os
from app import create_app, db
from app.models import User, Book
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy import text

def main():
    print("=" * 60)
    print("MIGRAÇÃO DE BANCO DE DADOS v1.0 → v2.0")
    print("=" * 60)
    print()
    
    # Criar app context
    app = create_app()
    
    with app.app_context():
        try:
            # Passo 1: Criar tabela users (SQLAlchemy)
            print("1️⃣  Criando tabelas...")
            db.create_all()
            print("   ✓ Tabelas criadas/verificadas")
            
            # Passo 2: Verificar e adicionar coluna user_id se necessária
            print("\n2️⃣  Verificando coluna user_id na tabela books...")
            
            # Checar se coluna user_id já existe
            result = db.session.execute(
                text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='books' AND COLUMN_NAME='user_id'")
            ).fetchone()
            
            if not result:
                print("   ⚠ Coluna user_id não encontrada, adicionando...")
                
                # Adicionar coluna user_id (começando como NULL)
                db.session.execute(
                    text("ALTER TABLE books ADD COLUMN user_id INT NULL")
                )
                db.session.commit()
                print("   ✓ Coluna user_id adicionada")
            else:
                print("   ✓ Coluna user_id já existe")
            
            # Passo 3: Verificar/criar usuário admin
            print("\n3️⃣  Verificando usuário admin...")
            admin_user = User.query.filter_by(username='admin').first()
            
            if not admin_user:
                print("   ⚠ Usuário admin não encontrado, criando...")
                admin_user = User(
                    username='admin',
                    email='admin@local.com',
                    reading_speed=2.5
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("   ✓ Usuário admin criado")
                print("   📝 Credenciais:")
                print("      - Username: admin")
                print("      - Senha: admin123")
                print("      - Email: admin@local.com")
            else:
                print("   ✓ Usuário admin já existe")
            
            # Passo 4: Associar livros existentes ao admin
            print("\n4️⃣  Verificando livros sem proprietário...")
            books_without_user = Book.query.filter_by(user_id=None).all()
            
            if books_without_user:
                print(f"   ⚠ {len(books_without_user)} livro(s) sem proprietário encontrado(s)")
                print("   Associando ao usuário admin...")
                
                for book in books_without_user:
                    book.user_id = admin_user.id
                
                db.session.commit()
                print(f"   ✓ {len(books_without_user)} livro(s) associado(s)")
            else:
                print("   ✓ Todos os livros têm proprietário")
            
            # Estatísticas finais
            print("\n5️⃣  Estatísticas finais:")
            total_users = User.query.count()
            total_books = Book.query.count()
            books_by_user = db.session.query(User.username, db.func.count(Book.id)).outerjoin(Book).group_by(User.id).all()
            
            print(f"   📊 Total de usuários: {total_users}")
            print(f"   📚 Total de livros: {total_books}")
            print("   📋 Livros por usuário:")
            for username, count in books_by_user:
                print(f"      - {username}: {count} livro(s)")
            
            print("\n" + "=" * 60)
            print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print()
            print("Próximos passos:")
            print("1. Execute: python run.py")
            print("2. Acesse: http://localhost:5000")
            print("3. Faça login com admin/admin123")
            print("4. Vá em Configurações e altere a velocidade de leitura")
            print("5. Seus livros antigos continuam lá! 📚")
            print()
            
            return 0
            
        except Exception as e:
            print(f"\n❌ ERRO DURANTE A MIGRAÇÃO:")
            print(f"   {type(e).__name__}: {e}")
            print()
            print("Solução:")
            print("1. Verifique se MySQL está rodando")
            print("2. Verifique o arquivo .env com credenciais corretas")
            print("3. Se o erro persiste, execute o script SQL manualmente:")
            print("   mysql -u root -p meta_leitura < migrate_v1_to_v2.sql")
            return 1

if __name__ == '__main__':
    sys.exit(main())
