#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste para verificar se a correção de datas funciona corretamente
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, CollectiveReading, CollectiveReadingBook

def test_collective_creation_with_dates():
    """Testa a criação de leitura coletiva com datas"""
    print("\n" + "="*60)
    print("TESTE: CRIAÇÃO DE LEITURA COLETIVA COM DATAS")
    print("="*60)
    
    app = create_app()
    with app.app_context():
        try:
            # Buscar ou criar usuário de teste
            test_user = User.query.filter_by(username='test_user').first()
            if not test_user:
                test_user = User(username='test_user', email='test@example.com')
                test_user.set_password('test123')
                db.session.add(test_user)
                db.session.commit()
                print(f"✅ Usuário criado: {test_user.username}")
            else:
                print(f"✅ Usuário encontrado: {test_user.username}")
            
            # Limpar dados de teste anteriores (deletar livros primeiro por FK)
            readings = CollectiveReading.query.filter_by(creator_id=test_user.id).all()
            for reading in readings:
                for book in reading.books:
                    db.session.delete(book)
                db.session.delete(reading)
            db.session.commit()
            
            # Dados para criação
            start_date = datetime.now()
            end_date = datetime.now() + timedelta(days=30)
            
            # Criar leitura coletiva com datas
            collective = CollectiveReading(
                creator_id=test_user.id,
                name='Teste com Datas',
                description='Uma leitura para testar as datas',
                start_date=start_date,
                end_date=end_date
            )
            collective.generate_share_hash()
            
            db.session.add(collective)
            db.session.commit()
            
            print(f"\n✅ Leitura coletiva criada com sucesso!")
            print(f"   - Nome: {collective.name}")
            print(f"   - Criador: {collective.creator.username}")
            print(f"   - Início: {collective.start_date.strftime('%d/%m/%Y')}")
            print(f"   - Término: {collective.end_date.strftime('%d/%m/%Y')}")
            print(f"   - Hash: {collective.share_hash}")
            
            # Verificar se foi salvo corretamente
            retrieved = CollectiveReading.query.get(collective.id)
            if retrieved and retrieved.start_date and retrieved.end_date:
                print(f"\n✅ Datas foram salvas corretamente no banco!")
                print(f"   - Start date no BD: {retrieved.start_date}")
                print(f"   - End date no BD: {retrieved.end_date}")
                print(f"\n✨ TESTE PASSOU!")
                return True
            else:
                print(f"\n❌ Datas não foram salvas corretamente")
                return False
            
        except Exception as e:
            print(f"\n❌ Erro ao criar leitura coletiva com datas:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    result = test_collective_creation_with_dates()
    sys.exit(0 if result else 1)
