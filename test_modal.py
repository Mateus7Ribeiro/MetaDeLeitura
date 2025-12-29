#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to verify modal functionality"""

from app import create_app
from app.models import User, CollectiveReading, CollectiveReadingParticipant

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        user = User.query.first()
        if user:
            print(f'Usuário: {user.username}')
            
            participations = CollectiveReading.query.join(
                CollectiveReadingParticipant
            ).filter(
                CollectiveReadingParticipant.user_id == user.id
            ).all()
            
            print(f'Leituras coletivas: {len(participations)}')
            for p in participations:
                print(f'  - {p.name} ({len(p.books)} livros)')
                for book in p.books:
                    print(f'    * Livro {book.order}: {book.title}')
        else:
            print("Nenhum usuário encontrado")
