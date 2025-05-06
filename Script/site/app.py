import os
from flask import Flask, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy

# --- Configuration des chemins ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DB_PATH = os.path.join(DATA_DIR, 'users.sqlite')

# --- Initialisation de Flask et SQLAlchemy ---
app = Flask(__name__)
app.secret_key = "your_secret_key"  # À changer pour la prod
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Modèle utilisateur ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# --- Formulaires ---
class RegisterForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Mot de passe", validators=[InputRequired(), Length(min=6, max=20)])

class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Mot de passe", validators=[InputRequired(), Length(min=6, max=20)])

# --- Routes ---
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash("Nom d'utilisateur déjà pris", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Inscription réussie ! Vous pouvez vous connecter.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash("Connexion réussie !", "success")
            session['user_id'] = user.id  # Ajouter l'ID de l'utilisateur dans la session
            session['username'] = user.username 
            return redirect(url_for("accueil"))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect", "danger")
    return render_template("login.html", form=form)

@app.route("/accueil")
def accueil():
    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        flash("Vous devez vous connecter pour accéder à l'accueil", "warning")
        return redirect(url_for('login'))
    return render_template("accueil.html")

@app.route("/logout")
def logout():
    # Supprime toutes les données de session (utilisateur et messages flash)
    session.clear()
    # Tu peux aussi effacer les messages flash ici si tu veux être plus explicite.
    flash("Vous êtes maintenant déconnecté.", "info")
    return redirect(url_for('login'))

@app.route("/")
def home():
    return redirect(url_for("login"))

# --- Création de la base au démarrage ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
