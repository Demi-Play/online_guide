from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length



class ProjectForm(FlaskForm):
    title = StringField(
        'Title', 
        validators=[DataRequired(), Length(max=100)],
        render_kw={"placeholder": "Название проекта"}
    )
    description = TextAreaField(
        'Description', 
        validators=[DataRequired(), Length(max=500)],
        render_kw={"placeholder": "Описание проекта"}
    )
    submit = SubmitField('Сохранить')