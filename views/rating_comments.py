from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Project, Rating, Comment
from forms.rating_comment_forms import RatingForm, CommentForm

rating_comment_bp = Blueprint('rating_comments', __name__, template_folder='templates/rating_comments')

@rating_comment_bp.route('/project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    rating_form = RatingForm()
    comment_form = CommentForm()

    # Handle rating submission
    if rating_form.validate_on_submit():
        existing_rating = Rating.query.filter_by(user_id=current_user.id, project_id=project.id).first()
        if existing_rating:
            flash('You have already rated this project!', 'warning')
        else:
            rating = Rating(score=rating_form.score.data, user_id=current_user.id, project_id=project.id)
            db.session.add(rating)
            db.session.commit()
            flash('Your rating has been submitted!', 'success')

    # Handle comment submission
    if comment_form.validate_on_submit():
        comment = Comment(text=comment_form.text.data, user_id=current_user.id, project_id=project.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')

    # Get all comments and ratings for the project
    comments = Comment.query.filter_by(project_id=project.id).all()
    ratings = Rating.query.filter_by(project_id=project.id).all()

    return render_template('rating_comments/project_detail.html', project=project, comments=comments, ratings=ratings, rating_form=rating_form, comment_form=comment_form)
