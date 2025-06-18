@echo off
cd /d %~dp0

echo [1/5] Creation de l'environnement virtuel 

REM Verifie si l'environnement virtuel existe deja
if not exist ".venv\" (
    py -3 -m venv .venv
    echo Environnement virtuel cree avec succes.
) else (
    echo L'environnement virtuel existe deja.
)

echo [2/5] Activation de l'environnement...
call .venv\Scripts\activate

echo [3/5] Installation des dependances...
pip install -r site\requirements.txt


echo [4/5] Voulez-vous creer la base de donnees ?
set /p USER_INPUT="(o/n) : "

if /i "%USER_INPUT%"=="o" (
    echo Creation de la base de donnees...
    python csv_to_database.py
)


echo [5/5] Lancement de l'application...
start http://127.0.0.1:5000/
python site\app.py

pause
