from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from tools import get_all_years, Elec, Gaz, Chauffage, db

page1_bp = Blueprint('page1', __name__)

@page1_bp.route("/page_1")
def page_1():
    if 'user_id' not in session:
        flash("Vous devez vous connecter", "warning")
        return redirect(url_for('auth.login'))

    annees = sorted(get_all_years())
    year = request.args.get('year', type=int)

    def get_conso_by_year(model):
        rows = db.session.query(model.annee, db.func.sum(model.conso)).group_by(model.annee).all()
        return {int(annee): round(conso) for annee, conso in rows}

    consommation = {
        "Électricité": get_conso_by_year(Elec),
        "Gaz": get_conso_by_year(Gaz),
        "Chauffage": get_conso_by_year(Chauffage)
    }

    # Calculer les KPIs
    def variation_annuelle(conso_dict, year):
        if year - 1 in conso_dict and year in conso_dict:
            return round(((conso_dict[year] - conso_dict[year - 1]) / conso_dict[year - 1]) * 100, 2)
        else:
            return None

    year = request.args.get('year', type=int, default=max(annees))

    kpis = {}
    for energie, data in consommation.items():
        kpis[energie] = {
            "variation_annuelle": variation_annuelle(data, year),
            "moyenne_annuelle": round(sum(data.values()) / len(data)),
            "pic_conso_annee": max(data, key=data.get),
            "evolution_totale": round(((data[max(data)] - data[min(data)]) / data[min(data)]) * 100, 2)
        }

    return render_template("page_1.html", annees=annees, consommation=consommation, kpis=kpis, year=year,page="page_1.html")
