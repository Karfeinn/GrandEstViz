import pandas as pd
import glob
import geopandas as gpd
import os
import json

dataset = pd.read_csv("./CSV/fusion.csv",engine='c', dtype={
    "gbifID": "int32",
    "kingdom":"category",
    "phylum":"category",
    "class":"category",
    "order":"category",
    "family":"category",
    "genus":"category",
    "species":"category",
    'scientificName':"category",
    'occurrenceStatus':"category", 
    'individualCount':"object",
    'decimalLatitude':"float64",
    'decimalLongitude':"float64", 
    'annee':"int32", 
    'code':"object", 
    'departement':"category",  
    'co2_kg':"float64",
    'ch4_kg':"float64", 
    'n2o_kg':"float64", 
    'hfc_23_kg':"float64", 
    'hfc_32_kg':"float64", 
    'hfc_125_kg':"float64",
    'hfc_134a_kg':"float64", 
    'hfc_143a_kg':"float64", 
    'hfc_152a_kg':"float64", 
    'hfc_227ea_kg':"float64",
    'hfc_245fa_kg':"float64", 
    'hfc_365mfc_kg':"float64", 
    'pfc_kg':"float64", 
    'sf6_kg':"float64", 
    'nf3_kg':"float64",
    'prg2007_teqco2':"float64", 
    'prg2013_teqco2':"float64", 
    'co2_bio_kg':"float64", 
    'nox_kg':"float64", 
    'so2_kg':"float64", 
    'pm10_kg':"float64", 
    'pm25_kg':"float64", 
    'co_kg':"float64", 
    'c6h6_kg':"float64",
    'covnm_kg':"float64", 
    'nh3_kg':"float64", 
    'as_kg':"float64", 
    'cd_kg':"float64", 
    'ni_kg':"float64", 
    'pb_kg':"float64", 
    'bap_kg':"float64",
    'geom_y':"string", 
})

path = "./CSV/GEOJSON/"
all_files = glob.glob(os.path.join(path, "*.geojson"))
liste_dep = [gpd.read_file(f) for f in all_files]
departements = pd.concat(liste_dep, ignore_index=True)
departements = departements.to_crs("EPSG:4326")
geojson_dep = json.loads(departements.to_json())

pollutant_dict = {
    "Oxydes d'azote (NOx)": "nox_kg",
    "Dioxyde de soufre (SO₂)": "so2_kg",
    "Particules PM10": "pm10_kg",
    "Particules PM2.5": "pm25_kg",
    "Monoxyde de carbone (CO)": "co_kg",
    "Benzène (C6H6)": "c6h6_kg",
    "Composés Organiques Volatils (COVNM)": "covnm_kg",
    "Ammoniac (NH₃)": "nh3_kg",
    "Arsenic (As)": "as_kg",
    "Cadmium (Cd)": "cd_kg",
    "Nickel (Ni)": "ni_kg",
    "Plomb (Pb)": "pb_kg",
    "Benzo[a]pyrène (BaP)": "bap_kg",
    "Dioxyde de carbone (CO₂)": "co2_kg",
    "Méthane (CH₄)": "ch4_kg",
    "Protoxyde d'azote (N₂O)": "n2o_kg",
    "HFC-23": "hfc_23_kg",
    "HFC-32": "hfc_32_kg",
    "HFC-125": "hfc_125_kg",
    "HFC-134a": "hfc_134a_kg",
    "HFC-143a": "hfc_143a_kg",
    "HFC-152a": "hfc_152a_kg",
    "HFC-227ea": "hfc_227ea_kg",
    "HFC-245fa": "hfc_245fa_kg",
    "HFC-365mfc": "hfc_365mfc_kg",
    "Perfluorocarbures (PFC)": "pfc_kg",
    "Hexafluorure de soufre (SF₆)": "sf6_kg",
    "Trifluorure d'azote (NF₃)": "nf3_kg",
    "PRG 2007 (t éq. CO₂)": "prg2007_teqco2",
    "PRG 2013 (t éq. CO₂)": "prg2013_teqco2",
    "CO₂ biogénique": "co2_bio_kg",
}

pollutant_options = [
    {"label": k, "value": v}
    for k, v in pollutant_dict.items()
]

family_options = [
    {"label": f, "value": f}
    for f in dataset["family"].cat.categories
]

gdf = gpd.GeoDataFrame(
    dataset,
    geometry=gpd.points_from_xy(dataset.decimalLongitude, dataset.decimalLatitude),
    crs="EPSG:4326" 
)

def unique_species_per_department(df):
    result = (
        df.groupby("departement", observed=True)["species"]
          .nunique()
          .reset_index(name="unique_species_count")
    )

    species_dict = dict(zip(result['departement'], result['unique_species_count']))

    return species_dict