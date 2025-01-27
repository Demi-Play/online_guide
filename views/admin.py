from flask import Blueprint, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from models import db, User, Project, Rating, Comment

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Создание административной панели
admin = Admin(name='Admin Panel', template_mode='bootstrap3')

class AdminModelView(ModelView):
    def is_accessible(self):
        # Проверяем, что пользователь администратор
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Project, db.session))
admin.add_view(AdminModelView(Rating, db.session))
admin.add_view(AdminModelView(Comment, db.session))

# Регистрация административной панели в приложении
@admin_bp.route('/')
@login_required
def index():
    return admin.index()
