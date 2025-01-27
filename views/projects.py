from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Project
from forms.project_forms import ProjectForm

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
@login_required
def list_projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('projects/list.html', projects=projects)

@projects_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        new_project = Project(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/form.html', form=form, title="Create Project")

@projects_bp.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/form.html', form=form, title="Edit Project")

@projects_bp.route('/projects/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'info')
    return redirect(url_for('projects.list_projects'))
