import dash
from dash import dcc, html, callback, Input, Output, dash_table
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

if __name__ == '__main__':
    app.run(debug=True)