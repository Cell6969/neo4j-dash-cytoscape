import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
server = app.server

sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Page 1',href='#')),
        dbc.NavItem(dbc.NavLink('Page 2',href='#')),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Header',header=True),
                dbc.DropdownMenuItem('About', href='#'),
                dbc.DropdownMenuItem('Log Out', href='#')
            ],
            nav=True,
            in_navbar=True,
            label='More'
        ),
    ],
    brand= 'Application',
    brand_href = '#',
    color="primary",
    dark=True,
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            [
                    navbar
            ])
            ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port='8050')