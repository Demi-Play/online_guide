from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from flask_login import current_user, login_required

from models import Project, db

planer_bp = Blueprint('planer', __name__)

@planer_bp.route('/<int:project_id>', methods=['GET', 'POST'])
@login_required
def index(project_id):
    return render_template('planing/floorplan.html', project_id=project_id)

@planer_bp.route('/view3d/<int:project_id>', methods=['POST'])
@login_required
def view3d(project_id):
    floor_data = request.get_json()
    
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    
    # Расширенная валидация данных
    if not floor_data or 'floor_data' not in floor_data:
        return jsonify({"error": "Некорректные данные планировки"}), 400
    
    try:
        project.floor_data = floor_data
        db.session.commit()
        
        return jsonify({
            "message": "Данные успешно сохранены",
            "redirect_url": url_for('planer.view3d_result', project_id=project.id)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@planer_bp.route('/view3d_result/<int:project_id>', methods=['GET'])
@login_required
def view3d_result(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Проверка прав доступа
    if project.user_id != current_user.id:
        return jsonify({"error": "Доступ запрещен"}), 403
    
    # Загрузка данных из базы с проверкой
    floor_data = project.floor_data or {}
    
    return render_template('planing/3dView.html', 
                           floor_data=floor_data, 
                           project_id=project_id)