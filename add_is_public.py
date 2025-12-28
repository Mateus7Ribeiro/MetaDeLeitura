"""
Script para adicionar coluna is_public à tabela books
Execute com: python add_is_public.py
"""

from app import create_app, db
from sqlalchemy import text

def main():
    print("=" * 60)
    print("ADICIONANDO CAMPO 'is_public' À TABELA 'books'")
    print("=" * 60)
    print()
    
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar se coluna já existe
            result = db.session.execute(
                text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='books' AND COLUMN_NAME='is_public'")
            ).fetchone()
            
            if result:
                print("✓ Coluna is_public já existe")
            else:
                print("⚠ Adicionando coluna is_public...")
                db.session.execute(
                    text("ALTER TABLE books ADD COLUMN is_public BOOLEAN DEFAULT FALSE")
                )
                db.session.commit()
                print("✓ Coluna is_public adicionada com sucesso!")
            
            print("\n" + "=" * 60)
            print("✅ OPERAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    main()
