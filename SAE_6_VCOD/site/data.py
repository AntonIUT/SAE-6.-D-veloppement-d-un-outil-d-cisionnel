from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from tools import get_all_years, get_regions, Elec, Gaz, Chauffage, IRIS, DEPARTMENTS, db

data_bp = Blueprint('data_', __name__)

@data_bp.route('/data')
def data():
    if 'user_id' not in session:
        flash("Vous devez vous connecter", "warning")
        return redirect(url_for('auth.login'))

    annees = get_all_years()
    regions = get_regions()
    year = request.args.get('year', type=int, default=max(annees))
    region = request.args.get('region')
    conso_type = request.args.get('conso_type', 'elec')

    model = Elec if conso_type == 'elec' else Gaz if conso_type == 'gaz' else Chauffage

    query = db.session.query(model).filter(model.annee == year)
    if region:
        query = query.join(IRIS, IRIS.CODE_IRIS == model.iris)\
                     .join(DEPARTMENTS, DEPARTMENTS.num_dep == IRIS.DEP)\
                     .filter(DEPARTMENTS.region_name == region)

    rows = query.limit(200).all()  # limit pour ne pas tout charger
    donnees = [r.__dict__ for r in rows]
    for d in donnees:
        d.pop('_sa_instance_state', None)

    return render_template(
        'data.html',
        annees=annees,
        regions=regions,
        year=year,
        region=region,
        conso_type=conso_type,
        donnees=donnees
    )
