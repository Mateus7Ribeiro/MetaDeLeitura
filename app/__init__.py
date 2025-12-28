from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)
    
    db.init_app(app)
    
    from app.models import Book
    
    with app.app_context():
        db.create_all()
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
