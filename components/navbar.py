import dash
import dash-bootstrap-components as dbc
from dash import html

def generate_sidebar():
    return html.Div([
        html.Div([
            html.H5("FINANSLA", style={"color": "#ffcc44", "fontWeight": "700", "margin": "0"}),
            html.Small("TERMINAL Engine v4.1", style={"color": "#5a7090", "fontSize": "9px"})
        ], style={"padding": "20px 15px", "borderBottom": "1px solid #1e2d42"}),
        
        dbc.Nav([
            dbc.NavLink([html.I(className="bi bi-speedometer2 me-2"), "MARKETS OVERVIEW"], href="/", active="exact", className="py-2 text-start"),
            dbc.NavLink([html.I(className="bi bi-graph-up me-2"), "STOCK ANALYTICS"], href="/stock", active="exact", className="py-2 text-start"),
            dbc.NavLink([html.I(className="bi bi-newspaper me-2"), "INTELLIGENCE FEED"], href="/news", active="exact", className="py-2 text-start"),
            dbc.NavLink([html.I(className="bi bi-person-workspace me-2"), "GURU PORTFOLIOS"], href="/gurus", active="exact", className="py-2 text-start"),
            dbc.NavLink([html.I(className="bi bi-filter-square me-2"), "EQUITY SCREENER"], href="/screener", active="exact", className="py-2 text-start"),
            dbc.NavLink([html.I(className="bi bi-wallet2 me-2"), "MY LEDGER PORTFOLIO"], href="/portfolio", active="exact", className="py-2 text-start")
        ], vertical=True, pills=True, style={"padding": "15px 10px"})
    ], style={
        "position": "fixed", "top": "0", "left": "0", "bottom": "0", 
        "width": "240px", "backgroundColor": "#111720", "borderRight": "1px solid #1e2d42",
        "zIndex": "1000"
    })