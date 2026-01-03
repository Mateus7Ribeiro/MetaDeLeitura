from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app(create_tables=True):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)
    
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
