import os
from flask import Flask, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy

# --- Configuration des chemins ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')



DB_PATH = os.path.join(DATA_DIR, 'users.sqlite')
NRJ_DB_PATH = os.path.join(DATA_DIR, 'BDD_NRJ.sqlite')

# --- Initialisation de Flask et SQLAlchemy ---
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'nrj': f'sqlite:///{NRJ_DB_PATH}'
}
db = SQLAlchemy(app)

class IRIS(db.Model):
    __bind_key__ = 'nrj'
    __tablename__ = 'IRIS' 
    CODE_IRIS = db.Column(db.String, primary_key=True)  
    DEP = db.Column(db.String) 
class DEPARTMENTS(db.Model):
    __bind_key__ = 'nrj'
    __tablename__ = 'departements'  
    num_dep = db.Column(db.String, primary_key=True)
    nom_dep = db.Column('dep_name',db.String)
       
class Elec(db.Model):
    __bind_key__ = 'nrj'
    __tablename__ = 'table_elec'
    id_db = db.Column(db.Integer, primary_key=True)
    annee = db.Column('ANNEE', db.Integer)
    conso = db.Column('CONSO', db.Float)
    filiere = db.Column('FILIERE', db.String)
    iris = db.Column('IRIS_CODE', db.String)#, db.ForeignKey('IRIS.CODE_IRIS'))

class Gaz(db.Model):
    __bind_key__ = 'nrj'
    __tablename__ = 'table_gaz'
    id_db = db.Column(db.Integer, primary_key=True)
    annee = db.Column('ANNEE', db.Integer)
    conso = db.Column('CONSO', db.Float)
    filiere = db.Column('FILIERE', db.String)
    iris = db.Column('IRIS_CODE', db.String)#, db.ForeignKey('IRIS.CODE_IRIS'))  

class Chauffage(db.Model):
    __bind_key__ = 'nrj'
    __tablename__ = 'table_chaleur'
    id_db = db.Column(db.Integer, primary_key=True)
    annee = db.Column('ANNEE', db.Integer)
    conso = db.Column('CONSO', db.Float)
    filiere = db.Column('FILIERE', db.String)
    iris = db.Column('IRIS_CODE', db.String)# , db.ForeignKey('IRIS.CODE_IRIS'))

def get_all_years():
    elec_years = [y[0] for y in db.session.query(Elec.annee).distinct().all()]
    gaz_years = [y[0] for y in db.session.query(Gaz.annee).distinct().all()]
    chauffage_years = [y[0] for y in db.session.query(Chauffage.annee).distinct().all()]
    annees = sorted(set(elec_years + gaz_years + chauffage_years))
    return annees


@app.route("/page_1")
def page_1():
    if 'user_id' not in session:
        flash("Vous devez vous connecter", "warning")
        return redirect(url_for('login'))

    # Récupérer toutes les années disponibles
    annees = get_all_years()
    year = request.args.get('year')

    consommation = {}
    if year:
        # Convertir l’année pour comparaison
        year_int = int(year)
        # Total conso par table
        elec_conso = db.session.query(db.func.sum(Elec.conso)).filter(Elec.annee == year_int).scalar() or 0
        gaz_conso = db.session.query(db.func.sum(Gaz.conso)).filter(Gaz.annee == year_int).scalar() or 0
        chauffage_conso = db.session.query(db.func.sum(Chauffage.conso)).filter(Chauffage.annee == year_int).scalar() or 0

        consommation = {
            'Électricité': round(elec_conso),
            'Gaz': round(gaz_conso),
            'Chauffage': round(chauffage_conso)
        }

    return render_template("page_1.html", year=year, annees=annees, consommation=consommation)

@app.route("/page_2")
def page_2():
    if 'user_id' not in session:
        flash("Vous devez vous connecter", "warning")
        return redirect(url_for('login'))
    conso_type = request.args.get('conso_type', 'elec')
    if conso_type == 'elec':
        model= Elec
    elif conso_type == 'gaz':
        model= Gaz
    elif conso_type == 'chauffage':
        model= Chauffage
        
    results = db.session.query(
        DEPARTMENTS.nom_dep.label("departement"),
        db.func.sum(model.conso).label("conso")
    ).outerjoin(IRIS, DEPARTMENTS.num_dep == IRIS.DEP) \
     .outerjoin(model, model.iris == IRIS.CODE_IRIS) \
     .group_by(DEPARTMENTS.nom_dep) \
     .all()
    conso_data = {row.departement: round(row.conso or 0)for row in results}
    return render_template("page_2.html", conso_data=conso_data, conso_type=conso_type)



@app.route("/page_3")
def page_3():
    if 'user_id' not in session:
        flash("Vous devez vous connecter", "warning")
        return redirect(url_for('login'))
    
    annees = get_all_years()
    def get_conso_by_year(model):
        rows = db.session.query(model.annee, db.func.sum(model.conso)).group_by(model.annee).all()
        return {int(annee): round(conso) for annee, conso in rows}

    data = {
        "Électricité": get_conso_by_year(Elec),
        "Gaz": get_conso_by_year(Gaz),
        "Chauffage": get_conso_by_year(Chauffage)
    }
    return render_template("page_3.html", data=data, annees=annees)

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
    if 'user_id' in session:
        flash("Vous êtes déjà connecté.", "info")
        return redirect(url_for("page_1"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash("Connexion réussie !", "success")
            session['user_id'] = user.id  # Ajouter l'ID de l'utilisateur dans la session
            session['username'] = user.username 
            return redirect(url_for("page_1"))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect", "danger")
    return render_template("login.html", form=form)

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# --- Création de la base au démarrage ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)





