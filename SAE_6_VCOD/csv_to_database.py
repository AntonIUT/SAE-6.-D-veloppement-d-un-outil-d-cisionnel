import pandas as pd
import os
from pathlib import Path
import sqlite3  # ✅ nécessaire

# Spécifiez le chemin des dossiers contenant les fichiers CSV

script_dir = Path(__file__).resolve().parent

print(script_dir)
dossiers = {
    'gaz': f'{script_dir}/DATA/gaz',
    'elec': f'{script_dir}/DATA/elec',
    'chaleur': f'{script_dir}/DATA/chaleur'
}

dataframes_par_energie = {}

# Chargement des fichiers CSV dans des DataFrames
for energie, dossier in dossiers.items():
    fichiers_csv = [f for f in os.listdir(dossier) if f.endswith('.csv')]
    dataframes = []
    for fichier in fichiers_csv:
        try:
            df = pd.read_csv(os.path.join(dossier, fichier), sep=';', encoding='utf-8', header=1)
            #Nettoyage
            if {'CONSO', 'PDL'}.issubset(df.columns):
                df = df[~((df['CONSO'] == 'secret') & (df['PDL'] == 'secret'))]
                df = df.dropna(subset=['CONSO', 'PDL'])
                df = df[(df['CONSO'] != '') & (df['PDL'] != '')]
            df.drop(columns=["ID","IRIS"], errors="ignore", inplace=True)

            dataframes.append(df)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {fichier}: {e}")
    

    
    df_concat = pd.concat(dataframes, ignore_index=True)
    df_concat.insert(0, 'id_db', range(1, len(df_concat) + 1))  # Ajout d'une colonne id
    dataframes_par_energie[energie] = df_concat

df_iris=pd.read_excel(f'{script_dir}/DATA/reference_IRIS_geo2024.xlsx', sheet_name='Emboitements_IRIS', header=5)   
df_dep=pd.read_csv(f'{script_dir}/DATA/departements-region.csv', sep=',', encoding='utf-8', header=0)

conn = sqlite3.connect(f'{script_dir}/site/data/BDD_NRJ.sqlite')

df_iris.to_sql('IRIS', conn, if_exists='replace', index=False)  
df_dep.to_sql('departements', conn, if_exists='replace', index=False)

#  Sauvegarde des DataFrames dans des tables
for energie, df in dataframes_par_energie.items():
    nom_table = f"table_{energie}"
    df.to_sql(nom_table, conn, if_exists='replace', index=False)

conn.close()
print("Base SQLite créée avec succès.")
