import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, register_page
import plotly.graph_objects as go
import dash_ag-grid as dag

from data.guru_holdings import GURU_DATA

register_page(__name__, path="/gurus")

layout = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Tabs(id="guru-tabs", value="buffett", children=[
                dcc.Tab(label="WARREN BUFFETT", value="buffett", className="custom-tab", selected_className="custom-tab--selected"),
                dcc.Tab(label="RAY DALIO", value="dalio", className="custom-tab", selected_className="custom-tab--selected"),
                dcc.Tab(label="MICHAEL BURRY", value="burry", className="custom-tab", selected_className="custom-tab--selected"),
                dcc.Tab(label="CATHIE WOOD", value="wood", className="custom-tab", selected_className="custom-tab--selected"),
                dcc.Tab(label="STANLEY DRUCKENMILLER", value="druckenmiller", className="custom-tab", selected_className="custom-tab--selected"),
            ], style={"fontFamily": "JetBrains Mono"})
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Div(id="guru-profile-panel", className="terminal-panel")
        ], width=4),
        dbc.Col([
            html.Div([
                html.Div("STRATEGIC ALLOCATION VECTOR PROFILE MATRIX", className="terminal-header"),
                dcc.Graph(id="guru-donut-chart", style={"height": "250px"})
            ], className="terminal-panel")
        ], width=8)
    ]),
    
    html.Div([
        html.Div("INSTITUTIONAL METRIC LEDGER POSITIONS FORMULA", className="terminal-header"),
        dag.AgGrid(
            id="guru-holdings-grid",
            className="ag-theme-alpine-dark",
            columnSize="sizeToFit",
            style={"height": "350px", "width": "100%"}
        )
    ], className="terminal-panel mt-4")
])

@callback(
    [Output("guru-profile-panel", "children"),
     Output("guru-donut-chart", "figure"),
     Output("guru-holdings-grid", "rowData"),
     Output("guru-holdings-grid", "columnDefs")],
    Input("guru-tabs", "value")
)
def update_guru_workspace(tab_key):
    g = GURU_DATA[tab_key]
    
    profile_html = [
        html.Div(g['fund'], className="terminal-header"),
        html.H3(g['name'], style={"color": "#ffcc44", "fontWeight": "700"}),
        html.Div([html.Strong("ESTIMATED REPORTED AUM: "), html.Span(g['aum'], style={"color": "#00ff88"})], style={"fontSize": "12px", "marginBottom": "10px"}),
        html.P(g['strategy'], style={"fontSize": "12px", "color": "#c8d8f0"}),
        html.Blockquote(f'"{g["quote"]}"', style={"fontSize": "11px", "color": "#5a7090", "fontStyle": "italic", "borderLeft": "2px solid #1e2d42", "paddingLeft": "10px"})
    ]
    
    sectors = list(set(g['sectors']))
    donut = go.Figure(data=[go.Pie(labels=sectors, values=g['allocation'][:len(sectors)], hole=.5, marker=dict(colors=['#00ff88','#ff4466','#4488ff','#ffcc44','#9944ff']))])
    donut.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True,
                        margin=dict(l=10, r=10, t=10, b=10), font=dict(family="JetBrains Mono", size=10))
    
    col_defs = [
        {"field": "Ticker", "headerName": "SYMBOL", "sortable": True, "filter": True},
        {"field": "Company", "headerName": "INSTITUTION NAME"},
        {"field": "Shares", "headerName": "SHARES REPORTED", "valueFormatter": {"function": "d3.format(',.0f')(params.value)"}},
        {"field": "Value", "headerName": "VALUE EQUIVALENT ($)", "valueFormatter": {"function": "d3.format(',.0f')(params.value)"}},
        {"field": "Weight", "headerName": "PORTFOLIO %", "valueFormatter": {"function": "d3.format('.2f')(params.value) + '%'"},
         "cellStyle": {"fontWeight": "600", "color": "#ffcc44"}},
        {"field": "Change", "headerName": "QoQ CHANGE VECTORS", "cellStyle": {"styleConditions": [
            {"condition": "params.value.includes('▲')", "style": {"color": "#00ff88"}},
            {"condition": "params.value.includes('▼')", "style": {"color": "#ff4466"}}
        ]}}
    ]
    
    return profile_html, donut, g['holdings'], col_defs