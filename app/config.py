import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuração base"""
    # Configuração do Banco de Dados
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:"
        f"{os.getenv('DB_PASSWORD', 'root')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'meta_leitura')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
    }
    
    # Configuração do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production-12345')
    JSON_SORT_KEYS = False
    
    # Configuração de Sessão
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 7 * 24 * 60 * 60  # 7 dias
    
    # Upload de arquivos
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    UPLOAD_FOLDER = 'static/uploads'
    
    # Debug
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    TESTING = False
    
    # Segurança aprimorada
    SESSION_COOKIE_SECURE = True  # Requer HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Secret key obrigatória em produção (validação adiada para runtime)
    def __init__(self):
        super().__init__()
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key and os.getenv('SKIP_SECRET_KEY_CHECK') != '1':
            import warnings
            warnings.warn(
                "SECRET_KEY não definida em produção! "
                "Configure no arquivo .env ou defina SKIP_SECRET_KEY_CHECK=1 para scripts."
            )
    
    # Validar configuração do banco
    if 'localhost' in os.getenv('DB_HOST', 'localhost'):
        import warnings
        warnings.warn("DB_HOST configurado como localhost em produção!")


class TestingConfig(Config):
    """Configuração de testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Mapeamento de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
