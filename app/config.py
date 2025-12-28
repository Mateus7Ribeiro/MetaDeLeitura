import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
env_file = '.env.production' if os.getenv('FLASK_ENV') == 'production' else '.env'
load_dotenv(env_file)

class Config:
    # Configuração do Banco de Dados
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:"
        f"{os.getenv('DB_PASSWORD', 'root')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'meta_leitura')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production-12345')
    JSON_SORT_KEYS = False
    
    # Configuração de Sessão
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'  # HTTPS em produção
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 7 * 24 * 60 * 60  # 7 dias
