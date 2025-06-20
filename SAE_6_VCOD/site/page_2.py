from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from tools import get_all_years, Elec, Gaz, Chauffage, IRIS, DEPARTMENTS, db

page2_bp = Blueprint('page2', __name__)

@page2_bp.route("/page_2")
def page_2():
    if 'user_id' not in session:
        flash("Vous devez vous connecter", "warning")
        return redirect(url_for('auth.login'))
    annees = get_all_years()
    conso_type = request.args.get('conso_type', 'elec')
    year = request.args.get('year', type=int, default=max(annees))

    model = Elec if conso_type == 'elec' else Gaz if conso_type == 'gaz' else Chauffage

    subquery = db.session.query(
        model.iris.label('iris'),
        db.func.sum(model.conso).label('conso')
    )
    if year:
        subquery = subquery.filter(model.annee == year)
    subquery = subquery.group_by(model.iris).subquery()

    results = db.session.query(
        DEPARTMENTS.nom_dep.label("departement"),
        db.func.sum(subquery.c.conso).label("conso")
    ).outerjoin(IRIS, DEPARTMENTS.num_dep == IRIS.DEP)\
     .outerjoin(subquery, subquery.c.iris == IRIS.CODE_IRIS)\
     .group_by(DEPARTMENTS.nom_dep).all()

    consommation = {row.departement: round(row.conso or 0) for row in results}

    return render_template("page_2.html", consommation=consommation, conso_type=conso_type, annees=annees, year=year,page="page_2.html")
