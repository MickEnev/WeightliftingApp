import dash
from dash import Dash, html, dash_table, dcc, ctx
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dbms_connection import (
    get_mysql_keywords, get_mongodb_pie, get_neo4j_bar, get_mysql_search, get_faculty,
    get_highest_KRC, list_faculty, list_faculty_details, update_faculty_details,
    list_faculty_keywords, update_faculty_keywordsA, update_faculty_keywordsD
)
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.CYBORG])