import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import matplotlib.pyplot as plt
import wikipedia
import fonctions_utiles

dataset = fonctions_utiles.dataset
departements = fonctions_utiles.departements
geojson_dep = fonctions_utiles.geojson_dep
pollutant_options = fonctions_utiles.pollutant_options
family_options = fonctions_utiles.family_options
gdf = fonctions_utiles.gdf

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
                        html.H3(id="text-public"),
                        dcc.Slider(
                            id="year-slider-public",
                            min=2018,
                            max=2022,
                            step=1,
                            value=2018,
                            marks={i: str(i) for i in range(2018, 2023)},
                            allow_direct_input=False
                        ),
                        html.Br(),
                        dcc.Graph(id="map-public"),
                        dcc.Store(id="family-index", data=0)
                    ]),
                    dcc.Interval(id="interval", interval=5000, n_intervals=0),
                    dbc.Col([
                        html.Br(),
                        html.H3("Wikipédia"),
                        html.H5(id="wikipedia-title"),
                        html.P(id="wikipedia-content"),
                        html.Img(
                            id="wikipedia-image", 
                            style={
                                "width": "400px",
                                "borderRadius": "10px",
                                "boxShadow": "0px 4px 10px rgba(0,0,0,0.2)"
                            })
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
    
@app.callback(
    Output("year-slider-public", "value"),
    Output("family-index", "data"),
    Input("interval", "n_intervals"),
    State("year-slider-public", "value"),
    State("family-index", "data"),
)
def animate_year(n, year, i):
    if year == 2022:
        year = 2018
        if i == len(family_options)-1:
            i = 0
        else:
            i += 1
    else:
        year += 1
    return year, i

@app.callback(
    Output("map-public", "figure"),
    Input("year-slider-public", "value"),
    Input("family-index", "data"),
)
def animate_map(year, i):
    gdf_year = gdf[gdf["annee"] == year]
    gdf_family = gdf_year[gdf_year["family"] == family_options[i]["value"]]

    fig = px.density_map(
        gdf_family,
        lat="decimalLatitude",
        lon="decimalLongitude",
        radius=10,
        center=dict(lat=48.8, lon=5.5),
        zoom=5.5,
        map_style="open-street-map",
        opacity=0.6,
        color_continuous_scale="greens"
    )
    fig.update_layout(coloraxis_showscale=False)
    return fig

@app.callback(
    Output("wikipedia-title", "children"),
    Output("wikipedia-content", "children"),
    Output("wikipedia-image", "src"),
    Input("family-index", "data"),
)
def complete_wikipedia(i):
    displayed_family = family_options[i]["value"]
    wikipedia.set_lang("fr")
    page = wikipedia.page(displayed_family)

    return page.title, page.summary, page.images[0]



if __name__ == '__main__':
    app.run(debug=True)


