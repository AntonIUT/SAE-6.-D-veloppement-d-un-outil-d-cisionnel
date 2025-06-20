from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from tools import get_all_years,get_regions,Elec, Gaz, Chauffage,IRIS, DEPARTMENTS, db

page4_bp = Blueprint('page4', __name__)

@page4_bp.route("/page_4")
def page_4():
    if 'user_id' not in session:
        flash("Vous devez vous connecter", "warning")
        return redirect(url_for('login'))

    conso_type = request.args.get('conso_type', 'elec')
    year = request.args.get('year', type=int)
    region= request.args.get('region')
    if conso_type == 'elec':
        model = Elec
    elif conso_type == 'gaz':
        model = Gaz
    elif conso_type == 'chauffage':
        model = Chauffage

    annees = get_all_years()
    regions = get_regions()

    
    def get_repartition_operateur(model, year, region):
        query = db.session.query(model.operateur, db.func.sum(model.conso))\
            .join(IRIS, IRIS.CODE_IRIS == model.iris)\
            .join(DEPARTMENTS, DEPARTMENTS.num_dep == IRIS.DEP)

        if year:
            query = query.filter(model.annee == year)
        if region:
            query = query.filter(DEPARTMENTS.region_name == region)

        query = query.group_by(model.operateur)
        rows = query.all()
        return {op: round(conso) for op, conso in rows}


    def get_repartition_categorie(model, year, region):
        query = db.session.query(model.code_categorie_consommation, db.func.sum(model.conso))\
            .join(IRIS, IRIS.CODE_IRIS == model.iris)\
            .join(DEPARTMENTS, DEPARTMENTS.num_dep == IRIS.DEP)

        if year:
            query = query.filter(model.annee == year)
        if region:
            query = query.filter(DEPARTMENTS.region_name == region)

        query = query.group_by(model.code_categorie_consommation)
        rows = query.all()
        return {cat: round(conso) for cat, conso in rows}

    operateur_repartition = get_repartition_operateur(model, year,region)
    categorie_repartition = get_repartition_categorie(model, year,region)

    return render_template("page_4.html",
        annees=annees,
        regions=regions,
        region=region,
        year=year,
        conso_type=conso_type,
        operateur_repartition=operateur_repartition,
        categorie_repartition=categorie_repartition
    )
