from flask import Blueprint, render_template, request, redirect, url_for
from forms.calc_form import CalculatorForm

calculator_bp = Blueprint('calculator', __name__)

@calculator_bp.route('/', methods=['GET', 'POST'])
def index():
    form = CalculatorForm()
    
    if form.validate_on_submit():
        room_length = form.room_length.data
        room_width = form.room_width.data
        material = form.materials.data
        work_type = form.work_type.data
        
        # Расчет стоимости
        area = room_length * room_width
        if material == 'paint':
            material_cost = area * 500
        elif material == 'tiles':
            material_cost = area * 1000
        elif material == 'laminate':
            material_cost = area * 800
        
        if work_type == 'simple':
            work_cost = area * 200
        elif work_type == 'complex':
            work_cost = area * 500
        
        total_cost = material_cost + work_cost
        
        result = [
            {'name': 'Материалы', 'cost': material_cost},
            {'name': 'Работы', 'cost': work_cost}
        ]
        
        return render_template('calc/calculator.html', calculator_form=form, result=result, total_cost=total_cost)
    
    return render_template('calc/calculator.html', calculator_form=form)

