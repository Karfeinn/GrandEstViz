import pandas as pd
import numpy as np
import glob
import os
import geopandas as gpd
from shapely.geometry import Point

oiseau = pd.read_csv("./CSV/oiseaux_grand-est_2018-2022_GBIF.csv", sep='\t', low_memory=False)
oiseau = oiseau.drop(['infraspecificEpithet','taxonRank','verbatimScientificName','verbatimScientificNameAuthorship','countryCode','locality','stateProvince','publishingOrgKey','elevation','elevationAccuracy','depth','depthAccuracy','day','month','taxonKey','speciesKey','institutionCode','collectionCode','catalogNumber','recordNumber','identifiedBy','dateIdentified','license','rightsHolder','recordedBy','typeStatus','establishmentMeans','lastInterpreted','mediaType','issue'], axis=1)

#import des geojson

path = "./CSV/GEOJSON/"
all_files = glob.glob(os.path.join(path, "*.geojson"))
liste_dep = [gpd.read_file(f) for f in all_files]
departements = pd.concat(liste_dep, ignore_index=True)
departements = departements.to_crs("EPSG:4326")

#import des GES

path_ges = "./CSV/GES/"
ges_files = glob.glob(os.path.join(path_ges, "*.csv"))

ges_list = []
for f in ges_files:
    df = pd.read_csv(f)
    annee = int(os.path.basename(f).split('_')[-1].split('.')[0])
    df['annee'] = df.get('annee_inv', annee)
    df = df.rename(columns={"lib_zone": "departement"})
    ges_list.append(df)

ges_all = pd.concat(ges_list, ignore_index=True)

#import des EMI

path_emi = "./CSV/EMI/"
emi_files = glob.glob(os.path.join(path_emi, "*.csv"))

emi_list = []
for f in emi_files:
    df = pd.read_csv(f)
    annee = int(os.path.basename(f).split('_')[-1].split('.')[0])
    df['annee'] = df.get('annee', annee)  # priorise la colonne annee si elle existe
    df = df.rename(columns={"lib_zone": "departement"})
    emi_list.append(df)

emi_all = pd.concat(emi_list, ignore_index=True)

geometry = [Point(xy) for xy in zip(oiseau['decimalLongitude'], oiseau['decimalLatitude'])]
gdf_oiseau = gpd.GeoDataFrame(oiseau, geometry=geometry, crs="EPSG:4326")

result = gpd.sjoin(gdf_oiseau, departements, how="left", predicate="within")
result = result.rename(columns={'nom': 'departement', 'year':'annee'})

merged = pd.merge(result, ges_all, on=["departement", "annee"], how="left")
merged = pd.merge(merged, emi_all, on=["departement", "annee"], how="left")

merged.to_csv('./CSV/fusion.csv')