from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user
from forms.auth_forms import RegistrationForm, LoginForm
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Проверяем, существует ли пользователь
        if User.query.filter_by(email=form.email.data).first():
            flash('Email is already registered.', 'danger')
            return redirect(url_for('auth.register'))

        # Создаем нового пользователя
        new_user = User(
            username=form.username.data,
            email=form.email.data,
        )
        new_user.password = form.password.data  # Хэшируем пароль
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # Логика успешного входа
            login_user(user=user)
            flash('Login successful!', 'success')
            return redirect(url_for('profile.view_profile'))
        flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
