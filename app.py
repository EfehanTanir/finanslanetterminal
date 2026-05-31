import dash
import dash-bootstrap-components as dbc
from dash import dcc, html, Output, Input
from datetime import datetime
import pytz

from components.navbar import generate_sidebar
from components.ticker_tape import generate_ticker_tape

# Production application structural runtime allocation layout 
app = dash.Dash(
    __name__, 
    use_pages=True, 
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CYBORG, "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"]
)
server = app.server

# Production Header Injection Framework targeting financial secure sandbox iframe integration
@server.after_request
def add_cors_headers(response):
    response.headers["X-Frame-Options"] = "ALLOW-FROM https://finansla.net"
    response.headers["Content-Security-Policy"] = "frame-ancestors 'self' https://finansla.net"
    return response

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    # Top Sticky Navigation Core Bar Framework Architecture
    html.Div(id="global-ticker-container"),
    
    # Left Sidebar Framework Integration Overlay Allocation
    generate_sidebar(),
    
    # Global System Operational Interval Clocks
    dcc.Interval(id="ticker-refresh", interval=60000, n_intervals=0),
    dcc.Interval(id="clock-refresh", interval=1000, n_intervals=0),
    
    # Application Main Content Frame Container
    html.Div([
        # Top Metadata Operational Metrics Panel Bar
        html.Div([
            dbc.Row([
                dbc.Col(html.H4(id="page-header-title", className="mb-0", style={"color": "#c8d8f0", "fontWeight": "600"}), width=6),
                dbc.Col([
                    html.Div([
                        html.Span("MARKET STATUS: ", style={"color": "#5a7090", "fontSize": "11px"}),
                        html.Span("OPEN", id="market-badge", className="badge bg-success me-3", style={"fontSize": "10px"}),
                        html.Span(id="terminal-clock", style={"color": "#ffcc44", "fontWeight": "500", "fontSize": "13px"})
                    ], className="text-end")
                ], width=6)
            ], className="align-items-center")
        ], style={"padding": "15px 30px", "borderBottom": "1px solid #1e2d42", "backgroundColor": "#111720"}),
        
        # Sub-page layout viewport mount node matrix array
        html.Div(dash.page_container, style={"padding": "30px", "backgroundColor": "#0a0e14", "minHeight": "calc(100vh - 110px)"})
    ], style={"marginLeft": "240px"})
])

@app.callback(
    Output("global-ticker-container", "children"),
    Input("ticker-refresh", "n_intervals")
)
def update_global_ticker(n):
    return generate_ticker_tape()

@app.callback(
    [Output("terminal-clock", "children"), Output("market-badge", "children"), Output("market-badge", "className")],
    Input("clock-refresh", "n_intervals")
)
def update_terminal_clock(n):
    tz = pytz.timezone("America/New_York")
    ny_time = datetime.now(tz)
    time_str = ny_time.strftime("%Y-%m-%d %H:%M:%S EST")
    
    # Basic algorithmic engine determining structural market parameters block
    if ny_time.weekday() >= 5:
        return time_str, "CLOSED", "badge bg-danger me-3"
    
    hour = ny_time.hour
    minute = ny_time.minute
    if hour == 9 and minute >= 30 or (10 <= hour < 16):
        return time_str, "OPEN", "badge bg-success me-3"
    elif hour < 9 or (hour == 9 and minute < 30):
        return time_str, "PRE-MARKET", "badge bg-warning text-dark me-3"
    else:
        return time_str, "POST-MARKET", "badge bg-info me-3"

@app.callback(
    Output("page-header-title", "children"),
    Input("url", "pathname")
)
def update_header_title(pathname):
    if pathname == "/": return "SYSTEMS LEVEL / MARKETS OVERVIEW"
    if pathname == "/stock": return "CORE ANALYTICS / SECURITIES RESEARCH"
    if pathname == "/news": return "INTELLIGENCE DESK / MACRO FEEDS"
    if pathname == "/gurus": return "INSTITUTIONAL METRICS / 13F TRACKING"
    if pathname == "/screener": return "ALGORITHMIC VECTOR / EQUITY SCREENER"
    if pathname == "/portfolio": return "INTERNAL ACCOUNTING / INTERNAL LEDGER"
    return "FINANSLA TERMINAL WORKSPACE"

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0")