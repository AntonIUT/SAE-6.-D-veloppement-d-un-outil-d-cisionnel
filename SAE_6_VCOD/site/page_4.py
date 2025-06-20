from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from tools import get_all_years,get_regions,Elec, Gaz, Chauffage,IRIS, DEPARTMENTS, db

page4_bp = Blueprint('page4', __name__)

@page4_bp.route("/page_4")
def page_4():
    if 'user_id' not in session:
        flash("Vous devez vous connecter", "warning")
        return redirect(url_for('login'))
    annees = get_all_years()
    regions = get_regions()
    conso_type = request.args.get('conso_type', 'elec')
    year = request.args.get('year', type=int, default=max(annees))
    region= request.args.get('region')
    if conso_type == 'elec':
        model = Elec
    elif conso_type == 'gaz':
        model = Gaz
    elif conso_type == 'chauffage':
        model = Chauffage



    
    def get_repartition_secteur(model, year, region=None):
        query = db.session.query(
            model.code_grand_secteur,
            db.func.sum(model.conso)
        ).filter(model.annee == year)

        if region:
            query = query.join(IRIS, IRIS.CODE_IRIS == model.iris).join(DEPARTMENTS, DEPARTMENTS.num_dep == IRIS.DEP)
            query = query.filter(DEPARTMENTS.region_name == region)

        query = query.group_by(model.code_grand_secteur)
        rows = query.all()

        secteur_labels = {
            "A": "Agriculture",
            "I": "Industrie",
            "T": "Tertiaire",
            "R": "Résidentiel",
            "X": "Non affecté"
        }

        return {
            secteur_labels.get(code, code): round(conso)
            for code, conso in rows
        }

    repartition_secteur = get_repartition_secteur(model, year, region)
    return render_template("page_4.html", conso_type=conso_type, annees=annees, year=year, repartition_secteur=repartition_secteur)
