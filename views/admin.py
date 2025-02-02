from functools import wraps
from flask import Blueprint, redirect, render_template, url_for, request, flash
from flask_login import current_user, login_required
from models import db, User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.role == 'admin':
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('admin.html', users=users)

@admin_bp.route('/add_user', methods=['GET', 'POST'])
@admin_required
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        new_user = User(username=username, email=email)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        
        flash('Пользователь успешно добавлен!', 'success')
        return redirect(url_for('admin.index'))

    return render_template('add_user.html')  # Создайте этот шаблон для добавления пользователя

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        
        # Обновляем роль пользователя
        role = request.form.get('role')
        user.role = role  # Устанавливаем роль в зависимости от выбора
        
        db.session.commit()
        
        flash('Данные пользователя успешно обновлены!', 'success')
        return redirect(url_for('admin.index'))

    return render_template('edit_user.html', user=user)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@admin_required
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Пользователь успешно удален!', 'success')
    return redirect(url_for('admin.index'))
