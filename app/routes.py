from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from app.models import Book, User, CollectiveReading, CollectiveReadingBook, CollectiveReadingParticipant, UserFollower
from app.auth import login_required, get_current_user
from datetime import datetime
import json


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    """Página inicial com lista de livros"""
    user = get_current_user()
    books = Book.query.filter_by(user_id=user.id).order_by(Book.created_at.desc()).all()
    return render_template('index.html', books=books, user=user)

@main_bp.route('/profile/<user_hash>')
def view_profile(user_hash):
    """Visualizar perfil de um usuário via hash"""
    user = User.query.filter_by(user_hash=user_hash).first_or_404()
    current_user = get_current_user() if session.get('user_id') else None
    
    # Buscar livros do usuário
    books = Book.query.filter_by(user_id=user.id).order_by(Book.created_at.desc()).all()
    
    # Contar seguidores
    followers_count = len(user.followers)
    following_count = len(user.following)
    
    # Verificar se já está seguindo
    is_following = False
    if current_user and current_user.id != user.id:
        from app.models import UserFollower
        is_following = UserFollower.query.filter_by(
            follower_id=current_user.id,
            following_id=user.id
        ).first() is not None
    
    return render_template('user_profile.html', 
                         profile_user=user, 
                         user=current_user,
                         books=books,
                         followers_count=followers_count,
                         following_count=following_count,
                         is_following=is_following)

@main_bp.route('/user/<int:user_id>/follow', methods=['POST'])
@login_required
def follow_user(user_id):
    """Seguir um usuário"""
    current_user = get_current_user()
    target_user = User.query.get_or_404(user_id)
    
    if current_user.id == target_user.id:
        return jsonify({'error': 'Você não pode seguir a si mesmo'}), 400
    
    from app.models import UserFollower
    
    # Verificar se já está seguindo
    existing = UserFollower.query.filter_by(
        follower_id=current_user.id,
        following_id=target_user.id
    ).first()
    
    if not existing:
        follower = UserFollower(follower_id=current_user.id, following_id=target_user.id)
        db.session.add(follower)
        db.session.commit()
    
    return jsonify({'success': True, 'message': f'Você está seguindo {target_user.username}'}), 200

@main_bp.route('/user/<int:user_id>/unfollow', methods=['POST'])
@login_required
def unfollow_user(user_id):
    """Parar de seguir um usuário"""
    current_user = get_current_user()
    target_user = User.query.get_or_404(user_id)
    
    from app.models import UserFollower
    
    follower = UserFollower.query.filter_by(
        follower_id=current_user.id,
        following_id=target_user.id
    ).first_or_404()
    
    db.session.delete(follower)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Você parou de seguir {target_user.username}'}), 200

@main_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_book():
    """Adiciona um novo livro"""
    user = get_current_user()
    
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            total_pages = int(request.form.get('total_pages'))
            current_page = int(request.form.get('current_page', 0))
            target_date_str = request.form.get('target_date')
            cover_url = request.form.get('cover_url', '')
            
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
                user_id=user.id,
                name=name,
                total_pages=total_pages,
                current_page=current_page,
                target_date=target_date,
                cover_url=cover_url if cover_url else None
            )
            book.update_progress(current_page=current_page)
            
            db.session.add(book)
            db.session.commit()
            
            return redirect(url_for('main.index'))
        except Exception as e:
            return render_template('add_book.html', error=str(e)), 400
    
    return render_template('add_book.html')

@main_bp.route('/book/<int:book_id>')
@login_required
def view_book(book_id):
    """Visualiza detalhes de um livro"""
    user = get_current_user()
    book = Book.query.get_or_404(book_id)
    
    # Verificar se o livro pertence ao usuário ou se é um livro público para visualizar
    if book.user_id != user.id:
        return render_template('error.html', message='Acesso negado'), 403
    
    return render_template('book_detail.html', book=book, user=user)

@main_bp.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    """Edita um livro"""
    user = get_current_user()
    book = Book.query.get_or_404(book_id)
    
    # Verificar permissão
    if book.user_id != user.id:
        return render_template('error.html', message='Acesso negado'), 403
    
    if request.method == 'POST':
        try:
            book.name = request.form.get('name', book.name)
            book.total_pages = int(request.form.get('total_pages', book.total_pages))
            current_page = int(request.form.get('current_page', book.current_page))
            target_date_str = request.form.get('target_date')
            book.is_public = request.form.get('is_public') == 'true'
            cover_url = request.form.get('cover_url', '')
            book.cover_url = cover_url if cover_url else None
            
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
    
    return render_template('edit_book.html', book=book, user=user)

