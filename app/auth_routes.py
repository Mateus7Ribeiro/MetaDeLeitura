from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import User, Book
from app.auth import login_required, get_current_user
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registrar novo usuário"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Validações
        if not username or not email or not password:
            return render_template('register.html', error='Todos os campos são obrigatórios'), 400
        
        if password != password_confirm:
            return render_template('register.html', error='Senhas não conferem'), 400
        
        if len(password) < 6:
            return render_template('register.html', error='Senha deve ter no mínimo 6 caracteres'), 400
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Nome de usuário já existe'), 400
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email já está registrado'), 400
        
        # Criar novo usuário
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login do usuário"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validações
        if not username or not password:
            return render_template('login.html', error='Username e senha são obrigatórios'), 400
        
        # Verificar usuário
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return render_template('login.html', error='Username ou senha incorretos'), 400
        
        # Criar sessão
        session['user_id'] = user.id
        session['username'] = user.username
        
        return redirect(url_for('main.index'))
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Página de configurações do usuário"""
    user = get_current_user()
    
    if request.method == 'POST':
        try:
            reading_speed = float(request.form.get('reading_speed', user.reading_speed))
            
            if reading_speed <= 0:
                return render_template('settings.html', user=user, error='Velocidade deve ser maior que 0'), 400
            
            user.reading_speed = reading_speed
            db.session.commit()
            
            return render_template('settings.html', user=user, success='Configurações salvas com sucesso!')
        except ValueError:
            return render_template('settings.html', user=user, error='Velocidade de leitura inválida'), 400
    
    return render_template('settings.html', user=user)
