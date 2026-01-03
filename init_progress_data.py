#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para inicializar dados de progresso por livro baseado no progresso geral
"""

from app import create_app, db
from app.models import (
    CollectiveReadingParticipant, CollectiveReading, 
    CollectiveReadingProgress, CollectiveReadingBook, UserFollower
)

if __name__ == '__main__':
    app = create_app(create_tables=False)
    
    with app.app_context():
        print("Inicializando dados de progresso por livro...")
        
        try:
            # Obter todos os participantes com progresso
            participants = CollectiveReadingParticipant.query.filter(
                CollectiveReadingParticipant.current_percentage > 0
            ).all()
            
            print(f"Processando {len(participants)} participantes...")
            
            for participant in participants:
                collective = participant.collective_reading
                total_pages = sum(book.total_pages for book in collective.books)
                
                if total_pages == 0:
                    continue
                
                # Calcular páginas lidas baseado no percentual geral
                total_pages_read = int((participant.current_percentage / 100) * total_pages)
                
                print(f"\n{participant.user.username} - {collective.name}")
                print(f"  Progresso geral: {participant.current_percentage:.1f}%")
                print(f"  Total de páginas: {total_pages}")
                print(f"  Páginas lidas: {total_pages_read}")
                
                # Distribuir as páginas lidas entre os livros
                # Distribuição proporcional ao número de páginas de cada livro
                remaining_pages = total_pages_read
                
                for book in collective.books:
                    # Calcular quantas páginas este livro deve ter lido
                    pages_for_this_book = int((book.total_pages / total_pages) * total_pages_read)
                    pages_for_this_book = min(pages_for_this_book, book.total_pages)
                    
                    # Criar ou atualizar registro de progresso
                    progress = CollectiveReadingProgress.query.filter_by(
                        collective_reading_id=collective.id,
                        user_id=participant.user_id,
                        book_order=book.order
                    ).first()
                    
                    if progress is None:
                        progress = CollectiveReadingProgress(
                            collective_reading_id=collective.id,
                            user_id=participant.user_id,
                            book_order=book.order,
                            pages_read=pages_for_this_book
                        )
                        db.session.add(progress)
                    else:
                        progress.pages_read = pages_for_this_book
                    
                    print(f"  Livro {book.order} ({book.title}): {pages_for_this_book}/{book.total_pages} páginas")
            
            db.session.commit()
            print("\n✅ Dados inicializados com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar dados: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
