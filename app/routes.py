from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import db
from app.models import Book
from datetime import datetime
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página inicial com lista de livros"""
    books = Book.query.order_by(Book.created_at.desc()).all()
    return render_template('index.html', books=books)

@main_bp.route('/add', methods=['GET', 'POST'])
def add_book():
    """Adiciona um novo livro"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            total_pages = int(request.form.get('total_pages'))
            current_page = int(request.form.get('current_page', 0))
            target_date_str = request.form.get('target_date')
            
            # Validação
            if not name or total_pages <= 0:
                return render_template('add_book.html', error='Nome e total de páginas são obrigatórios'), 400
            
            if current_page > total_pages:
                return render_template('add_book.html', error='Páginas atuais não podem exceder o total'), 400
            
            # Converter data
            try:
                target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
            except ValueError:
                return render_template('add_book.html', error='Formato de data inválido'), 400
            
            # Criar livro
            book = Book(
                name=name,
                total_pages=total_pages,
                current_page=current_page,
                target_date=target_date
            )
            book.update_progress(current_page=current_page)
            
            db.session.add(book)
            db.session.commit()
            
            return redirect(url_for('main.index'))
        except Exception as e:
            return render_template('add_book.html', error=str(e)), 400
    
    return render_template('add_book.html')

@main_bp.route('/book/<int:book_id>')
def view_book(book_id):
    """Visualiza detalhes de um livro"""
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@main_bp.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
def edit_book(book_id):
    """Edita um livro"""
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        try:
            book.name = request.form.get('name', book.name)
            book.total_pages = int(request.form.get('total_pages', book.total_pages))
            current_page = int(request.form.get('current_page', book.current_page))
            target_date_str = request.form.get('target_date')
            
            if book.total_pages <= 0:
                return render_template('edit_book.html', book=book, error='Total de páginas deve ser maior que 0'), 400
            
            if current_page > book.total_pages:
                return render_template('edit_book.html', book=book, error='Páginas atuais não podem exceder o total'), 400
            
            if target_date_str:
                try:
                    book.target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
                except ValueError:
                    return render_template('edit_book.html', book=book, error='Formato de data inválido'), 400
            
            book.update_progress(current_page=current_page)
            db.session.commit()
            
            return redirect(url_for('main.view_book', book_id=book.id))
        except Exception as e:
            return render_template('edit_book.html', book=book, error=str(e)), 400
    
    return render_template('edit_book.html', book=book)

@main_bp.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Deleta um livro"""
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/api/book/<int:book_id>/update-progress', methods=['POST'])
def update_progress(book_id):
    """API para atualizar progresso do livro"""
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    
    try:
        if 'current_page' in data:
            book.update_progress(current_page=data['current_page'])
        elif 'current_percentage' in data:
            book.update_progress(current_percentage=data['current_percentage'])
        
        db.session.commit()
        return jsonify(book.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/books')
def get_books_api():
    """API para obter lista de livros em JSON"""
    books = Book.query.order_by(Book.created_at.desc()).all()
    return jsonify([book.to_dict() for book in books]), 200

@main_bp.route('/api/book/<int:book_id>')
def get_book_api(book_id):
    """API para obter dados de um livro"""
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict()), 200
