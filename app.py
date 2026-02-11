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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Br(), 
            html.H1("La vie avifaune du Grand Est", className="text-primary fw-bold text-center"),
            html.Br()
            ])
    ]),

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
                            {"label": "Option 1", "value": "1"},
                            {"label": "Option 2", "value": "2"}
                        ]),
                        html.Br(), 
                        html.P("Polluant à analyser"),
                        dbc.Select(id="Pollutant", options=[
                            {"label": "Option 1", "value": "1"},
                            {"label": "Option 2", "value": "2"}
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
                        )
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
                            id="year-slider",
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

if __name__ == '__main__':
    app.run(debug=True)