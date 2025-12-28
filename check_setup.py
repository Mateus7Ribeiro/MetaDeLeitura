"""
Script de verificação de dependências e configuração
Execute com: python check_setup.py
"""

import sys
import os
from pathlib import Path

def print_header(text):
    print(f"\n{'='*50}")
    print(f"  {text}")
    print('='*50)

def check_python_version():
    """Verifica versão do Python"""
    print_header("Verificando Python")
    version = sys.version
    print(f"✓ Python: {version}")
    if sys.version_info < (3, 8):
        print("⚠ Aviso: Python 3.8+ recomendado")
        return False
    return True

def check_files():
    """Verifica estrutura de arquivos"""
    print_header("Verificando Estrutura de Arquivos")
    
    required_files = [
        'run.py',
        'requirements.txt',
        '.env',
        'app/__init__.py',
        'app/config.py',
        'app/models.py',
        'app/routes.py',
        'templates/base.html',
        'templates/index.html',
        'templates/add_book.html',
        'templates/edit_book.html',
        'templates/book_detail.html',
        'static/css/style.css',
        'static/js/script.js',
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - FALTANDO!")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Verifica dependências instaladas"""
    print_header("Verificando Dependências Python")
    
    dependencies = [
        'flask',
        'flask_sqlalchemy',
        'flask_migrate',
        'pymysql',
        'dotenv',
    ]
    
    missing = []
    for package in dependencies:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NÃO INSTALADO!")
            missing.append(package)
    
    if missing:
        print(f"\nInstale com: pip install {' '.join(missing)}")
    
    return len(missing) == 0

def check_env_config():
    """Verifica configuração do .env"""
    print_header("Verificando Arquivo .env")
    
    env_file = Path('.env')
    
    if not env_file.exists():
        print("✗ Arquivo .env não encontrado!")
        return False
    
    print("✓ Arquivo .env encontrado")
    
    # Ler .env
    required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME', 'SECRET_KEY']
    
    with open('.env', 'r') as f:
        env_content = f.read()
    
    for var in required_vars:
        if var in env_content:
            print(f"✓ {var} - configurado")
        else:
            print(f"⚠ {var} - não encontrado (opcional)")
    
    return True

def main():
    print("\n")
    print("╔════════════════════════════════════════════╗")
    print("║  META DE LEITURA - Verificação de Setup  ║")
    print("╚════════════════════════════════════════════╝")
    
    checks = [
        ("Python", check_python_version),
        ("Arquivos", check_files),
        ("Arquivo .env", check_env_config),
        ("Dependências", check_dependencies),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Erro ao verificar {name}: {e}")
            results.append((name, False))
    
    # Resumo
    print_header("RESUMO")
    
    all_passed = True
    for name, result in results:
        status = "✓ OK" if result else "✗ FALHOU"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    print("\n")
    
    if all_passed:
        print("╔════════════════════════════════════════════╗")
        print("║   ✓ TUDO PRONTO! Sistema configurado!     ║")
        print("║   Execute: python run.py                   ║")
        print("╚════════════════════════════════════════════╝\n")
        return 0
    else:
        print("╔════════════════════════════════════════════╗")
        print("║   ✗ Existem problemas a resolver          ║")
        print("║   Verifique os erros acima                ║")
        print("╚════════════════════════════════════════════╝\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
