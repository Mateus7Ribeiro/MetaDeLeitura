"""
Script para adicionar as tabelas de Leituras Coletivas
Execute com: python migrate_collective_reading.py
"""

from app import create_app, db
from sqlalchemy import text

def main():
    print("=" * 70)
    print("ADICIONANDO TABELAS DE LEITURAS COLETIVAS")
    print("=" * 70)
    print()
    
    app = create_app()
    
    with app.app_context():
        try:
            # Criar todas as tabelas
            print("1️⃣  Criando tabelas...")
            db.create_all()
            print("   ✓ Tabelas criadas com sucesso!")
            
            # Verificar se tabelas existem
            tables_to_check = ['collective_readings', 'collective_reading_books', 'collective_reading_participants']
            
            print("\n2️⃣  Verificando tabelas...")
            for table in tables_to_check:
                result = db.session.execute(
                    text(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='{table}'")
                ).fetchone()
                
                if result:
                    print(f"   ✓ Tabela '{table}' existe")
                else:
                    print(f"   ⚠ Tabela '{table}' não encontrada")
            
            print("\n" + "=" * 70)
            print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            print()
            print("Próximos passos:")
            print("1. Execute: python run.py")
            print("2. Teste a nova funcionalidade de Leituras Coletivas")
            print("3. Acesse: http://localhost:5000/collective")
            
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    main()
