from flask import Blueprint, render_template
from flask_login import current_user, login_required

from models import Project

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/')
@login_required
def view_profile():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    
    return render_template('profile.html', projects=projects)
