import os
import pandas as pd

# Dossier de sortie
output_dir = "FICHIERS_NETTOYES"
output_file = os.path.join(output_dir, "fichiers_chaleurs_nettoyes.csv")

# Vérifier et créer le dossier de sortie si nécessaire
os.makedirs(output_dir, exist_ok=True)

# Liste des chemins des fichiers
fichiers_chaleur = [
    "DATA\\chaleur\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-chaleur-et-f.2018.csv",
    "DATA\\chaleur\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-chaleur-et-f.2019.csv",
    "DATA\\chaleur\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-chaleur-et-f.2020.csv",
    "DATA\\chaleur\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-chaleur-et-f.2021.csv",
    "DATA\\chaleur\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-chaleur-et-f.2022.csv",
    "DATA\\chaleur\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-chaleur-et-f.2023.csv"
]
# Liste pour stocker les DataFrames
dfs = []


# Traitement de chaque fichier
for fichier in fichiers_chaleur:
    if not os.path.exists(fichier):
        continue

    # Charger le fichier CSV avec gestion d'encodage
    try:
        df = pd.read_csv(fichier, encoding="utf-8-sig", skiprows=1, sep=";", quotechar='"')
    except UnicodeDecodeError:
        df = pd.read_csv(fichier, encoding="latin1", skiprows=1, sep=";", quotechar='"')

    # Supprimer explicitement la première ligne si elle existe
    df = df.drop(index=0, errors='ignore')


    # Supprimer les lignes avec valeurs 'secret' ou nulles
    if {'CONSO', 'PDL'}.issubset(df.columns):
        df = df[~((df['CONSO'] == 'secret') & (df['PDL'] == 'secret'))]
        df = df.dropna(subset=['CONSO', 'PDL'])
        df = df[(df['CONSO'] != '') & (df['PDL'] != '')]

    # Supprimer colonnes inutiles
    df.drop(columns=["ID","IRIS"], errors="ignore", inplace=True)


    # Ajouter à la liste
    dfs.append(df)

# Fusion finale
if dfs:
    df_final = pd.concat(dfs, ignore_index=True)
    df_final.to_csv(output_file, index=False, encoding="utf-8-sig", sep=";")
