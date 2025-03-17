from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.secret_key = "your_secret_key"  # À ne pas exposer en production

# Dictionnaire simulant une base de données pour les utilisateurs
users_db = {}

# Formulaire d'inscription
class RegisterForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=6, max=20)])

# Formulaire de connexion
class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=6, max=20)])

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Vérifier si l'utilisateur existe déjà
        if username in users_db:
            flash("Nom d'utilisateur déjà pris", "danger")
            return redirect(url_for("register"))

        # Hachage du mot de passe
        hashed_password = generate_password_hash(password, method='sha256')

        # Ajouter l'utilisateur à notre "base de données"
        users_db[username] = hashed_password
        flash("Inscription réussie ! Vous pouvez vous connecter.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Vérifier si l'utilisateur existe
        if username in users_db:
            # Vérifier si le mot de passe est correct
            if check_password_hash(users_db[username], password):
                flash("Connexion réussie !", "success")
                return redirect(url_for("welcome"))
            else:
                flash("Mot de passe incorrect", "danger")
        else:
            flash("Nom d'utilisateur introuvable", "danger")

    return render_template("login.html", form=form)

@app.route("/welcome")
def welcome():
    return "Bienvenue sur votre espace personnel !"

if __name__ == "__main__":
    app.run(debug=True)
