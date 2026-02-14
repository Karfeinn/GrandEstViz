import dash
from dash import dcc, html, callback, Input, Output, dash_table
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import wikipedia

dataset = pd.read_csv("./CSV/fusion.csv", dtype={
    "gbifID": "int32",
    "kingdom":"string",
    "phylum":"string",
    "class":"string",
    "order":"string",
    "family":"string",
    "genus":"string",
    "species":"string",
    'scientificName':"string",
    'occurrenceStatus':"string", 
    'individualCount':"object",
    'decimalLatitude':"float64",
    'decimalLongitude':"float64", 
    'coordinateUncertaintyInMeters':"float64",
    'coordinatePrecision':"float64", 
    'eventDate':"string", 
    'annee':"int32", 
    'basisOfRecord':"string",
    'geometry':"object", 
    'index_right':"float64", 
    'code':"object", 
    'departement':"string", 
    'OBJECTID_x':"object",
    'type_zone_x':"string", 
    'code_zone_x':"object", 
    'version_x':"string", 
    'annee_inv_x':"object", 
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
    'geom_x':"string",
    'GlobalID_x':"string", 
    'Shape__Area_x':"float64", 
    'Shape__Length_x':"float64", 
    'code_epci':"object",
    'OBJECTID_y':"object", 
    'type_zone_y':"string", 
    'code_zone_y':"object", 
    'version_y':"string", 
    'annee_inv_y':"object",
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
    'GlobalID_y':"string", 
    'Shape__Area_y':"float64", 
    'Shape__Length_y':"float64"
})


pollutant_list = ['nox_kg','so2_kg','pm10_kg','pm25_kg','co_kg','c6h6_kg','covnm_kg','nh3_kg','as_kg','cd_kg','ni_kg','pb_kg','bap_kg','co2_kg','ch4_kg','n2o_kg','hfc_23_kg','hfc_32_kg','hfc_125_kg','hfc_134a_kg','hfc_143a_kg','hfc_152a_kg','hfc_227ea_kg','hfc_245fa_kg','hfc_365mfc_kg','pfc_kg','sf6_kg','nf3_kg','prg2007_teqco2','prg2013_teqco2','co2_bio_kg']

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
                        html.P("Espèce d'oiseau à analyser"),
                        dbc.Select(id="Species", options=[
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
                            dbc.Button("Appliquer filtres", color="primary"),
                            className="d-grid gap-2",
                        ),
                    ],width=3),
                    dbc.Col([
                        html.Br(),
                        html.H3("Carte")
                    ],width=5),
                    dbc.Col([
                        html.Br(),
                        html.H3("Abondance par département")
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
    Output(component_id="Species", component_property="options"),
    Input("url", "pathname") 
)
def complete_family_select(_):
    option_list = []
    for family in pd.unique(dataset['family']):
        option_list.append({"label": family, "value": family})
    return option_list

@app.callback(
    Output(component_id="Pollutant", component_property="options"),
    Input("url", "pathname") 
)
def complete_pollutant_select(_):
    option_list = []
    for pollutant in pollutant_list:
        option_list.append({"label": pollutant, "value": pollutant})
    return option_list


if __name__ == '__main__':
    app.run(debug=True)


