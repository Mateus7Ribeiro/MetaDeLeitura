#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug teste para botão Sair
"""

import sys
from app import create_app, db
from app.models import CollectiveReading, CollectiveReadingParticipant, User

app = create_app()

with app.app_context():
    collective = CollectiveReading.query.filter_by(name='Saga Senhor dos Anéis').first()
    user = User.query.filter(User.id != collective.creator_id).first()
    
    # Verificar se é participante
    participant = CollectiveReadingParticipant.query.filter_by(
        collective_reading_id=collective.id,
        user_id=user.id
    ).first()
    
    print(f"Coletiva: {collective.id}")
    print(f"Usuário: {user.id} ({user.username})")
    print(f"É participante: {participant is not None}")
    
    if not participant:
        print("Adicionando como participante...")
        p = CollectiveReadingParticipant(
            collective_reading_id=collective.id,
            user_id=user.id
        )
        db.session.add(p)
        db.session.commit()
    
    # Testar com client
    client = app.test_client()
    
    with client.session_transaction() as sess:
        sess['user_id'] = user.id
    
    print("\nTestando POST /collective/{}/leave".format(collective.id))
    response = client.post(f'/collective/{collective.id}/leave')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Verificar se foi removido
    participant = CollectiveReadingParticipant.query.filter_by(
        collective_reading_id=collective.id,
        user_id=user.id
    ).first()
    print(f"Ainda é participante: {participant is not None}")
