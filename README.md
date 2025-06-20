# SAE-6.-D-veloppement-d-un-outil-d-cisionnel

https://github.com/AntonIUT/SAE-6.-D-veloppement-d-un-outil-d-cisionnel

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
Il faut pour lancer en manuelle soit ouvrir le dossier SAE_6_VCOD sur votre editeur de code soit ouvrir le cmd puis specifier le chemin où vous avez téléchargé le dossier avec ```cd votrechemin/SAE_6_VCOD```;
Il faut après cela lancer les commandes suivantes dans le terminal.

### 1. Créer l’environnement virtuel 
```py -3 -m venv .venv```
### 2. Activer l’environnement virtuel
```.venv\Scripts\activate```
### 3. Installer les dépendances
```pip install -r site\requirements.txt```
### 4. Générer la base de données (optionnel si déjà fait)
```python csv_to_database.py```
### 5. Lancer l’application Flask
```python site\app.py```

### 6. Aller sur l'application web 
``http://127.0.0.1:5000``
On peut alors creer un compte et naviguer entre les pages, les comptes admin ne sont pas encore inclus dans l'app.

📝 À propos
Base de données SQLite : générée dans site/data/BDD_NRJ.sqlite

Technos : Python 3.9, pandas, Flask, SQLite

Auteurs : BELLANTAN Anton, CHAURAND Lison et BOUKHALF Amin
