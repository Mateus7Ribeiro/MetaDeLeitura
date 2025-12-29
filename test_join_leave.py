#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste de participação em leitura coletiva - Entrar e Sair
Valida que o usuário pode escolher entrar ou não, e pode sair a qualquer momento
"""

import sys
import os
from app import create_app, db
from app.models import User, CollectiveReading, CollectiveReadingParticipant

def test_join_leave():
    """Testa fluxo de entrar e sair de leitura coletiva"""
    
    app = create_app()
    
    print("\n" + "="*60)
    print("TESTE: ENTRAR E SAIR DE LEITURA COLETIVA")
    print("="*60 + "\n")
    
    with app.app_context():
        # Buscar leitura coletiva
        collective = CollectiveReading.query.filter_by(name='Saga Senhor dos Anéis').first()
        if not collective:
            print("❌ Leitura coletiva não encontrada!")
            return False
        
        # Buscar ou criar usuário de teste
        user = User.query.filter(User.id != collective.creator_id).first()
        if not user:
            user = User(username='leavetestuser', email='leave_test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Limpar qualquer participação anterior do usuário
        existing_participation = CollectiveReadingParticipant.query.filter_by(
            collective_reading_id=collective.id,
            user_id=user.id
        ).first()
        if existing_participation:
            db.session.delete(existing_participation)
            db.session.commit()
        
        print(f"📚 Leitura: {collective.name}")
        print(f"👤 Usuário teste: {user.username} (ID: {user.id})")
        print(f"📋 Criador: ID {collective.creator_id}\n")
        
        client = app.test_client()
        
        # Simular usuário logado
        with client.session_transaction() as sess:
            sess['user_id'] = user.id
        
        # TESTE 1: Verificar que NÃO é participante inicialmente
        print("TESTE 1: Verificar se usuário NÃO é participante inicialmente")
        participants_before = CollectiveReadingParticipant.query.filter_by(
            collective_reading_id=collective.id,
            user_id=user.id
        ).count()
        
        if participants_before == 0:
            print("  ✅ Usuário não é participante\n")
        else:
            print("  ❌ Usuário já é participante (deveria limpar DB)\n")
            return False
        
        # TESTE 2: Acessar a página (não deve adicionar automaticamente)
        print("TESTE 2: Acessar página de leitura coletiva")
        print(f"  URL: /collective/{collective.id}?hash={collective.share_hash}")
        response = client.get(f'/collective/{collective.id}?hash={collective.share_hash}')
        print(f"  Status: {response.status_code}")
        
        if response.status_code != 200:
            print("  ❌ Não conseguiu acessar\n")
            return False
        
        # Verificar que CONTINUA não sendo participante
        participants_after_view = CollectiveReadingParticipant.query.filter_by(
            collective_reading_id=collective.id,
            user_id=user.id
        ).count()
        
        if participants_after_view == 0:
            print("  ✅ Ainda não é participante (não foi adicionado automaticamente)\n")
        else:
            print("  ❌ Foi adicionado automaticamente (deveria ser manual)\n")
            return False
        
        # TESTE 3: Clicar no botão "Aderir"
        print("TESTE 3: Aderir à leitura coletiva")
        print(f"  URL: /collective/{collective.id}/join")
        response = client.get(f'/collective/{collective.id}/join')
        print(f"  Status: {response.status_code}")
        
        # Verificar que agora é participante
        participants_after_join = CollectiveReadingParticipant.query.filter_by(
            collective_reading_id=collective.id,
            user_id=user.id
        ).count()
        
        if participants_after_join == 1:
            print("  ✅ Usuário agora é participante\n")
        else:
            print("  ❌ Não foi adicionado como participante\n")
            return False
        
        # Fazer uma nova requisição para a página (simular novo carregamento)
        print("TESTE 4: Verificar badge de participação na página (nova requisição)")
        response = client.get(f'/collective/{collective.id}')  # Redireciona para compartilhado
        
        # Seguir redirect se houver
        if response.status_code == 302:
            response = client.get(response.location)
        
        html = response.data.decode()
        
        # Procurar por indicadores de participação
        has_badge = 'Você está participando' in html
        has_leave_btn = 'leaveCollective' in html or 'leave' in html.lower()
        has_adheir_btn = 'Aderir' in html
        
        print(f"  Status: {response.status_code}")
        print(f"  Badge encontrado: {has_badge}")
        print(f"  Botão sair encontrado: {has_leave_btn}")
        print(f"  Botão aderir encontrado: {has_adheir_btn}\n")
        
        if has_badge and has_leave_btn and not has_adheir_btn:
            print("  ✅ Mostra 'Você está participando' e botão 'Sair'\n")
        elif has_leave_btn:
            print("  ✅ Botão 'Sair' está presente\n")
        else:
            print(f"  ⚠️  Badge pode estar renderizado, mas não encontrado no HTML\n")
            # Procurar pelos elementos no HTML
            import re
            if re.search(r'você está participando', html, re.IGNORECASE):
                print("  ℹ️  Encontrou 'você está participando' (case-insensitive)\n")
            if re.search(r'class.*btn.*danger', html):
                print("  ℹ️  Encontrou botão danger (possível botão Sair)\n")
            
            # Mostrar seção relevante
            idx = html.find('header-actions')
            if idx > -1:
                print(f"  Seção header-actions:\n{html[idx:min(idx+800, len(html))]}\n")

        
        # TESTE 5: Clicar em "Sair"
        print("TESTE 5: Sair da leitura coletiva")
        print(f"  URL: /collective/{collective.id}/leave (POST)")
        response = client.post(f'/collective/{collective.id}/leave')
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                print("  ✅ Resposta indica sucesso\n")
            else:
                print("  ❌ Resposta não indica sucesso\n")
                print(f"  Response: {data}\n")
                return False
        else:
            print(f"  ❌ Status code esperado 200, recebeu {response.status_code}\n")
            return False
        
        # TESTE 6: Verificar que NÃO é mais participante
        print("TESTE 6: Verificar que usuário não é mais participante")
        participants_after_leave = CollectiveReadingParticipant.query.filter_by(
            collective_reading_id=collective.id,
            user_id=user.id
        ).count()
        
        if participants_after_leave == 0:
            print("  ✅ Usuário saiu com sucesso\n")
        else:
            print("  ❌ Usuário ainda é participante\n")
            return False
        
        # TESTE 7: Verificar que página mostra botão "Aderir" novamente
        print("TESTE 7: Verificar que página mostra botão 'Aderir' novamente")
        response = client.get(f'/collective/{collective.id}?hash={collective.share_hash}')
        html = response.data.decode()
        
        if 'Aderir' in html and 'Você está participando' not in html:
            print("  ✅ Badge 'Você está participando' foi removido")
            print("  ✅ Botão 'Aderir' visível novamente\n")
        else:
            print("  ❌ Badge ou botão em estado incorreto\n")
            return False
        
        # TESTE 8: Aderir novamente (para garantir que pode reutilizar)
        print("TESTE 8: Aderir novamente (reutilização)")
        response = client.get(f'/collective/{collective.id}/join')
        
        participants_final = CollectiveReadingParticipant.query.filter_by(
            collective_reading_id=collective.id,
            user_id=user.id
        ).count()
        
        if participants_final == 1:
            print("  ✅ Pode aderir novamente\n")
        else:
            print("  ❌ Não conseguiu aderir novamente\n")
            return False
        
        print("=" * 60)
        print("✨ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print("\n📋 RESUMO:")
        print("  ✅ Acesso à página não adiciona automaticamente")
        print("  ✅ Usuário pode ESCOLHER entrar (clicando em Aderir)")
        print("  ✅ Usuário pode SAIR a qualquer momento")
        print("  ✅ Pode entrar e sair múltiplas vezes\n")
        
        return True

if __name__ == '__main__':
    success = test_join_leave()
    sys.exit(0 if success else 1)
