from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Project, Rating, Comment
from forms.rating_comment_forms import RatingForm, CommentForm
import statistics


planer_bp = Blueprint('planer', __name__)

@planer_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('planing/floorplan.html')