import dash
from dash import dcc, html, callback, Input, Output, State, dash_table
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import wikipedia
import geopandas as gpd
import glob
import os
import json
import fonctions_utiles

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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Br(), 
            html.H1("La vie avifaune du Grand Est", className="text-primary fw-bold text-center"),
            html.Br()
            ])
    ]),
    dcc.Location(id="url"),
    dbc.Tabs([ 
        # Onglet Pouvoirs Publics
        dbc.Tab(label="Pouvoirs Publics", tab_id="tab-pp", children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        html.H3("Filtre d'affichage"),
                        html.P("Famille d'oiseau à analyser"),
                        dbc.Select(id="Family", options=[
                        ]),
                        html.Br(), 
                        html.P("Polluant à analyser"),
                        dbc.Select(id="Pollutant", options=[
                        ]),
                        html.Br(),
                        html.P("Choix de l'année"),
                        dcc.Slider(
                            id="year-slider",
                            min=2018,
                            max=2022,
                            step=1,
                            value=2020,
                            marks={i: str(i) for i in range(2018, 2023)},
                            allow_direct_input=False
                        ),
                        html.Br(),
                        html.Div(
                            dbc.Button("Appliquer filtres",id="filter-button", color="primary"),
                            className="d-grid gap-2",
                        ),
                    ],width=3),
                    dbc.Col([
                        html.Br(),
                        html.H3("Carte"),
                        html.Br(),
                        dcc.Graph(id="map-executive"),
                        html.Br(),
                        html.P(id="map-count")
                    ],width=5),
                    dbc.Col([
                        html.Br(),
                        html.H3("Richesse spécifique par département"),
                        html.H5(id="species-year"),
                        html.P(id="species-count", style={"white-space": "pre-line"})
                    ],width=4)
                ])
            ])
        ]),
        
        # Onglet Grand Public
        dbc.Tab(label="Grand Public", tab_id="tab-gp", children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        html.H3("Choix de l'année"),
                        dcc.Slider(
                            id="year-slider-public",
                            min=2018,
                            max=2022,
                            step=1,
                            value=2020,
                            marks={i: str(i) for i in range(2018, 2023)},
                            allow_direct_input=False
                        )
                    ]),
                    dbc.Col([
                        html.Br(),
                        html.H3("Wikipédia"),
                        html.H3("Abondance")
                    ])
                ]) 
            ])       
        ])
    ])
])

@app.callback(
    Output(component_id="Family", component_property="options"),
    Input("url", "pathname") 
)
def complete_family_select(_):
    return family_options

@app.callback(
    Output(component_id="Pollutant", component_property="options"),
    Input("url", "pathname") 
)
def complete_pollutant_select(_):
    return pollutant_options

@app.callback(
    Output("map-executive", "figure"),
    Output("map-count", "children"),
    Input("filter-button", "n_clicks"),
    State("Family", "value"),
    State("Pollutant", "value"),
    State("year-slider", "value")
)
def update_map(n_clicks, family, pollutant, year):
    if n_clicks == 0:
        return dash.no_update 
    if family == "" or pollutant == "":
        return dash.no_update 
    
    gdf_year = gdf[gdf["annee"] == year]
    gdf_family = gdf_year[gdf_year["family"] == family]

    fig = go.Figure()

    fig.add_trace(
        go.Choroplethmap(
            geojson=geojson_dep,
            locations=departements.index,
            z=gdf_year[pollutant],
            colorscale="purples",
            showscale=False,
            marker_line_color="gray",
            marker_line_width=0.5,
            hoverinfo="skip"
        )
    )

    fig.add_trace(
        go.Scattermap(
            lat=gdf_family["decimalLatitude"],
            lon=gdf_family ["decimalLongitude"],
            mode="markers",
            marker=dict(
                size=6,
                color="lightgreen",
                opacity=0.7
            ),
            name="Observations"
        )
    )

    fig.update_layout(
        map=dict(
            center=dict(lat=48.8, lon=5.5),
            zoom=6
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return fig, f"{len(gdf_family)} obeservations de {family}"

@app.callback(
    Output("species-count", "children"),
    Output("species-year", "children"),
    Input("filter-button", "n_clicks"),
    State("year-slider", "value")
)
def update_specific_wealth(n_clicks, year):
    if n_clicks == 0:
        return dash.no_update 

    df_year = dataset[dataset["annee"] == year]
    specific_wealth = fonctions_utiles.unique_species_per_department(df_year)

    str_list = []

    for key, val in specific_wealth.items():
        str_list.append(f" - {key} : {val} espèces différentes")
    
    return "\n".join(str_list), year
    
if __name__ == '__main__':
    app.run(debug=True)


