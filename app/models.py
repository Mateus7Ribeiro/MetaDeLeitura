from app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    current_page = db.Column(db.Integer, default=0, nullable=False)
    current_percentage = db.Column(db.Float, default=0.0, nullable=False)
    target_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)
    
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
            'target_date': self.target_date.strftime('%d/%m/%Y'),
            'is_completed': self.is_completed,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        }
