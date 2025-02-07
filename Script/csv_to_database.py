import pandas as pd
import os

# Spécifiez le chemin des dossiers contenant les fichiers CSV
gaz = 'C:/Users/abellantan/Documents/GitHub/SAE-6.-D-veloppement-d-un-outil-d-cisionnel/DATA/gaz'
elec = 'C:/Users/abellantan/Documents/GitHub/SAE-6.-D-veloppement-d-un-outil-d-cisionnel/DATA/elec'
chaleur = 'C:/Users/abellantan/Documents/GitHub/SAE-6.-D-veloppement-d-un-outil-d-cisionnel/DATA/chaleur'

# Liste des dossiers avec leurs types d'énergie associés
dossiers = {
    'gaz': gaz,
    'elec': elec,
    'chaleur': chaleur
}

# Dictionnaire pour stocker les DataFrames par type d'énergie
dataframes_par_energie = {}

# Parcours chaque dossier et charge les fichiers CSV dans un DataFrame par type d'énergie
for energie, dossier in dossiers.items():
    fichiers_csv = [f for f in os.listdir(dossier) if f.endswith('.csv')]  # Liste des fichiers CSV dans le dossier
    fichier_excel = [f for f in os.listdir(dossier) if f.endswith('.xlsx')]
    dataframes = []  # Liste pour les DataFrames de ce type d'énergie
    df=pd.read_excel(os.path.join(dossier,fichier_excel[0]),header=1)
    dataframes.append(df)
    for fichier in fichiers_csv:
        try:
            # Chargement du fichier CSV et ajout à la liste
            df = pd.read_csv(os.path.join(dossier, fichier), sep=';', encoding='UTF-8', header=1)
            dataframes.append(df)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {fichier}: {e}")
    
    # Concaténer les DataFrames du type d'énergie courant
    dataframes_par_energie[energie] = pd.concat(dataframes, ignore_index=True)


# Afficher les premières lignes pour chaque type d'énergie
for energie, df in dataframes_par_energie.items():
    print(f"\nDataFrame pour {energie}:")
    print("Colonnes:", df.columns)
    print(df.shape)
    #print(df.head())
