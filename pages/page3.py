import dash
from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import numpy as np
from cypher_function import *
import dash_leaflet as dl

dash.register_page(__name__,
                   path='/Maps',
                   name='Maps',
                   title='Maps'
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
            dl.Map(
                id='map',
                children=[
                    dl.TileLayer(),
                    dl.LayerGroup(id='marker-layer'),
                    dl.LayerGroup(id='polyline-layer')
                ],
                center=[-7.2575, 112.7521],
                zoom=7,
                style={'width': '100%', 'height': '470px'}
            )
        ])
    ]
)

@callback(
    Output('marker-layer','children'),
    Output('polyline-layer','children'),
    Input('button','n_clicks'),
    State('dropdown1', 'value'),
    State('dropdown2','value'),
    State('dropdown3', 'value'),
    State('map','children')
)

def update_map(n_clicks, value1, value2, value3, map_children):
    if n_clicks is None:
        return [], []
    else:
        data = get_all_properties(url=url, username=username, password=password, database=database,
                                  NODE_1=value1, NODE_2=value2, RELATIONSHIP=value3)
        markers = [dl.Marker(position=[np.float64(data[i]['S_LATITUDE']), np.float64(data[i]['S_LONGITUDE'])],
                             children=[dl.Popup(f"{data[i]['S_NAME']}")])
                   for i in range(len(data))]
        markers += [dl.Marker(position=[np.float64(data[i]['T_LATITUDE']), np.float64(data[i]['T_LONGITUDE'])],
                             children=[dl.Popup(f"{data[i]['T_NAME']}")])
                   for i in range(len(data))]
        polylines = [dl.Polyline(
            positions=[[np.float64(data[i]['S_LATITUDE']), np.float64(data[i]['S_LONGITUDE'])],
                       [np.float64(data[i]['T_LATITUDE']), np.float64(data[i]['T_LONGITUDE'])]],
            color='red',
            weight=2,
            opacity=1.0,
            lineCap='round',
            lineJoin='round',
            children=[
                dl.Popup(f"Line {data[i]['S_NAME']} and {data[i]['T_NAME']}")
            ]) for i in range(len(data))]
        
        return markers, polylines