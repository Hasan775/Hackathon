from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
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

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trail = db.Column(db.String(100), nullable=False)  # e.g., 'Laza-Kuzun'
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='comments')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------------
# ROUTES
# ---------------------
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
    return redirect(url_for('main'))

# ---------------------
# Hiking pages
# ---------------------
@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/Laza-Kuzun', methods=['GET', 'POST'])
def laza_kuzun():
    if request.method == "POST":
        content = request.form['content']
        if content.strip():  # ignore empty comments
            comment = Comment(content=content, user_id=current_user.id, trail='Laza-Kuzun')
            db.session.add(comment)
            db.session.commit()
        return redirect(url_for('laza_kuzun'))

    comments = Comment.query.filter_by(trail='Laza-Kuzun').order_by(Comment.timestamp.desc()).all()
    return render_template('Laza-Kuzun.html', comments=comments)

@app.route('/Shahdag', methods=['GET', 'POST'])
def shahdag():
    if request.method == "POST":
        if current_user.is_authenticated:
            content = request.form['content']
            if content.strip():
                comment = Comment(content=content, user_id=current_user.id, trail='Shahdag')
                db.session.add(comment)
                db.session.commit()
        return redirect(url_for('shahdag'))

    comments = Comment.query.filter_by(trail='Shahdag').order_by(Comment.timestamp.desc()).all()
    return render_template('Shahdag.html', comments=comments)

@app.route('/Xinaliq', methods=['GET', 'POST'])
def xinaliq():
    if request.method == "POST":
        if current_user.is_authenticated:
            content = request.form['content']
            if content.strip():
                comment = Comment(content=content, user_id=current_user.id, trail='Xinaliq')
                db.session.add(comment)
                db.session.commit()
        return redirect(url_for('xinaliq'))

    comments = Comment.query.filter_by(trail='Xinaliq').order_by(Comment.timestamp.desc()).all()
    return render_template('Xinaliq.html', comments=comments)

@app.route('/Transcaucas', methods=['GET', 'POST'])
def transcaucas():
    if request.method == "POST":
        if current_user.is_authenticated:
            content = request.form['content']
            if content.strip():
                comment = Comment(content=content, user_id=current_user.id, trail='Transcaucas')
                db.session.add(comment)
                db.session.commit()
        return redirect(url_for('transcaucas'))

    comments = Comment.query.filter_by(trail='Transcaucas').order_by(Comment.timestamp.desc()).all()
    return render_template('Transcaucas.html', comments=comments)

# ---------------------
# START
# ---------------------
if __name__ == "__main__":
    if not os.path.exists("users.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
