import os
from dotenv import load_dotenv

load_dotenv()

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
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    JSON_SORT_KEYS = False