@main_bp.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    """Deleta um livro"""
    user = get_current_user()
    book = Book.query.get_or_404(book_id)
    
    # Verificar permissão
    if book.user_id != user.id:
        return render_template('error.html', message='Acesso negado'), 403
    
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/api/book/<int:book_id>/update-progress', methods=['POST'])
@login_required
def update_progress(book_id):
    """API para atualizar progresso do livro"""
    user = get_current_user()
    book = Book.query.get_or_404(book_id)
    
    # Verificar permissão
    if book.user_id != user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
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
@login_required
def get_books_api():
    """API para obter lista de livros em JSON"""
    user = get_current_user()
    books = Book.query.filter_by(user_id=user.id).order_by(Book.created_at.desc()).all()
    return jsonify([book.to_dict() for book in books]), 200

@main_bp.route('/api/book/<int:book_id>')
@login_required
def get_book_api(book_id):
    """API para obter dados de um livro"""
    user = get_current_user()
    book = Book.query.get_or_404(book_id)
    
    # Verificar permissão
    if book.user_id != user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    return jsonify(book.to_dict()), 200

@main_bp.route('/user/<username>')
@login_required
def view_user_books(username):
    """Visualiza livros públicos de um usuário"""
    current_user = get_current_user()
    target_user = User.query.filter_by(username=username).first_or_404()
    
    # Obter livros próprios do usuário
    user_books = Book.query.filter_by(user_id=target_user.id, is_public=True).order_by(Book.created_at.desc()).all()
    
    # Se for o próprio usuário, mostrar todos os livros (públicos e privados)
    if target_user.id == current_user.id:
        user_books = Book.query.filter_by(user_id=target_user.id).order_by(Book.created_at.desc()).all()
    
    # Obter livros das leituras coletivas que o usuário está participando
    collective_books = []
    if target_user.id == current_user.id:  # Mostrar leituras coletivas apenas para o próprio usuário
        participations = CollectiveReading.query.join(
            CollectiveReadingParticipant
        ).filter(
            CollectiveReadingParticipant.user_id == current_user.id
        ).all()
        
        for participation in participations:
            for book in participation.books:
                # Criar um wrapper para o livro com informação de leitura coletiva
                book.collective_reading = participation
                collective_books.append(book)
    
    return render_template('user_books.html', 
                         target_user=target_user, 
                         books=user_books, 
                         collective_books=collective_books,
                         current_user=current_user)

@main_bp.route('/book/<int:book_id>/public')
@login_required
def view_public_book(book_id):
    """Visualiza um livro público em modo somente leitura"""
    current_user = get_current_user()
    book = Book.query.get_or_404(book_id)
    
    # Apenas o proprietário ou um livro público pode ser visualizado
    if not book.is_public and book.user_id != current_user.id:
        return render_template('error.html', message='Este livro é privado'), 403
    
    return render_template('book_public.html', book=book, current_user=current_user, is_owner=(book.user_id == current_user.id))
# ===== ROTAS DE LEITURAS COLETIVAS =====

@main_bp.route('/collective')
@login_required
def list_collective():
    """Lista leituras coletivas (criadas e participando)"""
    user = get_current_user()
    
    # Leituras que criou
    created = CollectiveReading.query.filter_by(creator_id=user.id).order_by(CollectiveReading.created_at.desc()).all()
    
    # Leituras que participa
    participations = db.session.query(CollectiveReading).join(CollectiveReadingParticipant).filter(
        CollectiveReadingParticipant.user_id == user.id
    ).order_by(CollectiveReading.created_at.desc()).all()
    
    return render_template('collective_list.html', participations=participations, created=created, user=user)

@main_bp.route('/collective/create', methods=['GET', 'POST'])
@login_required
def create_collective():
    """Criar nova leitura coletiva"""
    user = get_current_user()
    
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            description = request.form.get('description', '')
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            
            if not name:
                return render_template('collective_create.html', error='Nome é obrigatório'), 400
            
            if not start_date_str or not end_date_str:
                return render_template('collective_create.html', error='Datas de início e término são obrigatórias'), 400
            
            # Converter datas
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            except ValueError:
                return render_template('collective_create.html', error='Formato de data inválido'), 400
            
            if start_date >= end_date:
                return render_template('collective_create.html', error='Data de início deve ser antes da data de término'), 400
            
            # Criar leitura coletiva
            collective = CollectiveReading(
                creator_id=user.id,
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date
            )
            collective.generate_share_hash()
            
            db.session.add(collective)
            db.session.commit()
            
            return redirect(url_for('main.edit_collective', collective_id=collective.id))
        except Exception as e:
            return render_template('collective_create.html', error=str(e)), 400
    
    return render_template('collective_create.html', user=user)

