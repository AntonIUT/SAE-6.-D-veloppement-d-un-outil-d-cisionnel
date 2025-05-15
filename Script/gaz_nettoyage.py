import os
import pandas as pd

# Dossier de sortie
output_dir = "FICHIERS_NETTOYES"
output_file = os.path.join(output_dir, "fichiers_gaz_nettoyes.csv")

# Vérifier et créer le dossier de sortie si nécessaire
os.makedirs(output_dir, exist_ok=True)

# Liste des fichiers d'électricité
fichiers_gaz = [
    "DATA\\gaz\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-gaz-naturel-.2018.csv",
    "DATA\\gaz\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-gaz-naturel-.2019.csv",
    "DATA\\gaz\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-gaz-naturel-.2020.csv",
    "DATA\\gaz\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-gaz-naturel-.2021.csv",
    "DATA\\gaz\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-gaz-naturel-.2022.csv",
    "DATA\\gaz\\Donnees-de-consommation-et-de-points-de-livraison-denergie-a-la-maille-IRIS-gaz-naturel-.2023.csv"]
# Liste pour stocker les DataFrames
dfs = []


# Traitement de chaque fichier
for fichier in fichiers_gaz:
    if not os.path.exists(fichier):
        continue

    # Charger le fichier CSV avec gestion d'encodage
    try:
        df = pd.read_csv(fichier, encoding="utf-8-sig", skiprows=1, sep=";", quotechar='"')
    except UnicodeDecodeError:
        df = pd.read_csv(fichier, encoding="latin1", skiprows=1, sep=";", quotechar='"')

    # Supprimer explicitement la première ligne si elle existe
    df = df.drop(index=0, errors='ignore')

    # Harmonisation des noms de colonnes
    if 'CODE_SECTEUR_NAF2_CODE' in df.columns:
        df.rename(columns={'CODE_SECTEUR_NAF2_CODE': 'CODE_SECTEUR_NAF2'}, inplace=True)
    if 'CODE_IRIS' in df.columns:
        df.rename(columns={'CODE_IRIS': 'IRIS_CODE'}, inplace=True)
    if 'CODE_IRIS_CODE' in df.columns:
        df.rename(columns={'CODE_IRIS_CODE': 'IRIS_CODE'}, inplace=True)
    if 'CODE_IRIS_LIBELLE' in df.columns:
        df.rename(columns={'CODE_IRIS_LIBELLE': 'IRIS_LIBELLE'}, inplace=True)


    # Supprimer les lignes avec valeurs 'secret' ou nulles
    if {'CONSO', 'PDL', 'INDQUAL'}.issubset(df.columns):
        df = df[~((df['CONSO'] == 'secret') & (df['PDL'] == 'secret'))]
        df = df.dropna(subset=['CONSO', 'PDL', 'INDQUAL'])
        df = df[(df['CONSO'] != '') & (df['PDL'] != '') & (df['INDQUAL'] != '')]

    # Supprimer colonnes inutiles
    df.drop(columns=["CODE_EIC","THERMOR","IRIS_LIBELLE","CORRECTION_CODE_IRIS","PART","NOM_COMMUNE","CODE_SECTEUR_NAF2_LIBELLE"], errors="ignore", inplace=True)


    # Ajouter à la liste
    dfs.append(df)

# Fusion finale
if dfs:
    df_final = pd.concat(dfs, ignore_index=True)
    df_final.to_csv(output_file, index=False, encoding="utf-8-sig", sep=";")
