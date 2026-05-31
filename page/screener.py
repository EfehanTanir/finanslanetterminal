import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, register_page
import dash_ag-grid as dag
import pandas as pd

register_page(__name__, path="/screener")

# Mock database matrix compilation targeting standard screener interface calculations
MOCK_SCREENER_POOL = [
    {"Ticker": "AAPL", "Company": "Apple Inc.", "Sector": "Technology", "Price": 175.20, "PE": 28.4, "Yield": 0.55, "Mcap": 2700000000000},
    {"Ticker": "NVDA", "Company": "NVIDIA Corp.", "Sector": "Technology", "Price": 875.12, "PE": 74.2, "Yield": 0.02, "Mcap": 2190000000000},
    {"Ticker": "TSLA", "Company": "Tesla Inc.", "Sector": "Automotive", "Price": 170.18, "PE": 42.1, "Yield": 0.00, "Mcap": 540000000000},
    {"Ticker": "XOM", "Company": "Exxon Mobil Corp.", "Sector": "Energy", "Price": 118.50, "PE": 12.8, "Yield": 3.20, "Mcap": 470000000000},
    {"Ticker": "JPM", "Company": "JPMorgan Chase", "Sector": "Financials", "Price": 195.40, "PE": 11.5, "Yield": 2.35, "Mcap": 560000000000},
    {"Ticker": "THYAO.IS", "Company": "Türk Hava Yolları", "Sector": "Transportation", "Price": 310.50, "PE": 8.2, "Yield": 0.00, "Mcap": 428000000000},
    {"Ticker": "TUPRS.IS", "Company": "Tüpraş", "Sector": "Energy", "Price": 165.20, "PE": 6.8, "Yield": 6.80, "Mcap": 318000000000},
]

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("DYNAMIC FUNDAMENTAL PARAMETRIC VECTOR FILTER CONTROLS", className="terminal-header"),
                html.Label("SECTOR MATRIX PROFILE SELECT", className="text-muted small"),
                dcc.Dropdown(
                    id='screener-sector-dropdown',
                    options=[{'label': s, 'value': s} for s in ["Technology", "Energy", "Financials", "Automotive", "Transportation"]],
                    multi=True, className="bg-dark text-white mb-3"
                ),
                html.Label("MAXIMUM P/E MATRIX BOUNDS", className="text-muted small"),
                dcc.Slider(id='screener-pe-slider', min=0, max=100, step=5, value=100, marks={0:'0', 50:'50', 100:'100'}, className="mb-3"),
                
                html.Label("MINIMUM ASSET DIVIDEND VALUE TARGET (%)", className="text-muted small"),
                dcc.Slider(id='screener-yield-slider', min=0, max=10, step=0.5, value=0, marks={0:'0%', 5:'5%', 10:'10%'}, className="mb-3")
            ], className="terminal-panel")
        ], width=4),
        
        dbc.Col([
            html.Div([
                html.Div("ALGORITHMIC AGGREGATION QUANT FILTER RESULTS VIEWPORT", className="terminal-header"),
                dag.AgGrid(
                    id="screener-results-grid",
                    className="ag-theme-alpine-dark",
                    columnSize="sizeToFit",
                    columnDefs=[
                        {"field": "Ticker", "headerName": "SYMBOL"},
                        {"field": "Company", "headerName": "CORPORATE NAME"},
                        {"field": "Sector", "headerName": "SECTOR RESOURCE"},
                        {"field": "Price", "headerName": "LAST PRICE MASK", "valueFormatter": {"function": "d3.format(',.2f')(params.value)"}},
                        {"field": "PE", "headerName": "P/E RATIO", "cellStyle": {"color": "#ffcc44"}},
                        {"field": "Yield", "headerName": "DIV VALUE YIELD %", "valueFormatter": {"function": "d3.format('.2f')(params.value) + '%'"}, "cellStyle": {"color": "#00ff88"}},
                        {"field": "Mcap", "headerName": "CAPITALIZATION INDEX", "valueFormatter": {"function": "d3.format(',.0f')(params.value)"}}
                    ],
                    style={"height": "400px", "width": "100%"}
                )
            ], className="terminal-panel")
        ], width=8)
    ])
])

@callback(
    Output("screener-results-grid", "rowData"),
    [Input("screener-sector-dropdown", "value"),
     Input("screener-pe-slider", "value"),
     Input("screener-yield-slider", "value")]
)
def run_screener_engine(sectors, max_pe, min_yield):
    filtered = MOCK_SCREENER_POOL
    if sectors:
        filtered = [r for r in filtered if r['Sector'] in sectors]
    filtered = [r for r in filtered if r['PE'] <= max_pe]
    filtered = [r for r in filtered if r['Yield'] >= min_yield]
    return filtered