@main_bp.route('/collective/<int:collective_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_collective(collective_id):
    """Editar leitura coletiva (adicionar/remover livros)"""
    user = get_current_user()
    collective = CollectiveReading.query.get_or_404(collective_id)
    
    # Verificar se é o criador
    if collective.creator_id != user.id:
        return render_template('error.html', message='Acesso negado'), 403
    
    if request.method == 'POST':
        try:
            action = request.form.get('action')
            
            if action == 'update_dates':
                collective.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
                collective.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
                db.session.commit()
                return redirect(url_for('main.edit_collective', collective_id=collective.id))
            
            elif action == 'add_book':
                title = request.form.get('title')
                total_pages = int(request.form.get('total_pages'))
                start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
                end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
                cover_url = request.form.get('cover_url', '')
                
                # Validar sequência de livros
                order = len(collective.books) + 1
                
                # Verificar sobreposição de datas
                for book in collective.books:
                    if not (end_date < book.start_date or start_date > book.end_date):
                        return render_template('collective_edit.html', collective=collective, 
                                             error='Datas dos livros não podem se sobrepor'), 400
                
                new_book = CollectiveReadingBook(
                    collective_reading_id=collective.id,
                    title=title,
                    total_pages=total_pages,
                    order=order,
                    start_date=start_date,
                    end_date=end_date,
                    cover_url=cover_url
                )
                
                db.session.add(new_book)
                db.session.commit()
                return redirect(url_for('main.edit_collective', collective_id=collective.id))
            
            elif action == 'remove_book':
                book_id = int(request.form.get('book_id'))
                book = CollectiveReadingBook.query.get_or_404(book_id)
                if book.collective_reading_id != collective.id:
                    return render_template('error.html', message='Acesso negado'), 403
                
                db.session.delete(book)
                db.session.commit()
                return redirect(url_for('main.edit_collective', collective_id=collective.id))
        
        except Exception as e:
            return render_template('collective_edit.html', collective=collective, error=str(e)), 400
    
    return render_template('collective_edit.html', collective=collective, user=user)

@main_bp.route('/collective/<int:collective_id>')
def view_collective(collective_id):
    """Visualizar leitura coletiva (público ou privado com link)"""
    collective = CollectiveReading.query.get_or_404(collective_id)
    user = get_current_user() if session.get('user_id') else None
    
    # Se é o criador, pode ver sempre
    if user and user.id == collective.creator_id:
        return render_template('collective_view.html', collective=collective, user=user)
    
    # Para outros usuários (ou não logados), verificar hash
    share_hash = request.args.get('hash')
    
    # Se não tem hash na URL, redirecionar para o link de compartilhamento
    if not share_hash:
        return redirect(url_for('main.join_collective_by_hash', share_hash=collective.share_hash))
    
    # Validar hash
    if share_hash != collective.share_hash:
        return render_template('error.html', message='Link inválido'), 404
    
    return render_template('collective_view.html', collective=collective, user=user)

@main_bp.route('/collective/<int:collective_id>/join')
@login_required
def join_collective(collective_id):
    """Aderir a uma leitura coletiva"""
    user = get_current_user()
    collective = CollectiveReading.query.get_or_404(collective_id)
    
    # Verificar se já está participando
    existing = CollectiveReadingParticipant.query.filter_by(
        collective_reading_id=collective.id,
        user_id=user.id
    ).first()
    
    if existing:
        return redirect(url_for('main.view_collective', collective_id=collective.id))
    
    # Adicionar como participante
    participant = CollectiveReadingParticipant(
        collective_reading_id=collective.id,
        user_id=user.id
    )
    db.session.add(participant)
    db.session.commit()
    
    return redirect(url_for('main.view_collective', collective_id=collective.id))

@main_bp.route('/collective/<int:collective_id>/update-progress', methods=['POST'])
@login_required
def update_collective_progress(collective_id):
    """Atualizar progresso na leitura coletiva (por páginas ou percentual)"""
    user = get_current_user()
    collective = CollectiveReading.query.get_or_404(collective_id)
    
    # Verificar se está participando
    participant = CollectiveReadingParticipant.query.filter_by(
        collective_reading_id=collective.id,
        user_id=user.id
    ).first_or_404()
    
    try:
        from app.models import CollectiveReadingProgress, CollectiveReadingBook
        
        data = request.get_json()
        book_order = data.get('book_order')  # Qual livro está atualizando
        pages_read = data.get('pages_read')  # Páginas lidas deste livro
        percentage_input = data.get('percentage')  # Percentual deste livro
        
        if book_order is None:
            return jsonify({'error': 'book_order é obrigatório'}), 400
        
        # Obter o livro
        book = CollectiveReadingBook.query.filter_by(
            collective_reading_id=collective.id,
            order=book_order
        ).first_or_404()
        
        # Converter percentual em páginas se necessário
        if pages_read is None and percentage_input is not None:
            pages_read = int((float(percentage_input) / 100) * book.total_pages)
        elif pages_read is None:
            return jsonify({'error': 'pages_read ou percentage é obrigatório'}), 400
        
        # Validar páginas
        pages_read = min(max(int(pages_read), 0), book.total_pages)
        
        # Criar ou atualizar registro de progresso para este livro
        progress = CollectiveReadingProgress.query.filter_by(
            collective_reading_id=collective.id,
            user_id=user.id,
            book_order=book_order
        ).first()
        
        if progress is None:
            progress = CollectiveReadingProgress(
                collective_reading_id=collective.id,
                user_id=user.id,
                book_order=book_order,
                pages_read=pages_read
            )
            db.session.add(progress)
        else:
            progress.pages_read = pages_read
        
        db.session.commit()
        
        # Calcular novo percentual geral
        total_pages = sum(b.total_pages for b in collective.books)
        total_pages_read = sum(
            p.pages_read for p in CollectiveReadingProgress.query.filter_by(
                collective_reading_id=collective.id,
                user_id=user.id
            ).all()
        )
        new_percentage = (total_pages_read / total_pages * 100) if total_pages > 0 else 0
        
        # Atualizar percentual geral do participante
        participant.current_percentage = new_percentage
        participant.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'percentage': round(new_percentage, 2),
            'pages_read': pages_read,
            'total_pages': book.total_pages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/collective/<int:collective_id>/progress-data', methods=['GET'])
@login_required
def get_collective_progress_data(collective_id):
    """Obter dados de progresso detalhados para gráfico (todos os participantes)"""
    user = get_current_user()
    collective = CollectiveReading.query.get_or_404(collective_id)
    
    # Verificar se está participando ou é creator (pode ver dados públicos)
    if user.id != collective.creator_id:
        participant = CollectiveReadingParticipant.query.filter_by(
            collective_reading_id=collective.id,
            user_id=user.id
        ).first_or_404()
    
    from app.models import CollectiveReadingProgress
    
    # Obter todos os participantes
    participants_data = []
    
    for participant in collective.participants:
        # Para cada participante, obter progresso em cada livro
        participant_books = []
        total_pages = 0
        total_pages_read = 0
        
        for book in sorted(collective.books, key=lambda b: b.order):
            progress = CollectiveReadingProgress.query.filter_by(
                collective_reading_id=collective.id,
                user_id=participant.user_id,
                book_order=book.order
            ).first()
            
            pages_read = progress.pages_read if progress else 0
            percentage_of_book = (pages_read / book.total_pages * 100) if book.total_pages > 0 else 0
            
            participant_books.append({
                'order': book.order,
                'title': book.title,
                'total_pages': book.total_pages,
                'pages_read': pages_read,
                'percentage_of_book': round(percentage_of_book, 2)
            })
            
            total_pages += book.total_pages
            total_pages_read += pages_read
        
        overall_percentage = (total_pages_read / total_pages * 100) if total_pages > 0 else 0
        
        participants_data.append({
            'username': participant.user.username,
            'user_id': participant.user_id,
            'books': participant_books,
            'total_pages': total_pages,
            'total_pages_read': total_pages_read,
            'overall_percentage': round(overall_percentage, 2)
        })
    
    return jsonify({
        'success': True,
        'participants': participants_data
    }), 200

@main_bp.route('/collective/<int:collective_id>/leave', methods=['POST'])
@login_required
def leave_collective(collective_id):
    """Sair de uma leitura coletiva"""
    user = get_current_user()
    collective = CollectiveReading.query.get_or_404(collective_id)
    
    # Verificar se está participando
    participant = CollectiveReadingParticipant.query.filter_by(
        collective_reading_id=collective.id,
        user_id=user.id
    ).first()
    
    if participant:
        db.session.delete(participant)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Você saiu da leitura coletiva'}), 200
    
    return jsonify({'error': 'Você não está participando desta leitura'}), 400

@main_bp.route('/collective/share/<share_hash>')
def join_collective_by_hash(share_hash):
    """Entrar em leitura coletiva via link compartilhável"""
    collective = CollectiveReading.query.filter_by(share_hash=share_hash).first_or_404()
    
    user = get_current_user() if session.get('user_id') else None
    
    if user:
        # Se logado, redirecionar para view com hash na URL
        return redirect(url_for('main.view_collective', collective_id=collective.id, hash=share_hash))
    else:
        # Se não logado, mostrar página com opção de login/registro
        return render_template('collective_view.html', collective=collective, user=None, share_hash=share_hash)