"""
Migração: Adicionar tabela de moderadores para Leituras Coletivas
Permite que o criador adicione co-administradores com permissão para editar
"""

from app import create_app, db
from sqlalchemy import text

def migrate():
    app = create_app()
    
    with app.app_context():
        print("=== MIGRAÇÃO: ADICIONAR MODERADORES ===")
        print("")
        
        try:
            # 1. Criar tabela de moderadores
            print("1. Criando tabela collective_reading_moderators...")
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS collective_reading_moderators (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    collective_reading_id INT NOT NULL,
                    user_id INT NOT NULL,
                    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (collective_reading_id) REFERENCES collective_readings(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_moderator (collective_reading_id, user_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """))
            db.session.commit()
            print("   Tabela criada com sucesso!")
            print("")
            
            # 2. Verificar estrutura
            print("2. Verificando estrutura da tabela...")
            result = db.session.execute(text("DESCRIBE collective_reading_moderators"))
            for row in result:
                print("   - %s: %s" % (row[0], row[1]))
            print("")
            
            print("=== MIGRAÇÃO CONCLUÍDA COM SUCESSO! ===")
            print("")
            print("Próximos passos:")
            print("1. Reinicie a aplicação")
            print("2. Acesse a página de edição de uma leitura coletiva")
            print("3. Adicione moderadores através da nova seção")
            
        except Exception as e:
            db.session.rollback()
            print("")
            print("ERRO durante a migração:")
            print(str(e))
            print("")
            print("A migração falhou. Verifique o erro acima.")
            return False
    
    return True

if __name__ == '__main__':
    migrate()
