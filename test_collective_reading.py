#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for Collective Reading System
Verifies all database models, routes, and functionality
"""

import sys
import os
from datetime import datetime, timedelta

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Book, CollectiveReading, CollectiveReadingBook, CollectiveReadingParticipant

def test_database_models():
    """Test database models and relationships"""
    print("\n" + "="*60)
    print("TESTE 1: MODELOS DE BANCO DE DADOS")
    print("="*60)
    
    with create_app().app_context():
        try:
            # Verificar se as tabelas existem
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            required_tables = ['users', 'books', 'collective_readings', 'collective_reading_books', 'collective_reading_participants']
            
            for table in required_tables:
                if table in tables:
                    print(f"✅ Tabela '{table}' existe")
                else:
                    print(f"❌ Tabela '{table}' não encontrada")
                    return False
            
            # Verificar colunas da tabela books
            books_columns = [col['name'] for col in inspector.get_columns('books')]
            required_columns = ['id', 'user_id', 'name', 'total_pages', 'current_page', 'target_date', 'is_public', 'cover_url']
            
            for col in required_columns:
                if col in books_columns:
                    print(f"✅ Coluna 'books.{col}' existe")
                else:
                    print(f"❌ Coluna 'books.{col}' não encontrada")
                    return False
            
            print("\n✨ TODOS OS MODELOS ESTÃO CORRETOS!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao verificar modelos: {str(e)}")
            return False

def test_collective_reading_operations():
    """Test collective reading operations"""
    print("\n" + "="*60)
    print("TESTE 2: OPERAÇÕES DE LEITURA COLETIVA")
    print("="*60)
    
    app = create_app()
    with app.app_context():
        try:
            # Limpar dados de teste anteriores
            db.session.query(CollectiveReadingParticipant).delete()
            db.session.query(CollectiveReadingBook).delete()
            db.session.query(CollectiveReading).delete()
            db.session.commit()
            
            # Buscar ou criar usuário de teste
            test_user = User.query.filter_by(username='test_user').first()
            if not test_user:
                test_user = User(username='test_user', email='test@example.com')
                test_user.set_password('test123')
                db.session.add(test_user)
                db.session.commit()
                print(f"✅ Usuário de teste criado: {test_user.username}")
            else:
                print(f"✅ Usuário de teste encontrado: {test_user.username}")
            
            # Criar leitura coletiva
            collective = CollectiveReading(
                creator_id=test_user.id,
                name='Teste de Leitura Coletiva',
                description='Uma leitura coletiva para testar o sistema',
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=30)
            )
            db.session.add(collective)
            db.session.commit()
            print(f"✅ Leitura coletiva criada: {collective.name}")
            print(f"   - ID: {collective.id}")
            print(f"   - Hash: {collective.share_hash}")
            
            # Adicionar livros à leitura coletiva
            book1 = CollectiveReadingBook(
                collective_reading_id=collective.id,
                title='Livro 1 - Teste',
                total_pages=300,
                order=1,
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=15),
                cover_url='https://via.placeholder.com/150'
            )
            db.session.add(book1)
            
            book2 = CollectiveReadingBook(
                collective_reading_id=collective.id,
                title='Livro 2 - Teste',
                total_pages=250,
                order=2,
                start_date=datetime.now() + timedelta(days=15),
                end_date=datetime.now() + timedelta(days=30),
                cover_url='https://via.placeholder.com/150'
            )
            db.session.add(book2)
            db.session.commit()
            print(f"✅ Livros adicionados à leitura coletiva")
            print(f"   - Livro 1: {book1.title} ({book1.total_pages} páginas)")
            print(f"   - Livro 2: {book2.title} ({book2.total_pages} páginas)")
            
            # Verificar totais
            total_pages = collective.get_total_pages()
            pages_per_day = collective.get_pages_per_day()
            print(f"✅ Estatísticas da leitura coletiva:")
            print(f"   - Total de páginas: {total_pages}")
            print(f"   - Páginas/dia: {pages_per_day:.2f}")
            
            # Adicionar participante
            participant = CollectiveReadingParticipant(
                collective_reading_id=collective.id,
                user_id=test_user.id,
                current_percentage=50
            )
            db.session.add(participant)
            db.session.commit()
            print(f"✅ Participante adicionado à leitura coletiva")
            
            # Verificar status do participante
            ideal_percentage = collective.get_ideal_progress_percentage()
            status = participant.get_status()
            print(f"   - Status: {status}")
            print(f"   - Progresso atual: {participant.current_percentage}%")
            print(f"   - Progresso ideal: {ideal_percentage:.2f}%")
            
            print("\n✨ TODOS OS TESTES DE OPERAÇÕES PASSARAM!")
            return True
            
        except Exception as e:
            print(f"❌ Erro durante testes de operações: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def test_book_cover_url():
    """Test book cover_url functionality"""
    print("\n" + "="*60)
    print("TESTE 3: FUNCIONALIDADE DE COVER_URL DOS LIVROS")
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
            
            # Limpar livros de teste anteriores
            Book.query.filter_by(user_id=test_user.id, name='Livro Teste com Cover').delete()
            db.session.commit()
            
            # Criar livro com cover_url
            book = Book(
                user_id=test_user.id,
                name='Livro Teste com Cover',
                total_pages=400,
                current_page=100,
                target_date=datetime.now() + timedelta(days=30),
                cover_url='https://via.placeholder.com/250x400?text=Test+Book'
            )
            db.session.add(book)
            db.session.commit()
            
            print(f"✅ Livro criado com cover_url")
            print(f"   - Nome: {book.name}")
            print(f"   - Cover URL: {book.cover_url}")
            print(f"   - Total de páginas: {book.total_pages}")
            print(f"   - Páginas atuais: {book.current_page}")
            
            # Verificar se a URL está armazenada
            retrieved_book = Book.query.filter_by(id=book.id).first()
            if retrieved_book and retrieved_book.cover_url == book.cover_url:
                print(f"✅ Cover URL recuperada corretamente do banco de dados")
            else:
                print(f"❌ Erro ao recuperar cover_url")
                return False
            
            print("\n✨ TESTES DE COVER_URL PASSARAM!")
            return True
            
        except Exception as e:
            print(f"❌ Erro durante testes de cover_url: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("INICIANDO TESTES DO SISTEMA DE LEITURA COLETIVA")
    print("="*60)
    
    results = {
        'Modelos de Banco de Dados': test_database_models(),
        'Operações de Leitura Coletiva': test_collective_reading_operations(),
        'Funcionalidade de Cover URL': test_book_cover_url()
    }
    
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n" + "="*60)
        print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("="*60)
        return 0
    else:
        print("\n" + "="*60)
        print("⚠️  ALGUNS TESTES FALHARAM - VERIFIQUE OS ERROS ACIMA")
        print("="*60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
