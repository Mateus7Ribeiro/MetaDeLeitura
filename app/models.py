from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import hashlib


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
    cover_url = db.Column(db.String(500))  # URL da capa do livro
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


class CollectiveReading(db.Model):
    """Modelo para Leituras Coletivas (múltiplos livros em sequência)"""
    __tablename__ = 'collective_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    share_hash = db.Column(db.String(64), unique=True, nullable=False)  # Para compartilhamento
    
    # Datas gerais
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='collective_readings_created', lazy=True)
    books = db.relationship('CollectiveReadingBook', backref='collective_reading', lazy=True, cascade='all, delete-orphan')
    participants = db.relationship('CollectiveReadingParticipant', backref='collective_reading', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(CollectiveReading, self).__init__(**kwargs)
        if not self.share_hash:
            self.generate_share_hash()
    
    def __repr__(self):
        return f'<CollectiveReading {self.name}>'
    
    def generate_share_hash(self):
        """Gera um hash único para compartilhamento (uma única vez)"""
        # Hash baseado em: criador + nome (garante consistência sem UUID)
        # Usa dados que não mudam após criação
        unique_str = f"{self.creator_id}_{self.name}"
        self.share_hash = hashlib.sha256(unique_str.encode()).hexdigest()[:32]
    
    def get_total_pages(self):
        """Retorna total de páginas de todos os livros"""
        return sum(book.total_pages for book in self.books)
    
    def get_pages_per_day(self):
        """Calcula páginas por dia necessárias"""
        total_pages = self.get_total_pages()
        if total_pages <= 0:
            return 0
        
        days = (self.end_date - self.start_date).days
        if days <= 0:
            return total_pages
        
        return total_pages / days
    
    def get_ideal_progress_percentage(self):
        """Retorna percentual ideal para estar em dia"""
        from datetime import datetime
        now = datetime.utcnow()
        
        if now >= self.end_date:
            return 100.0
        
        if now <= self.start_date:
            return 0.0
        
        total_days = (self.end_date - self.start_date).days
        elapsed_days = (now - self.start_date).days
        
        if total_days <= 0:
            return 0.0
        
        return (elapsed_days / total_days) * 100


class CollectiveReadingBook(db.Model):
    """Livros que fazem parte de uma leitura coletiva (em sequência)"""
    __tablename__ = 'collective_reading_books'
    
    id = db.Column(db.Integer, primary_key=True)
    collective_reading_id = db.Column(db.Integer, db.ForeignKey('collective_readings.id'), nullable=False)
    
    title = db.Column(db.String(255), nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)  # Ordem na sequência
    
    # Datas de início e fim desta parte da leitura
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    # URL da capa (não armazenar no servidor)
    cover_url = db.Column(db.String(500))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CollectiveReadingBook {self.title}>'


class CollectiveReadingParticipant(db.Model):
    """Participantes de uma leitura coletiva e seu progresso"""
    __tablename__ = 'collective_reading_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    collective_reading_id = db.Column(db.Integer, db.ForeignKey('collective_readings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Progresso
    current_percentage = db.Column(db.Float, default=0.0)  # Percentual geral
    
    # Status
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='collective_participations')
    
    def __repr__(self):
        return f'<CollectiveReadingParticipant {self.user.username}>'
    
    def get_status(self):
        """Retorna o status: 'adiantado', 'em_dia' ou 'atrasado'"""
        ideal_progress = self.collective_reading.get_ideal_progress_percentage()
        
        # Margem de 5%
        if self.current_percentage >= ideal_progress - 5:
            if self.current_percentage <= ideal_progress + 5:
                return 'em_dia'
            return 'adiantado'
        return 'atrasado'

