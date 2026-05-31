import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, register_page, State
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

register_page(__name__, path="/stock")

layout = html.Div([
    dbc.Row([
        dbc.Col(dbc.Input(id="stock-search", placeholder="ENTER SEC TICKER SYMBOL (e.g. NVDA, THYAO.IS)...", value="NVDA", type="text", className="bg-dark text-white border-secondary"), width=4),
        dbc.Col(dbc.Button("EXECUTE RUNTIME RETRIEVAL", id="stock-search-btn", color="warning", className="w-100"), width=2)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("TECHNICAL FINANCIAL ENGINE CORE FRAMEWORK VISUALIZER", className="terminal-header"),
                dbc.ButtonGroup([
                    dbc.Button("1D", id="btn-1d", color="secondary", size="sm"),
                    dbc.Button("1W", id="btn-1w", color="secondary", size="sm"),
                    dbc.Button("1M", id="btn-1m", color="secondary", size="sm"),
                    dbc.Button("3M", id="btn-3m", color="secondary", size="sm"),
                    dbc.Button("1Y", id="btn-1y", color="secondary", size="sm", active=True),
                ], className="mb-3 me-3"),
                
                dbc.Checklist(
                    options=[
                        {"label": "SMA 20", "value": "sma20"},
                        {"label": "SMA 50", "value": "sma50"},
                        {"label": "BOLLINGER BANDS", "value": "bb"},
                        {"label": "RSI PANEL", "value": "rsi"},
                        {"label": "MACD INTEGRATION", "value": "macd"}
                    ],
                    value=[],
                    id="technical-toggles",
                    inline=True,
                    style={"display": "inline-block", "color": "#c8d8f0", "fontSize": "12px"}
                ),
                dbc.Spinner(dcc.Graph(id="main-stock-chart", style={"height": "600px"}), color="success")
            ], className="terminal-panel")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("CORPORATE OPERATIONAL METADATA", className="terminal-header"),
                html.H4(id="comp-name", style={"color": "#ffcc44"}),
                html.P(id="comp-desc", style={"fontSize": "12px", "color": "#c8d8f0", "textAlign": "justify"})
            ], className="terminal-panel", style={"height": "100%"})
        ], width=6),
        dbc.Col([
            html.Div([
                html.Div("KEY METRIC ENGINE ACCOUNTING RATIOS", className="terminal-header"),
                html.Div(id="key-stats-grid")
            ], className="terminal-panel")
        ], width=6)
    ], className="mt-4")
])

