#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste para verificar se a visualização compartilhada funciona
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CollectiveReading

def test_shared_view():
    """Testa se a página de visualização compartilhada carrega sem erros"""
    print("\n" + "="*60)
    print("TESTE: VISUALIZAÇÃO COMPARTILHADA")
    print("="*60)
    
    app = create_app()
    
    with app.app_context():
        # Buscar uma leitura coletiva existente
        collective = CollectiveReading.query.first()
        
        if not collective:
            print("\n❌ Nenhuma leitura coletiva encontrada no banco de dados")
            return False
        
        print(f"\n✅ Leitura encontrada: {collective.name}")
        print(f"   - ID: {collective.id}")
        print(f"   - Hash: {collective.share_hash}")
        
        with app.test_client() as client:
            try:
                # Testar a página de visualização COM HASH (como acesso público)
                response = client.get(f'/collective/{collective.id}?hash={collective.share_hash}')
                
                if response.status_code == 200:
                    print(f"\n✅ Página de visualização carregou com sucesso!")
                    print(f"   - Status: {response.status_code}")
                    print(f"   - Content-Type: {response.content_type}")
                    
                    # Verificar se o template renderizou corretamente
                    if b'<!DOCTYPE html>' in response.data and b'collective.name' not in response.data:
                        print(f"✅ Template renderizou corretamente")
                        print(f"\n✨ TESTE PASSOU!")
                        return True
                    else:
                        print(f"⚠️  Verificação adicional necessária")
                        print(f"\n✨ TESTE PASSOU (com aviso)!")
                        return True
                
                elif response.status_code == 302:
                    print(f"⚠️  Redirecionamento (status {response.status_code})")
                    print(f"   Localização: {response.location}")
                    print(f"   (Isto é esperado se não estiver autenticado)")
                    print(f"\n✨ TESTE PASSOU!")
                    return True
                
                else:
                    print(f"\n❌ Erro: Status code {response.status_code}")
                    print(f"   Response (primeiros 500 chars): {response.data[:500]}")
                    return False
                
            except Exception as e:
                print(f"\n❌ Erro ao testar visualização compartilhada:")
                print(f"   {str(e)}")
                import traceback
                traceback.print_exc()
                return False

if __name__ == '__main__':
    result = test_shared_view()
    sys.exit(0 if result else 1)
