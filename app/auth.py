from functools import wraps
from flask import session, redirect, url_for, request

def login_required(f):
    """Decorator para exigir login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Salvar a URL que o usuário tentou acessar
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Retorna o usuário atual da sessão"""
    from app.models import User
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None
