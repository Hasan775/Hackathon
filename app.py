from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------------
# MODELS
# ---------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------------
# ROUTES
# ---------------------
@app.route('/')
def index():
    return "Главная страница. <a href='/profile'>Профиль</a> | <a href='/login'>Войти</a> | <a href='/register'>Регистрация</a>"  # create index.html in templates

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return "Такой email уже зарегистрирован"

        hashed = generate_password_hash(password)
        new_user = User(email=email, password=hashed)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return "Неверные данные"

        login_user(user)
        return redirect(url_for('main'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ---------------------
# Hiking pages
# ---------------------
@app.route('/Main')
@login_required
def main():
    return render_template('Main.html')

@app.route('/Laza-Kuzun')
@login_required
def laza_kuzun():
    return render_template('Laza-Kuzun.html')

@app.route('/Shahdag')
@login_required
def shahdag():
    return render_template('Shahdag.html')

@app.route('/Xinaliq')
@login_required
def xinaliq():
    return render_template('Xinaliq.html')

@app.route('/Transcaucas')
@login_required
def transcaucas():
    return render_template('Transcaucas.html')

# ---------------------
# START
# ---------------------
if __name__ == "__main__":
    if not os.path.exists("users.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
