"""
Script de migração completa para v3.0
Adiciona todos os campos necessários para a nova versão
Execute com: python migrate_to_v3.py
"""

from app import create_app, db
from sqlalchemy import text
import secrets
import string

def generate_user_hash():
    """Gera hash curta única para usuário"""
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(12))

def main():
    print("=" * 70)
    print("MIGRACAO COMPLETA PARA v3.0")
    print("=" * 70)
    print()
    
    app = create_app(create_tables=False)
    
    with app.app_context():
        try:
            # ========================================
            # 1. VERIFICAR ESTRUTURA ATUAL
            # ========================================
            print("1. Verificando estrutura atual...")
            result = db.session.execute(text("DESCRIBE users")).fetchall()
            existing_columns = [row[0] for row in result]
            print("   Colunas existentes: %s" % ', '.join(existing_columns))
            print()
            
            # ========================================
            # 2. ADICIONAR COLUNA 'name'
            # ========================================
            if 'name' not in existing_columns:
                print("2. Adicionando coluna 'name'...")
                db.session.execute(
                    text("ALTER TABLE users ADD COLUMN name VARCHAR(120) AFTER username")
                )
                db.session.commit()
                print("   OK - Coluna 'name' adicionada!")
                
                print("   Populando 'name' com valores de 'username'...")
                db.session.execute(
                    text("UPDATE users SET name = username WHERE name IS NULL")
                )
                db.session.commit()
                print("   OK - Valores iniciais preenchidos!")
            else:
                print("2. Coluna 'name' ja existe - OK")
                
                # Verificar se ha valores NULL e preencher
                result = db.session.execute(
                    text("SELECT COUNT(*) FROM users WHERE name IS NULL")
                ).fetchone()
                if result[0] > 0:
                    print("   Preenchendo %d registros sem nome..." % result[0])
                    db.session.execute(
                        text("UPDATE users SET name = username WHERE name IS NULL")
                    )
                    db.session.commit()
                    print("   OK - Registros atualizados!")
            print()
            
            # ========================================
            # 3. ADICIONAR COLUNA 'profile_picture'
            # ========================================
            if 'profile_picture' not in existing_columns:
                print("3. Adicionando coluna 'profile_picture'...")
                db.session.execute(
                    text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500) AFTER password_hash")
                )
                db.session.commit()
                print("   OK - Coluna 'profile_picture' adicionada!")
            else:
                print("3. Coluna 'profile_picture' ja existe - OK")
            print()
            
            # ========================================
            # 4. ADICIONAR COLUNA 'user_hash'
            # ========================================
            if 'user_hash' not in existing_columns:
                print("4. Adicionando coluna 'user_hash'...")
                db.session.execute(
                    text("ALTER TABLE users ADD COLUMN user_hash VARCHAR(12) UNIQUE AFTER reading_speed")
                )
                db.session.commit()
                print("   OK - Coluna 'user_hash' adicionada!")
                
                # Gerar hashes para usuarios existentes
                print("   Gerando hashes unicos para usuarios existentes...")
                users = db.session.execute(
                    text("SELECT id FROM users WHERE user_hash IS NULL")
                ).fetchall()
                
                for user in users:
                    user_id = user[0]
                    # Gerar hash unico
                    while True:
                        new_hash = generate_user_hash()
                        # Verificar se ja existe
                        exists = db.session.execute(
                            text("SELECT COUNT(*) FROM users WHERE user_hash = :hash"),
                            {"hash": new_hash}
                        ).fetchone()[0]
                        
                        if exists == 0:
                            break
                    
                    # Atualizar usuario
                    db.session.execute(
                        text("UPDATE users SET user_hash = :hash WHERE id = :id"),
                        {"hash": new_hash, "id": user_id}
                    )
                
                db.session.commit()
                print("   OK - %d hashes gerados!" % len(users))
            else:
                print("4. Coluna 'user_hash' ja existe - OK")
                
                # Verificar se ha usuarios sem hash
                result = db.session.execute(
                    text("SELECT COUNT(*) FROM users WHERE user_hash IS NULL")
                ).fetchone()
                
                if result[0] > 0:
                    print("   Gerando hashes para %d usuarios..." % result[0])
                    users = db.session.execute(
                        text("SELECT id FROM users WHERE user_hash IS NULL")
                    ).fetchall()
                    
                    for user in users:
                        user_id = user[0]
                        while True:
                            new_hash = generate_user_hash()
                            exists = db.session.execute(
                                text("SELECT COUNT(*) FROM users WHERE user_hash = :hash"),
                                {"hash": new_hash}
                            ).fetchone()[0]
                            if exists == 0:
                                break
                        
                        db.session.execute(
                            text("UPDATE users SET user_hash = :hash WHERE id = :id"),
                            {"hash": new_hash, "id": user_id}
                        )
                    
                    db.session.commit()
                    print("   OK - Hashes gerados!")
            print()
            
            # ========================================
            # 5. ADICIONAR COLUNAS NA TABELA books
            # ========================================
            print("5. Verificando colunas da tabela 'books'...")
            result = db.session.execute(text("DESCRIBE books")).fetchall()
            books_columns = [row[0] for row in result]
            print("   Colunas existentes: %s" % ', '.join(books_columns))
            
            if 'cover_url' not in books_columns:
                print("   Adicionando coluna 'cover_url'...")
                db.session.execute(
                    text("ALTER TABLE books ADD COLUMN cover_url VARCHAR(500) AFTER target_date")
                )
                db.session.commit()
                print("   OK - Coluna 'cover_url' adicionada!")
            else:
                print("   Coluna 'cover_url' ja existe - OK")
            
            if 'is_public' not in books_columns:
                print("   Adicionando coluna 'is_public'...")
                db.session.execute(
                    text("ALTER TABLE books ADD COLUMN is_public TINYINT(1) DEFAULT 0 AFTER is_completed")
                )
                db.session.commit()
                print("   OK - Coluna 'is_public' adicionada!")
            else:
                print("   Coluna 'is_public' ja existe - OK")
            print()
            
            # ========================================
            # 6. CRIAR TABELA user_followers
            # ========================================
            print("6. Verificando tabela 'user_followers'...")
            tables = db.session.execute(text("SHOW TABLES")).fetchall()
            table_names = [t[0] for t in tables]
            
            if 'user_followers' not in table_names:
                print("   Criando tabela 'user_followers'...")
                db.session.execute(text("""
                    CREATE TABLE user_followers (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        follower_id INT NOT NULL,
                        following_id INT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE KEY unique_follow (follower_id, following_id),
                        FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """))
                db.session.commit()
                print("   OK - Tabela 'user_followers' criada!")
            else:
                print("   Tabela 'user_followers' ja existe - OK")
            print()
            
            # ========================================
            # 7. VERIFICACAO FINAL
            # ========================================
            print("7. Verificacao final...")
            result = db.session.execute(text("DESCRIBE users")).fetchall()
            print()
            print("   Estrutura final da tabela 'users':")
            for row in result:
                print("   - %s: %s" % (row[0], row[1]))
            
            # Contar registros
            user_count = db.session.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0]
            book_count = db.session.execute(text("SELECT COUNT(*) FROM books")).fetchone()[0]
            print()
            print("   Total de usuarios: %d" % user_count)
            print("   Total de livros: %d" % book_count)
            
            # Verificar dados
            print()
            print("   Verificando integridade dos dados:")
            
            print()
            print("   Tabela USERS:")
            user_checks = [
                ("name IS NOT NULL", "Todos tem nome"),
                ("user_hash IS NOT NULL", "Todos tem hash"),
                ("LENGTH(user_hash) = 12", "Hashes com tamanho correto")
            ]
            
            for condition, description in user_checks:
                count = db.session.execute(
                    text("SELECT COUNT(*) FROM users WHERE %s" % condition)
                ).fetchone()[0]
                status = "OK" if count == user_count else "AVISO"
                print("   [%s] %s: %d/%d" % (status, description, count, user_count))
            
            print()
            print("   Tabela BOOKS:")
            result = db.session.execute(text("DESCRIBE books")).fetchall()
            books_final_columns = [row[0] for row in result]
            
            book_checks = [
                ("cover_url" in books_final_columns, "Coluna cover_url existe"),
                ("is_public" in books_final_columns, "Coluna is_public existe")
            ]
            
            for condition, description in book_checks:
                status = "OK" if condition else "AVISO"
                print("   [%s] %s" % (status, description))
            
            print()
            print("=" * 70)
            print("MIGRACAO CONCLUIDA COM SUCESSO!")
            print("=" * 70)
            print()
            print("Alteracoes realizadas:")
            print()
            print("  TABELA users:")
            print("    - name (nome completo editavel)")
            print("    - profile_picture (foto do perfil)")
            print("    - user_hash (identificador unico para URLs)")
            print()
            print("  TABELA books:")
            print("    - cover_url (URL da capa do livro)")
            print("    - is_public (livro visivel publicamente)")
            print()
            print("  NOVA TABELA:")
            print("    - user_followers (sistema de seguir usuarios)")
            print()
            print("Proximos passos:")
            print("  1. Recarregar a aplicacao web (Web tab > Reload)")
            print("  2. Testar o login")
            print("  3. Verificar perfis de usuario")
            print("  4. Testar upload de foto")
            print()
            
        except Exception as e:
            print()
            print("=" * 70)
            print("ERRO DURANTE A MIGRACAO")
            print("=" * 70)
            print("Erro: %s" % str(e))
            print()
            print("O que fazer:")
            print("  1. Verifique se o banco de dados esta acessivel")
            print("  2. Verifique se o arquivo .env esta configurado corretamente")
            print("  3. Execute: mysql -u USER -h HOST -p DATABASE")
            print("  4. Verifique os logs de erro")
            print()
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()
