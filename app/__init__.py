from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config
import os

db = SQLAlchemy()

def create_app(create_tables=True, config_name=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Determinar configuração a usar
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Carregar configuração apropriada
    app.config.from_object(config.get(config_name, config['development']))
    
    db.init_app(app)
    
    from app.models import Book, User
    
    with app.app_context():
        if create_tables:
            try:
                db.create_all()
            except Exception as e:
                print(f"Aviso: Erro ao criar tabelas: {e}")
    
    # Registrar blueprints
    from app.routes import main_bp
    from app.auth_routes import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    return app
