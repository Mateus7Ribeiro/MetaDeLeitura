"""
Script para adicionar coluna cover_url aos livros individuais
Execute com: python add_cover_url.py
"""

from app import create_app, db
from sqlalchemy import text

def main():
    print("=" * 70)
    print("ADICIONANDO CAMPO cover_url AOS LIVROS")
    print("=" * 70)
    print()
    
    app = create_app()
    
    with app.app_context():
        try:
            print("1️⃣  Verificando coluna cover_url na tabela books...")
            
            # Checar se coluna já existe
            result = db.session.execute(
                text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='books' AND COLUMN_NAME='cover_url'")
            ).fetchone()
            
            if result:
                print("   ✓ Coluna cover_url já existe")
            else:
                print("   ⚠ Adicionando coluna cover_url...")
                db.session.execute(
                    text("ALTER TABLE books ADD COLUMN cover_url VARCHAR(500) NULL")
                )
                db.session.commit()
                print("   ✓ Coluna cover_url adicionada")
            
            print("\n" + "=" * 70)
            print("✅ OPERAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    main()
