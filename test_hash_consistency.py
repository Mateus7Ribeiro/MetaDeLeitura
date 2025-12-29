#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste para verificar se o hash de compartilhamento é consistente
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, CollectiveReading, CollectiveReadingBook, CollectiveReadingParticipant

def test_hash_consistency():
    """Testa se o hash permanece o mesmo após múltiplas consultas"""
    print("\n" + "="*60)
    print("TESTE: CONSISTÊNCIA DO HASH DE COMPARTILHAMENTO")
    print("="*60)
    
    app = create_app()
    with app.app_context():
        try:
            # Buscar ou criar usuário
            user = User.query.filter_by(username='test_user').first()
            if not user:
                user = User(username='test_user', email='test@example.com')
                user.set_password('test123')
                db.session.add(user)
                db.session.commit()
            
            # Limpar leituras antigas
            readings = CollectiveReading.query.filter_by(creator_id=user.id).all()
            for reading in readings:
                for book in reading.books:
                    db.session.delete(book)
                db.session.delete(reading)
            db.session.commit()
            
            # Criar nova leitura coletiva
            collective = CollectiveReading(
                creator_id=user.id,
                name='Teste Hash Consistente',
                description='Teste para verificar hash consistente',
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=30)
            )
            collective.generate_share_hash()
            hash_1 = collective.share_hash
            
            db.session.add(collective)
            db.session.commit()
            
            print(f"\n✅ Leitura coletiva criada:")
            print(f"   - Nome: {collective.name}")
            print(f"   - ID: {collective.id}")
            print(f"   - Hash 1ª geração: {hash_1}")
            
            # Obter a mesma leitura do BD
            collective_from_db = CollectiveReading.query.get(collective.id)
            hash_2 = collective_from_db.share_hash
            
            print(f"\n✅ Leitura recuperada do BD:")
            print(f"   - Hash 2ª consulta: {hash_2}")
            
            # Tentar gerar hash novamente (não deve mudar!)
            collective_from_db.generate_share_hash()
            hash_3 = collective_from_db.share_hash
            
            print(f"\n✅ Hash regenerado:")
            print(f"   - Hash após gerar novamente: {hash_3}")
            
            # Comparar hashes
            print(f"\n📊 Comparação:")
            print(f"   - Hash 1ª == Hash 2ª: {hash_1 == hash_2}")
            print(f"   - Hash 2ª == Hash 3ª: {hash_2 == hash_3}")
            print(f"   - Hash 1ª == Hash 3ª: {hash_1 == hash_3}")
            
            if hash_1 == hash_2 == hash_3:
                print(f"\n✨ SUCESSO! Hash é consistente!")
                print(f"   O link pode ser compartilhado múltiplas vezes")
                print(f"   Hash final: {hash_1}")
                return True
            else:
                print(f"\n❌ FALHA! Hash não é consistente!")
                print(f"   Hash muda a cada geração")
                return False
            
        except Exception as e:
            print(f"\n❌ Erro ao testar hash:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    result = test_hash_consistency()
    sys.exit(0 if result else 1)
