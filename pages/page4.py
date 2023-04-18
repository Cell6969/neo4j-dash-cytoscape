import dash
from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import numpy as np
from cypher_function import *
from dash_table import DataTable

dash.register_page(__name__,
                   path='/Table',
                   name='Table',
                   title='Table'
                   )

# define neo4j identity
url = 'bolt://localhost:7687'
username = 'neo4j'
password = '12345678'
database = 'neo4j'

# get list node and relationship
node_list = get_list_nodes(url=url, username=username, password=password, database=database)
rel_list = get_list_relationship(url=url, username=username, password=password, database=database)

layout = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(options=node_list, id='dropdown1')
            ]),
            
            dbc.Col([
                dcc.Dropdown(options=node_list, id='dropdown2')
            ]),
            dbc.Col([
                dcc.Dropdown(options=rel_list, id='dropdown3')
            ]),
            dbc.Col([
                html.Button('MATCH',id='button', style={'width':'200px'})
            ])
        ]),
        html.Hr(),
        dbc.Row([
            DataTable(
                id = 'table',
                columns=[{"name": i, "id": i} for i in ["S_IP", "S_NAME","T_DEVICE","T_IP","T_NAME"]],
                data=[],
                style_cell={
                    'textAlign': 'center',  # Set text alignment to center
                    'padding': '5px',  # Set padding around the cell
                    'minWidth': '100px',  # Set minimum width of the cell
                    'width': '150px',  # Set width of the cell
                    'maxWidth': '150px',  # Set maximum width of the cell
                    'whiteSpace': 'normal',  # Set white space handling to normal
                    'overflow': 'hidden',  # Set overflow handling to hidden
                    'textOverflow': 'ellipsis'  # Set text overflow handling to ellipsis
                }
            )
        ])
    ]
)

@callback(
    Output('table','data'),
    Input('button', 'n_clicks'),
    State('dropdown1', 'value'),
    State('dropdown2','value'),
    State('dropdown3', 'value')
)

def update_table(n_clicks,value1, value2, value3):
    data = []
    if n_clicks is not None:
        data = get_all_properties(url=url, username=username, password=password, database=database,
                                  NODE_1=value1, NODE_2=value2, RELATIONSHIP=value3)
        return data
    return data