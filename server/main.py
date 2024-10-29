import dash
from dash import Dash, html, dash_table, dcc, ctx
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_bootstrap_components as dbc
from dbms_connection import (
    get_exercise_details, update_exercise_details, add_new_exercise
)

app = Dash(external_stylesheets=[dbc.themes.CYBORG])

# Search Widget
searchwidget = html.Div(children=[
    html.H2("Search Exercises"),
    html.Label("Enter exercise name or keyword:"),
    dcc.Input(id='input-box1', type='text', value='', debounce=True),
    html.Button('Search', id='search-button', n_clicks=0),
    html.Div(id='output-container1', style={'margin-top': '10px'})
], className='widget')

# Add New Exercise Form
add_exercise_form = html.Div(children=[
    html.H2("Add New Exercise"),
    dbc.Input(id='exercise-name', placeholder='Enter exercise name', type='text'),
    dbc.Input(id='body-part', placeholder='Enter body part', type='text'),
    dbc.Input(id='equipment', placeholder='Enter equipment', type='text'),
    html.Button('Add Exercise', id='add-exercise-button', n_clicks=0),
    html.Div(id='add-exercise-output', style={'margin-top': '10px'})
])

# Layout
app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(searchwidget, width=4),
            dbc.Col(add_exercise_form, width=4)
        ],
        className='rowing',
    )
)

# Callback for Searching Exercises
@app.callback(
    Output('output-container1', 'children'),
    Input('search-button', 'n_clicks'),
    State('input-box1', 'value')
)
def search_exercise(n_clicks, exercise_name):
    if n_clicks == 0 or not exercise_name:
        raise PreventUpdate

    result = get_exercise_details(exercise_name)
    if result == ['', '', '', '']:
        return html.P("No matching exercises found.")
    
    return html.Div([
        html.P(f"WorkoutID: {result[0]}"),
        html.P(f"Name: {result[1]}"),
        html.P(f"Body Part: {result[2]}"),
        html.P(f"Equipment: {result[3]}")
    ])

# Callback for Adding New Exercise
@app.callback(
    Output('add-exercise-output', 'children'),
    Input('add-exercise-button', 'n_clicks'),
    State('exercise-name', 'value'),
    State('body-part', 'value'),
    State('equipment', 'value')
)
def add_exercise(n_clicks, name, body_part, equipment):
    if n_clicks == 0:
        raise PreventUpdate

    if not name or not body_part or not equipment:
        return html.P("All fields are required.", style={'color': 'red'})

    add_new_exercise(name, body_part, equipment)
    return html.P(f"Exercise '{name}' added successfully!", style={'color': 'green'})

if __name__ == '__main__':
    app.run(debug=True)
