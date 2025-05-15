@chcp 65001 >nul
@echo off
cd /d %~dp0

echo [1/5] Creation de l'environnement virtuel 

REM Vérifie si l'environnement virtuel existe déjà
if not exist ".venv\" (
    py -3 -m venv .venv
    echo Environnement virtuel créé avec succès.
) else (
    echo L'environnement virtuel existe déjà.
)

echo [2/5] Activation de l'environnement...
call .venv\Scripts\activate

echo [3/5] Installation des dépendances...
pip install -r site\requirements.txt


echo [4/5] Voulez-vous créer la base de données ?
set /p USER_INPUT="(o/n) : "

if /i "%USER_INPUT%"=="o" (
    echo Création de la base de données...
    python csv_to_database.py
)


echo [5/5] Lancement de l'application...
start http://127.0.0.1:5000/
python site\app.py

pause
