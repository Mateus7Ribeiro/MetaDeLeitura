#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migração para criar tabela CollectiveReadingProgress
"""

from app import create_app
import pymysql

if __name__ == '__main__':
    app = create_app(create_tables=False)
    
    with app.app_context():
        print("Criando tabela CollectiveReadingProgress...")
        try:
            from app import db
            # Verificar se a tabela já existe
            connection = db.engine.connect()
            try:
                connection.execute(db.text("SELECT 1 FROM collective_reading_progress LIMIT 1"))
                print("✅ Tabela CollectiveReadingProgress já existe!")
            except:
                # Tabela não existe, criar manualmente
                print("Criando tabela...")
                connection.execute(db.text("""
                    CREATE TABLE IF NOT EXISTS collective_reading_progress (
                        id INTEGER NOT NULL AUTO_INCREMENT,
                        collective_reading_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        book_order INTEGER NOT NULL,
                        pages_read INTEGER NOT NULL DEFAULT 0,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id),
                        UNIQUE KEY unique_user_book_progress (collective_reading_id, user_id, book_order),
                        FOREIGN KEY (collective_reading_id) REFERENCES collective_readings(id) ON DELETE CASCADE,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """))
                connection.commit()
                print("✅ Tabela CollectiveReadingProgress criada com sucesso!")
            finally:
                connection.close()
        except Exception as e:
            print(f"❌ Erro ao criar tabela: {e}")
            import traceback
            traceback.print_exc()


