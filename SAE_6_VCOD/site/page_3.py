from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from tools import get_all_years,get_regions,Elec, Gaz, Chauffage,IRIS, DEPARTMENTS, db
from collections import defaultdict


page3_bp = Blueprint('page3', __name__)

@page3_bp.route("/page_3")
def page_3():
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

    def get_fournisseur_categorie(model, year, region=None):
        query = db.session.query(
            model.operateur,
            model.code_categorie_consommation,
            db.func.sum(model.conso)
        ).filter(model.annee == year)

        if region:
            query = query.join(IRIS, IRIS.CODE_IRIS == model.iris).join(DEPARTMENTS, DEPARTMENTS.num_dep == IRIS.DEP)
            query = query.filter(DEPARTMENTS.region_name == region)

        query = query.group_by(model.operateur, model.code_categorie_consommation)
        rows = query.all()

        # Regrouper les consommations par opérateur + catégorie
        data = defaultdict(lambda: {"RES": 0, "ENT": 0, "PRO": 0, "ENT_PRO": 0})
        for op, cat, conso in rows:
            if cat in data[op]:
                data[op][cat] += conso

        # Calculer total pour trier
        fournisseurs_total = {
            op: sum(cats.values())
            for op, cats in data.items()
        }

        # Garder les top 5
        top5 = sorted(fournisseurs_total.items(), key=lambda x: x[1], reverse=True)[:5]
        top_data = {op: data[op] for op, _ in top5}

        return top_data
    
    operateur_repartition = get_repartition_operateur(model, year,region)
    if model == Chauffage:
        categorie_repartition = {}
        fournisseur_categorie = {}
    else:
        categorie_repartition = get_repartition_categorie(model, year, region)
        fournisseur_categorie = get_fournisseur_categorie(model, year, region)

    return render_template("page_3.html",
        annees=annees,
        regions=regions,
        region=region,
        year=year,
        conso_type=conso_type,
        operateur_repartition=operateur_repartition,
        categorie_repartition=categorie_repartition,
        fournisseur_categorie=fournisseur_categorie
    )
