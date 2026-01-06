"""
Script para adicionar os campos 'name' e 'profile_picture' à tabela users
Execute com: python migrate_add_user_fields.py
"""

from app import create_app, db
from sqlalchemy import text

def main():
    print("=" * 70)
    print("ADICIONANDO NOVOS CAMPOS À TABELA USERS")
    print("=" * 70)
    print()
    
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar se as colunas já existem
            print("1️⃣  Verificando colunas existentes...")
            result = db.session.execute(
                text("DESCRIBE users")
            ).fetchall()
            
            existing_columns = [row[0] for row in result]
            print(f"   Colunas existentes: {', '.join(existing_columns)}")
            
            # Adicionar coluna 'name' se não existir
            if 'name' not in existing_columns:
                print("\n2️⃣  Adicionando coluna 'name'...")
                db.session.execute(
                    text("ALTER TABLE users ADD COLUMN name VARCHAR(120) AFTER username")
                )
                db.session.commit()
                print("   ✓ Coluna 'name' adicionada!")
                
                # Preencher com username como valor inicial
                print("   Populando 'name' com valores de 'username'...")
                db.session.execute(
                    text("UPDATE users SET name = username WHERE name IS NULL")
                )
                db.session.commit()
                print("   ✓ Valores iniciais preenchidos!")
            else:
                print("\n2️⃣  Coluna 'name' já existe ✓")
            
            # Adicionar coluna 'profile_picture' se não existir
            if 'profile_picture' not in existing_columns:
                print("\n3️⃣  Adicionando coluna 'profile_picture'...")
                db.session.execute(
                    text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500) AFTER password_hash")
                )
                db.session.commit()
                print("   ✓ Coluna 'profile_picture' adicionada!")
            else:
                print("\n3️⃣  Coluna 'profile_picture' já existe ✓")
            
            # Verificar estrutura final
            print("\n4️⃣  Verificando estrutura final...")
            result = db.session.execute(
                text("DESCRIBE users")
            ).fetchall()
            
            print("\n   Estrutura da tabela users:")
            for row in result:
                print(f"   - {row[0]}: {row[1]}")
            
            print("\n" + "=" * 70)
            print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            print()
            print("Novos recursos disponíveis:")
            print("1. Campo 'name' - Nome completo editável do usuário")
            print("2. Campo 'profile_picture' - URL/caminho da foto de perfil")
            print()
            print("Próximos passos:")
            print("1. Execute: python run.py")
            print("2. Acesse as configurações para editar seu perfil")
            
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    main()
