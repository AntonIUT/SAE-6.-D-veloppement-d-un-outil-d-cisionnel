import pandas as pd
import os
import sqlite3  # ✅ nécessaire

# Spécifiez le chemin des dossiers contenant les fichiers CSV
gaz = 'DATA/gaz'
elec = 'DATA/elec'
chaleur = 'DATA/chaleur'

dossiers = {
    'gaz': gaz,
    'elec': elec,
    'chaleur': chaleur
}

dataframes_par_energie = {}

# Chargement des fichiers CSV dans des DataFrames
for energie, dossier in dossiers.items():
    fichiers_csv = [f for f in os.listdir(dossier) if f.endswith('.csv')]
    dataframes = []
    for fichier in fichiers_csv:
        try:
            df = pd.read_csv(os.path.join(dossier, fichier), sep=';', encoding='utf-8', header=1)
            dataframes.append(df)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {fichier}: {e}")
    dataframes_par_energie[energie] = pd.concat(dataframes, ignore_index=True)

# ✅ Connexion à une vraie base SQLite
conn = sqlite3.connect('Script/site/BDD_NRJ.sqlite')

# ✅ Sauvegarde des DataFrames dans des tables
for energie, df in dataframes_par_energie.items():
    nom_table = f"table_{energie}"
    df.to_sql(nom_table, conn, if_exists='replace', index=False)

conn.close()
print("Base SQLite créée avec succès.")
