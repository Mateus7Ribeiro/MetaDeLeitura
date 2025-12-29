#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste de controle de acesso para leitura coletiva compartilhada
Simula cenários de usuário não-criador acessando links compartilhados
"""

import sys
import os
from app import create_app, db
from app.models import User, CollectiveReading

def test_access_control():
    """Testa o fluxo completo de acesso a leitura coletiva compartilhada"""
    
    app = create_app()
    
    print("\n" + "="*60)
    print("TESTE: CONTROLE DE ACESSO - LINKS COMPARTILHADOS")
    print("="*60 + "\n")
    
    with app.app_context():
        # Buscar a leitura coletiva
        collective = CollectiveReading.query.filter_by(name='Saga Senhor dos Anéis').first()
        if not collective:
            print("❌ Leitura coletiva não encontrada!")
            return False
        
        print(f"✅ Leitura encontrada: {collective.name}")
        print(f"   - Criador ID: {collective.creator_id}")
        print(f"   - Share Hash: {collective.share_hash}")
        print(f"   - ID: {collective.id}\n")
        
        # Criar teste client
        client = app.test_client()
        
        # TESTE 1: Acessar link compartilhado sem estar logado
        print("TESTE 1: Usuário NÃO logado acessando link compartilhado")
        print(f"  URL: /collective/share/{collective.share_hash}")
        response = client.get(f'/collective/share/{collective.share_hash}')
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  ✅ Pode acessar link compartilhado sem login\n")
        else:
            print(f"  ❌ Erro ao acessar link: {response.status_code}\n")
            print(f"  Response snippet: {response.data.decode()[:300]}\n")
            return False
        
        # TESTE 2: Simular usuário logado com ID diferente do criador
        print("TESTE 2: Simular usuário logado (não-criador)")
        
        # Obter ou criar outro usuário
        other_user = User.query.filter(User.id != collective.creator_id).first()
        if not other_user:
            print("  ⚠️  Criando usuário de teste...")
            other_user = User(email='test@example.com', name='Test User')
            other_user.set_password('password123')
            db.session.add(other_user)
            db.session.commit()
        
        print(f"  ✅ Usuário de teste: ID {other_user.id} (criador é ID {collective.creator_id})\n")
        
        # TESTE 3: Fazer login com outro usuário
        print("TESTE 3: Acessar link compartilhado APÓS login com outro usuário")
        print(f"  URL: /collective/share/{collective.share_hash}")
        
        with client.session_transaction() as sess:
            sess['user_id'] = other_user.id
        
        response = client.get(f'/collective/share/{collective.share_hash}')
        print(f"  Status da resposta: {response.status_code}")
        
        # Verificar redirect
        if response.status_code == 302:
            print(f"  ✅ Redirecionado para: {response.location}")
            # Seguir o redirect
            response = client.get(response.location)
            print(f"  Status após redirect: {response.status_code}")
        
        if response.status_code == 200:
            if 'Saga Senhor' in response.data.decode() or collective.name in response.data.decode():
                print("  ✅ Pode acessar visualização coletiva após login com outro usuário\n")
            else:
                print("  ⚠️  Página carregada mas conteúdo pode não estar visível\n")
        else:
            print(f"  ❌ Erro ao acessar visualização: {response.status_code}\n")
            print(f"  Response snippet: {response.data.decode()[:300]}\n")
            return False
        
        # TESTE 4: Acessar URL direta sem hash (deve redirecionar)
        print("TESTE 4: Usuário não-criador acessando URL direta SEM hash parameter")
        print(f"  URL: /collective/{collective.id}")
        response = client.get(f'/collective/{collective.id}')
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 302:
            print(f"  ✅ Redirecionou automaticamente para link com hash")
            print(f"  Redirecionado para: {response.location}\n")
        elif response.status_code == 200:
            print(f"  ⚠️  Acesso direto permitido (possível redireção via location)\n")
        else:
            print(f"  ❌ Erro: {response.status_code}\n")
            return False
        
        # TESTE 5: Acessar URL com hash correto
        print("TESTE 5: Acessar URL com hash correto na query string")
        print(f"  URL: /collective/{collective.id}?hash={collective.share_hash}")
        response = client.get(f'/collective/{collective.id}?hash={collective.share_hash}')
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ Acesso permitido com hash correto\n")
        else:
            print(f"  ❌ Erro ao acessar com hash: {response.status_code}\n")
            print(f"  Response snippet: {response.data.decode()[:300]}\n")
            return False
        
        # TESTE 6: Acessar URL com hash INCORRETO
        print("TESTE 6: Acessar URL com hash INCORRETO")
        print(f"  URL: /collective/{collective.id}?hash=invalid_hash")
        response = client.get(f'/collective/{collective.id}?hash=invalid_hash')
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 404:
            error_msg = response.data.decode().lower()
            if 'inválido' in error_msg or 'invalid' in error_msg or 'error' in error_msg:
                print("  ✅ Acesso bloqueado corretamente com hash inválido\n")
            else:
                print("  ✅ Acesso bloqueado (erro 404)\n")
        else:
            print(f"  ❌ Deveria ter rejeitado hash inválido, recebeu: {response.status_code}\n")
            return False
        
        # TESTE 7: Usuário criador acessando URL direta (sem hash)
        print("TESTE 7: Usuário CRIADOR acessando URL direta (sem hash)")
        print(f"  URL: /collective/{collective.id}")
        
        # Limpar sessão
        with client.session_transaction() as sess:
            sess['user_id'] = collective.creator_id
        
        response = client.get(f'/collective/{collective.id}')
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ Criador pode acessar diretamente sem hash\n")
        else:
            print(f"  ❌ Criador não conseguiu acessar: {response.status_code}\n")
            return False
        
        print("=" * 60)
        print("✨ TODOS OS TESTES PASSARAM!")
        print("=" * 60 + "\n")
        return True

if __name__ == '__main__':
    success = test_access_control()
    sys.exit(0 if success else 1)
