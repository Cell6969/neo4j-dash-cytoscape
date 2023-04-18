import dash
from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
from cypher_function import *
import dash_cytoscape as cyto

dash.register_page(__name__,
                   path='/Graph',
                   name='Graph',
                   title='Graph'
                   )

# define neo4j identity
url = 'bolt://localhost:7687'
username = 'neo4j'
password = '12345678'
database = 'neo4j'

# get list node and relationship
node_list = get_list_nodes(url=url, username=username, password=password, database=database)
rel_list = get_list_relationship(url=url, username=username, password=password, database=database)
elements = []

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
            cyto.Cytoscape(
                id='cytoscape',
                elements=elements,
                layout={'name':'cose'},
                style={'width': '100%', 'height': '500px',},
                zoom = 20,
                stylesheet= [
                                {
                                    'selector': 'node',
                                    'style': {
                                        'label': 'data(label)',
                                        'text-valign': 'center',
                                        'text-halign': 'center',
                                        'font-size': 14,
                                        'color': '#000',
                                        'background-color': '#119DFF',
                                        'width' : '100px',
                                        'height': '100px'
                                    }
                                },
                                {
                                    'selector': 'node:selected',
                                    'style': {
                                        'background-color': '#f44336'
                                    }
                                },
                                {
                                    'selector': 'edge',
                                    'style': {
                                        'curve-style': 'bezier',
                                        'target-arrow-shape': 'triangle',
                                        'label': 'data(label)',
                                        'target-arrow-color': 'black',
                                        'target-arrow-size':2,
                                        'text-outline-color': '#fff',
                                        'text-outline-width': 2,
                                        'text-outline-opacity': 1,
                                        'color': '#000',
                                        'font-size': 14,
                                        'line-color': 'black',
                                        'width' : 3
                                    }
                                },
                                {
                                    'selector': 'edge:selected',
                                    'style' : {
                                        'line-color' : '#f44336'
                                    }
                                }
                                    ]
            )
        ])
    ]
)

@callback(
    Output('cytoscape', 'elements'),
    Input('button', 'n_clicks'),
    State('dropdown1', 'value'),
    State('dropdown2','value'),
    State('dropdown3', 'value')
)

def update_graph(n_clicks, value1, value2,value3):
    elements = []
    if n_clicks is not None:
        data = get_all_properties(url=url, username=username, password=password, database=database,
                                  NODE_1=value1, NODE_2=value2, RELATIONSHIP=value3)
        node1 = [{'data':{'id':row['S_NAME'], 'label':row['S_NAME']}} for row in data]
        node2 = [{'data':{'id':row['T_NAME'], 'label':row['T_NAME']}} for row in data]
        node1_2  = [{'data':{'source':row['S_NAME'], 'target':row['T_NAME'], 'label':value3}} for row in data]
        elements = node1 + node2 + node1_2
        return elements
    
    return elements