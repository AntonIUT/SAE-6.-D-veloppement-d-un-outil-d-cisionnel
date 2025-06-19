from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from tools import get_all_years,Elec, Gaz, Chauffage, db

page3_bp = Blueprint('page3', __name__)

@page3_bp.route("/page_3")
def page_3():
    if 'user_id' not in session:
        flash("Vous devez vous connecter", "warning")
        return redirect(url_for('login'))

    conso_type = request.args.get('conso_type', 'elec')
    year = request.args.get('year', type=int)

    if conso_type == 'elec':
        model = Elec
    elif conso_type == 'gaz':
        model = Gaz
    elif conso_type == 'chauffage':
        model = Chauffage

    annees = get_all_years()

    def get_conso_by_year(model):
        rows = db.session.query(model.annee, db.func.sum(model.conso)).group_by(model.annee).all()
        return {int(annee): round(conso) for annee, conso in rows}

    def get_repartition_operateur(model, year):
        query = db.session.query(model.operateur, db.func.sum(model.conso)).group_by(model.operateur)
        if year:
            query = query.filter(model.annee == year)
        rows = query.all()
        return {op: round(conso) for op, conso in rows}

    def get_repartition_categorie(model, year):
        query = db.session.query(model.code_categorie_consommation, db.func.sum(model.conso)).group_by(model.code_categorie_consommation)
        if year:
            query = query.filter(model.annee == year)
        rows = query.all()
        return {cat: round(conso) for cat, conso in rows}

    consommation = {
        "Électricité": get_conso_by_year(Elec),
        "Gaz": get_conso_by_year(Gaz),
        "Chauffage": get_conso_by_year(Chauffage)
    }

    operateur_repartition = get_repartition_operateur(model, year)
    categorie_repartition = get_repartition_categorie(model, year)

    return render_template("page_3.html",
        consommation=consommation,
        annees=annees,
        year=year,
        conso_type=conso_type,
        operateur_repartition=operateur_repartition,
        categorie_repartition=categorie_repartition
    )
