from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app import db
from app.models import User, Book
from app.auth import login_required, get_current_user
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import re

auth_bp = Blueprint('auth', __name__)

# Configurações de upload
UPLOAD_FOLDER = 'static/uploads/profiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_password(password):
    """
    Valida senha seguindo política de segurança:
    - Mínimo 8 caracteres
    - Pelo menos 1 letra maiúscula
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 número
    - Pelo menos 1 caractere especial
    """
    if len(password) < 8:
        return False, "Senha deve ter no mínimo 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "Senha deve conter pelo menos 1 letra maiúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "Senha deve conter pelo menos 1 letra minúscula"
    
    if not re.search(r'\d', password):
        return False, "Senha deve conter pelo menos 1 número"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Senha deve conter pelo menos 1 caractere especial (!@#$%^&*(),.?\":{}|<>)"
    
    return True, "Senha válida"

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
        user.user_hash = user.generate_user_hash()
        
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
        action = request.form.get('action')
        
        # Atualizar perfil (nome e velocidade de leitura)
        if action == 'update_profile':
            try:
                name = request.form.get('name', '').strip()
                reading_speed = float(request.form.get('reading_speed', user.reading_speed))
                
                if reading_speed <= 0:
                    return render_template('settings.html', user=user, error='Velocidade deve ser maior que 0'), 400
                
                user.name = name if name else user.username
                user.reading_speed = reading_speed
                db.session.commit()
                
                return render_template('settings.html', user=user, success='Perfil atualizado com sucesso!')
            except ValueError:
                return render_template('settings.html', user=user, error='Velocidade de leitura inválida'), 400
        
        # Upload de foto de perfil
        elif action == 'upload_photo':
            if 'profile_photo' not in request.files:
                return render_template('settings.html', user=user, error='Nenhum arquivo selecionado'), 400
            
            file = request.files['profile_photo']
            
            if file.filename == '':
                return render_template('settings.html', user=user, error='Nenhum arquivo selecionado'), 400
            
            if file and allowed_file(file.filename):
                # Criar diretório se não existir
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                # Gerar nome único
                filename = secure_filename(f"{user.id}_{datetime.now().timestamp()}.{file.filename.rsplit('.', 1)[1].lower()}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                
                # Salvar arquivo
                file.save(filepath)
                
                # Deletar foto antiga se existir
                if user.profile_picture and user.profile_picture.startswith('/static/uploads'):
                    old_path = user.profile_picture.lstrip('/')
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except:
                            pass
                
                # Atualizar no banco
                user.profile_picture = '/' + filepath.replace('\\', '/')
                db.session.commit()
                
                return render_template('settings.html', user=user, success='Foto atualizada com sucesso!')
            else:
                return render_template('settings.html', user=user, error='Tipo de arquivo não permitido. Use: PNG, JPG, JPEG, GIF, WEBP'), 400
        
        # Remover foto de perfil
        elif action == 'remove_photo':
            if user.profile_picture:
                # Deletar arquivo se for local
                if user.profile_picture.startswith('/static/uploads'):
                    old_path = user.profile_picture.lstrip('/')
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except:
                            pass
                
                user.profile_picture = None
                db.session.commit()
                
                return render_template('settings.html', user=user, success='Foto removida com sucesso!')
        
        # Trocar senha
        elif action == 'change_password':
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            new_password_confirm = request.form.get('new_password_confirm')
            
            # Validar senha antiga
            if not user.check_password(old_password):
                return render_template('settings.html', user=user, error='Senha atual incorreta'), 400
            
            # Validar confirmação
            if new_password != new_password_confirm:
                return render_template('settings.html', user=user, error='As senhas não conferem'), 400
            
            # Validar política de segurança
            is_valid, message = validate_password(new_password)
            if not is_valid:
                return render_template('settings.html', user=user, error=message), 400
            
            # Atualizar senha
            user.set_password(new_password)
            db.session.commit()
            
            return render_template('settings.html', user=user, success='Senha alterada com sucesso!')
    
    return render_template('settings.html', user=user)

