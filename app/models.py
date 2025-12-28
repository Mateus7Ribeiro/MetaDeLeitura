from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    reading_speed = db.Column(db.Float, default=2.5)  # minutos por página
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com livros
    books = db.relationship('Book', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Criptografa a senha"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'reading_speed': self.reading_speed,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        }


class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    current_page = db.Column(db.Integer, default=0, nullable=False)
    current_percentage = db.Column(db.Float, default=0.0, nullable=False)
    target_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)  # Novo: livro público
    
    def __repr__(self):
        return f'<Book {self.name}>'
    
    def update_progress(self, current_page=None, current_percentage=None):
        """Atualiza o progresso do livro"""
        if current_page is not None:
            self.current_page = min(current_page, self.total_pages)
            self.current_percentage = (self.current_page / self.total_pages) * 100
        elif current_percentage is not None:
            self.current_percentage = min(current_percentage, 100.0)
            self.current_page = int((self.current_percentage / 100) * self.total_pages)
        
        if self.current_page >= self.total_pages:
            self.is_completed = True
        
        self.updated_at = datetime.utcnow()
        return self
    
    def get_pages_remaining(self):
        """Retorna quantidade de páginas restantes"""
        return max(0, self.total_pages - self.current_page)
    
    def get_percentage_remaining(self):
        """Retorna percentual restante"""
        return max(0.0, 100.0 - self.current_percentage)
    
    def get_pages_per_day(self):
        """Calcula páginas por dia necessárias para atingir a meta"""
        from datetime import datetime
        
        if self.is_completed:
            return 0
        
        pages_remaining = self.get_pages_remaining()
        if pages_remaining <= 0:
            return 0
        
        now = datetime.utcnow()
        days_remaining = (self.target_date - now).days
        
        if days_remaining <= 0:
            return pages_remaining
        
        return pages_remaining / days_remaining
    
    def get_days_remaining(self):
        """Retorna quantidade de dias até a data limite"""
        from datetime import datetime
        
        if self.is_completed:
            return 0
        
        now = datetime.utcnow()
        days = (self.target_date - now).days
        return max(0, days)
    
    def get_daily_reading_time(self):
        """Calcula tempo diário em minutos usando a velocidade do usuário"""
        pages_per_day = self.get_pages_per_day()
        if pages_per_day <= 0:
            return 0
        
        reading_speed = self.owner.reading_speed if self.owner else 2.5
        return pages_per_day * reading_speed
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'total_pages': self.total_pages,
            'current_page': self.current_page,
            'current_percentage': round(self.current_percentage, 2),
            'pages_remaining': self.get_pages_remaining(),
            'percentage_remaining': round(self.get_percentage_remaining(), 2),
            'pages_per_day': round(self.get_pages_per_day(), 2),
            'days_remaining': self.get_days_remaining(),
            'daily_reading_time': round(self.get_daily_reading_time(), 1),
            'target_date': self.target_date.strftime('%d/%m/%Y'),
            'is_completed': self.is_completed,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        }
