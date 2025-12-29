#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test para verificar se os templates renderizam corretamente"""

from app import create_app
from app.models import User

if __name__ == '__main__':
    app = create_app()
    
    # Criar um cliente de teste
    with app.test_client() as client:
        # Fazer login (simular sessão)
        with client.session_transaction() as sess:
            user = User.query.first()
            if user:
                sess['user_id'] = user.id
        
        # Testar a página de livros
        response = client.get('/user/books')
        if response.status_code == 200:
            print("✅ Página /user/books renderizou com sucesso (200)")
            
            # Verificar se o modal está no HTML
            if b'progressModalCollective' in response.data:
                print("✅ Modal progressModalCollective encontrado no HTML")
            else:
                print("❌ Modal progressModalCollective NÃO encontrado no HTML")
            
            # Verificar se a função openProgressModalCollective está no JS
            if b'openProgressModalCollective' in response.data:
                print("✅ Função openProgressModalCollective encontrada no HTML")
            else:
                print("❌ Função openProgressModalCollective NÃO encontrada no HTML")
                
            # Verificar se o modal do collective_view está funcionando
            collective_id = 1  # Assumindo ID 1
            response2 = client.get(f'/collective/{collective_id}?hash=test123')
            if b'progressModal' in response2.data:
                print("✅ Modal progressModal encontrado em collective_view")
            else:
                print("❌ Modal progressModal NÃO encontrado em collective_view")
        else:
            print(f"❌ Página /user/books retornou status {response.status_code}")
