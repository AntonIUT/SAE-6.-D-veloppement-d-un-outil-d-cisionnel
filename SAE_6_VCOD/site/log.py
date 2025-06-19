from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from tools import LoginForm, RegisterForm,User, db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        flash("Déjà connecté", "info")
        return redirect(url_for("accueil"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Connecté", "success")
            return redirect(url_for("accueil"))
        flash("Identifiants incorrects", "danger")
    return render_template("login.html", form=form)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Nom d'utilisateur déjà pris", "danger")
            return redirect(url_for("auth.register"))
        hashed = generate_password_hash(form.password.data)
        db.session.add(User(username=form.username.data, password=hashed))
        db.session.commit()
        flash("Inscription réussie", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth.route("/logout")
def logout():
    session.clear()
    flash("Déconnecté", "info")
    return redirect(url_for("auth.login"))
