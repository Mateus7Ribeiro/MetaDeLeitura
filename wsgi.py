"""
WSGI file for PythonAnywhere deployment
Configure this file in the PythonAnywhere Web tab
"""
import sys
import os

# Adicionar o diretório do projeto ao path
project_home = '/home/YOUR_USERNAME/MetaDeLeitura'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Carregar variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
dotenv_path = os.path.join(project_home, '.env')
load_dotenv(dotenv_path)

# Criar aplicação Flask
from app import create_app
application = create_app()
