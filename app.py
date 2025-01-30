from flask import Flask, render_template
from config import Config
from models import Project, db, bcrypt, User
from views.auth import auth_bp
from views.profile import profile_bp
from flask_login import LoginManager
from views.projects import projects_bp
from views.planer import planer_bp
from views.calc import calculator_bp
from views.rating_comments import rating_comment_bp 

app = Flask(__name__, static_folder='./static')
app.config.from_object(Config)

# Инициализация расширений
db.init_app(app)
bcrypt.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Пользовательская загрузка
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Регистрация Blueprint
app.register_blueprint(auth_bp, url_prefix='/auth') 
app.register_blueprint(profile_bp, url_prefix='/profile') 
app.register_blueprint(projects_bp, url_prefix='/projects')
app.register_blueprint(rating_comment_bp, url_prefix='/project')
app.register_blueprint(planer_bp, url_prefix='/planer')
app.register_blueprint(calculator_bp, url_prefix='/calc')


@app.route('/')
def home():
    projects = Project.query.all()
    return render_template('home.html', projects=projects)

@app.route('/news')
def index():
    return render_template('news.html')

# Команда для создания базы данных
@app.cli.command("create-db")
def create_db():
    db.create_all()
    print("База данных создана!")
    

if __name__ == '__main__':
    app.run(debug=True)
    # with app.app_context():
        # create_db()
        
