from flask import Flask, redirect, url_for, render_template
from tools import db
from page_1 import page1_bp
from page_2 import page2_bp
from page_3 import page3_bp
from page_4 import page4_bp
from log import auth
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'users.sqlite')
NRJ_DB_PATH = os.path.join(DATA_DIR, 'BDD_NRJ.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_BINDS'] = {'nrj': f'sqlite:///{NRJ_DB_PATH}'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(page1_bp)
app.register_blueprint(page2_bp)
app.register_blueprint(page3_bp)
app.register_blueprint(page4_bp)
app.register_blueprint(auth)

@app.route("/")
def home():
    return redirect(url_for("auth.login"))

@app.route("/accueil")
def accueil():
    return render_template("accueil.html", page="accueil.html")

@app.route("/data")
def data():
    return render_template("data.html", page="data.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
