from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class CalculatorForm(FlaskForm):
    room_length = IntegerField('Длина комнаты (м)', validators=[DataRequired()])
    room_width = IntegerField('Ширина комнаты (м)', validators=[DataRequired()])
    
    materials = SelectField('Материалы', choices=[
        ('paint', 'Краска'),
        ('tiles', 'Плитка'),
        ('laminate', 'Ламинат')
    ], validators=[DataRequired()])
    
    work_type = SelectField('Тип работ', choices=[
        ('simple', 'Простой ремонт'),
        ('complex', 'Сложный ремонт')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Рассчитать стоимость')