@callback(
    [Output("main-stock-chart", "figure"),
     Output("comp-name", "children"),
     Output("comp-desc", "children"),
     Output("key-stats-grid", "children")],
    [Input("stock-search-btn", "n_clicks"),
     Input("btn-1d", "n_clicks"), Input("btn-1w", "n_clicks"), Input("btn-1m", "n_clicks"), Input("btn-3m", "n_clicks"), Input("btn-1y", "n_clicks"),
     Input("technical-toggles", "value")],
    [State("stock-search", "value")]
)
def update_stock_analysis(n_clicks, b1, b2, b3, b4, b5, overlays, ticker):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'btn-1y'
    
    period = "1y"
    if "btn-1d" in triggered_id: period = "1d"
    elif "btn-1w" in triggered_id: period = "5d"
    elif "btn-1m" in triggered_id: period = "1mo"
    elif "btn-3m" in triggered_id: period = "3mo"
    
    ticker_obj = yf.Ticker(ticker)
    df = ticker_obj.history(period=period)
    
    if df.empty:
        return go.Figure(), "SECURITY NOT FOUND", "Verification sequence failed for selected asset identifier token ticker.", ""

    try:
        info = ticker_obj.info
        name = info.get("longName", ticker)
        desc = info.get("longBusinessSummary", "No institutional operational data package cached.")
    except Exception:
        name = ticker
        desc = "System failure connecting to primary indexing asset registry databases."
        info = {}

    # Technical Indicators Algorithm Processing Array Framework
    if "sma20" in overlays or "bb" in overlays:
        df['SMA20'] = df['Close'].rolling(window=20).mean()
    if "sma50" in overlays:
        df['SMA50'] = df['Close'].rolling(window=50).mean()
    if "bb" in overlays:
        std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['SMA20'] + (2 * std)
        df['BB_Lower'] = df['SMA20'] - (2 * std)
    
    use_rsi = "rsi" in overlays
    use_macd = "macd" in overlays
    
    rows = 2
    row_heights = [0.7, 0.3]
    specs = [[{"secondary_y": False}], [{"secondary_y": False}]]
    
    if use_rsi and use_macd:
        rows = 4
        row_heights = [0.5, 0.15, 0.17, 0.18]
        specs = [[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]]
    elif use_rsi or use_macd:
        rows = 3
        row_heights = [0.6, 0.2, 0.2]
        specs = [[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]]

    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.04, row_width=row_heights[::-1], specs=specs)
    
    # Core Financial Architecture Candlestick Matrix Plot
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Price Matrix",
                                 increasing_line_color='#00ff88', decreasing_line_color='#ff4466'), row=1, col=1)
    
    if "sma20" in overlays and 'SMA20' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], name="SMA 20", line=dict(color='#ffcc44', width=1.5)), row=1, col=1)
    if "sma50" in overlays and 'SMA50' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], name="SMA 50", line=dict(color='#4488ff', width=1.5)), row=1, col=1)
    if "bb" in overlays and 'BB_Upper' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name="BB Upper", line=dict(color='rgba(200,216,240,0.4)', dash='dash')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name="BB Lower", line=dict(color='rgba(200,216,240,0.4)', dash='dash'), fill='tonexty'), row=1, col=1)

    # Volume Subplot Integration Framework Processing
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume Data", marker_color='#1e2d42'), row=2, col=1)
    
    current_row = 3
    if use_rsi:
        # Classical 14-day relative strength algorithmic momentum tracking logic
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI (14)", line=dict(color='#ffaa00')), row=current_row, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="#ff4466", row=current_row, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#00ff88", row=current_row, col=1)
        current_row += 1
        
    if use_macd:
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name="MACD Matrix", line=dict(color='#4488ff')), row=current_row, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['Signal'], name="Signal Vector", line=dict(color='#ff4466')), row=current_row, col=1)
        
    fig.update_layout(template="plotly_dark", paper_bgcolor='#111720', plot_bgcolor='#111720', xaxis_rangeslider_visible=False,
                      margin=dict(l=20, r=20, t=20, b=20), font=dict(family="JetBrains Mono"))
    
    # Financial Stats Infrastructure Layout Table
    stats = [
        {"m": "P/E Ratio", "v": f"{info.get('trailingPE', 0):.2f}" if info.get('trailingPE') else "N/A"},
        {"m": "Forward P/E", "v": f"{info.get('forwardPE', 0):.2f}" if info.get('forwardPE') else "N/A"},
        {"m": "Dividend Yield", "v": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "0.00%"},
        {"m": "Beta Risk Structural Marker", "v": f"{info.get('beta', 0):.2f}" if info.get('beta') else "N/A"},
        {"m": "52W Variance High", "v": f"{info.get('fiftyTwoWeekHigh', 0):,.2f}"},
        {"m": "52W Variance Low", "v": f"{info.get('fiftyTwoWeekLow', 0):,.2f}"}
    ]
    
    stats_grid = dbc.Table([
        html.Tbody([
            html.Tr([html.Td(s['m'], style={"color": "#5a7090"}), html.Td(s['v'], style={"color": "#ffcc44", "fontWeight": "700"})]) for s in stats
        ])
    ], borderless=True, dark=True, hover=True, size="sm")
    
    return fig, name, desc, stats_grid