from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from tools import get_all_years,Elec, Gaz, Chauffage, db

page1_bp = Blueprint('page1', __name__)

@page1_bp.route("/page_1")
def page_1():
    if 'user_id' not in session:
        flash("Vous devez vous connecter", "warning")
        return redirect(url_for('auth.login'))

    annees = get_all_years()
    year = request.args.get('year', type=int)
    consommation = {}

    if year:
        elec = db.session.query(db.func.sum(Elec.conso)).filter(Elec.annee == year).scalar() or 0
        gaz = db.session.query(db.func.sum(Gaz.conso)).filter(Gaz.annee == year).scalar() or 0
        chauffage = db.session.query(db.func.sum(Chauffage.conso)).filter(Chauffage.annee == year).scalar() or 0
        consommation = {'Électricité': round(elec), 'Gaz': round(gaz), 'Chauffage': round(chauffage)}

    return render_template("page_1.html", year=year, annees=annees, consommation=consommation)
