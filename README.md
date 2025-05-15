# SAE-6.-D-veloppement-d-un-outil-d-cisionnel

## ▶️ Lancement rapide (Windows)

1. **Ouvre un terminal ou double-clique sur `lancement_appli.bat`** :
   - Crée un environnement virtuel Python si besoin
   - Installe les dépendances
   - Te demande si tu veux générer la base de données
   - Lance l'application Flask
   - Ouvre automatiquement le navigateur à `http://127.0.0.1:5000/`

2. ✅ Suis les instructions affichées dans le terminal

---

## ⚙️ Installation manuelle (si besoin)

### 1. Créer l’environnement virtuel 
```py -3 -m venv .venv```
### 2. Activer l’environnement virtuel
```.venv\Scripts\activate```
### 3. Générer la base de données (optionnel si déjà fait)
```python csv_todatabase.py```
### 4. Installer les dépendances
```pip install -r site\requirements.txt```
### 5. Lancer l’application Flask
python site\app.py

📝 À propos
Base de données SQLite : générée dans site/data/BDD_NRJ.sqlite

Technos : Python 3.9, pandas, Flask, SQLite