# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

db = SQLAlchemy()

class IRIS(db.Model):
    __bind_key__ = 'nrj'
    __tablename__ = 'IRIS'
    CODE_IRIS = db.Column(db.String, primary_key=True)
    DEP = db.Column(db.String)

class DEPARTMENTS(db.Model):
    __bind_key__ = 'nrj'
    __tablename__ = 'departements'
    num_dep = db.Column(db.String, primary_key=True)
    nom_dep = db.Column('dep_name', db.String)
    region_name = db.Column('region_name', db.String)

class Elec(db.Model):
    __bind_key__ = 'nrj'
    __tablename__ = 'table_elec'  # ⚠️ assure-toi que ce nom est exact dans ta base SQLite
    id_db = db.Column(db.Integer, primary_key=True)
    annee = db.Column('ANNEE', db.Integer)
    conso = db.Column('CONSO', db.Float)
    filiere = db.Column('FILIERE', db.String)
    iris = db.Column('IRIS_CODE', db.String)
    operateur = db.Column('OPERATEUR', db.String)
    code_categorie_consommation = db.Column('CODE_CATEGORIE_CONSOMMATION', db.String)
    code_grand_secteur= db.Column('CODE_GRAND_SECTEUR', db.String)

class Gaz(db.Model):
    __bind_key__ = 'nrj'
    __tablename__ = 'table_gaz'
    id_db = db.Column(db.Integer, primary_key=True)
    annee = db.Column('ANNEE', db.Integer)
    conso = db.Column('CONSO', db.Float)
    filiere = db.Column('FILIERE', db.String)
    iris = db.Column('IRIS_CODE', db.String)
    operateur = db.Column('OPERATEUR', db.String)
    code_categorie_consommation = db.Column('CODE_CATEGORIE_CONSOMMATION', db.String)
    code_grand_secteur= db.Column('CODE_GRAND_SECTEUR', db.String)

class Chauffage(db.Model):
    __bind_key__ = 'nrj'
    __tablename__ = 'table_chaleur'
    id_db = db.Column(db.Integer, primary_key=True)
    annee = db.Column('ANNEE', db.Integer)
    conso = db.Column('CONSO', db.Float)
    filiere = db.Column('FILIERE', db.String)
    iris = db.Column('IRIS_CODE', db.String)
    operateur = db.Column('OPERATEUR', db.String)
    code_categorie_consommation = db.Column('CODE_CATEGORIE_CONSOMMATION', db.String)
    code_grand_secteur= db.Column('CODE_GRAND_SECTEUR', db.String)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role=db.Column(db.String(200), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Mot de passe", validators=[InputRequired(), Length(min=6, max=20)])

class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Mot de passe", validators=[InputRequired(), Length(min=6, max=20)])


def get_all_years():
    elec_years = [y[0] for y in db.session.query(Elec.annee).distinct()]
    gaz_years = [y[0] for y in db.session.query(Gaz.annee).distinct()]
    chauffage_years = [y[0] for y in db.session.query(Chauffage.annee).distinct()]
    return sorted(set(elec_years + gaz_years + chauffage_years))
def get_regions():
    regions = db.session.query(DEPARTMENTS.region_name).distinct().all()
    return [region[0] for region in regions]