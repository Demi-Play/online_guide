from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RatingForm(FlaskForm):
    score = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)], render_kw={"placeholder": "Rate the project (1-5)"})
    submit = SubmitField('Submit Rating')

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()], render_kw={"placeholder": "Leave a comment"})
    submit = SubmitField('Post Comment')
