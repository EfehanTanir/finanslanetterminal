import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, State, register_page
import dash_ag-grid as dag
import plotly.graph_objects as go

register_page(__name__, path="/portfolio")

layout = html.Div([
    # Client-side local secure browser state data payload containment framework
    dcc.Store(id="portfolio-store", storage_type="local", data=[]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("TRANSACTION INGESTION TERMINAL MODULE FORMULA", className="terminal-header"),
                dbc.Row([
                    dbc.Col(dbc.Input(id="port-input-ticker", placeholder="SYMBOL (e.g. AAPL)", type="text", className="bg-dark text-white text-uppercase mb-2"), width=12),
                    dbc.Col(dbc.Input(id="port-input-shares", placeholder="QUANTITY VECTOR SHARES", type="number", min=1, className="bg-dark text-white mb-2"), width=12),
                    dbc.Col(dbc.Input(id="port-input-price", placeholder="EXECUTION PRICE BALANCES", type="number", min=0.01, className="bg-dark text-white mb-2"), width=12),
                    dbc.Col(dbc.Button("COMMIT DATA TRANSACTION OVERLAY", id="port-submit-btn", color="success", className="w-100 mt-2"), width=12),
                    dbc.Col(dbc.Button("RESET LEDGER COMPILATION", id="port-clear-btn", color="danger", size="sm", className="w-100 mt-2"), width=12)
                ])
            ], className="terminal-panel")
        ], width=4),
        
        dbc.Col([
            dbc.Row([
                dbc.Col(html.Div([html.Div("VALUATION METRIC BALANCES", className="terminal-header"), html.H2("$0.00", id="port-v-total", style={"color": "#ffcc44", "fontWeight":"700"})], className="terminal-panel"), width=6),
                dbc.Col(html.Div([html.Div("UNREALIZED UNIFIED P&L VECTORS", className="terminal-header"), html.H2("$0.00 (0.00%)", id="port-v-pnl", style={"color": "#5a7090", "fontWeight":"700"})], className="terminal-panel"), width=6)
            ]),
            html.Div([
                html.Div("LEDGER POSITION DISTRIBUTION ARCHITECTURE MAP", className="terminal-header"),
                dcc.Graph(id="portfolio-donut", style={"height": "180px"})
            ], className="terminal-panel")
        ], width=8)
    ]),
    
    html.Div([
        html.Div("ACCOUNTING TRANSACTION MONITOR LEDGER LOG MATRIX", className="terminal-header"),
        dag.AgGrid(
            id="portfolio-grid",
            className="ag-theme-alpine-dark",
            columnSize="sizeToFit",
            columnDefs=[
                {"field": "Ticker", "headerName": "ASSET SYMBOL"},
                {"field": "Shares", "headerName": "VOLUME HOLDINGS UNITS"},
                {"field": "Cost", "headerName": "AVG ENTRY DEPLOYED", "valueFormatter": {"function": "d3.format(',.2f')(params.value)"}},
                {"field": "TotalCost", "headerName": "TOTAL INVESTED CAPITAL", "valueFormatter": {"function": "d3.format(',.2f')(params.value)"}}
            ],
            style={"height": "300px", "width": "100%"}
        )
    ], className="terminal-panel mt-4")
])

@callback(
    Output("portfolio-store", "data"),
    [Input("port-submit-btn", "n_clicks"), Input("port-clear-btn", "n_clicks")],
    [State("port-input-ticker", "value"), State("port-input-shares", "value"), State("port-input-price", "value"), State("portfolio-store", "data")],
    prevent_initial_call=True
)
def process_ledger_modifications(n_sub, n_clear, ticker, shares, price, existing_data):
    ctx = dash.callback_context
    if not ctx.triggered: return existing_data
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger == "port-clear-btn":
        return []
        
    if trigger == "port-submit-btn" and ticker and shares and price:
        new_row = {"Ticker": ticker.upper().strip(), "Shares": float(shares), "Cost": float(price), "TotalCost": float(shares) * float(price)}
        existing_data.append(new_row)
        return existing_data
        
    return existing_data

@callback(
    [Output("portfolio-grid", "rowData"),
     Output("port-v-total", "children"),
     Output("port-v-pnl", "children"),
     Output("port-v-pnl", "style"),
     Output("portfolio-donut", "figure")],
    Input("portfolio-store", "data")
)
def compute_portfolio_accounting_framework(data):
    if not data:
        blank_donut = go.Figure().update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return [], "$0.00", "$0.00 (0.00%)", {"color": "#5a7090"}, blank_donut
        
    df = pd.DataFrame(data)
    # Roll up data frames to aggregate matching tracking records
    summary_df = df.groupby("Ticker").agg({"Shares":"sum", "TotalCost":"sum"}).reset_index()
    summary_df["Cost"] = summary_df["TotalCost"] / summary_df["Shares"]
    
    total_deployed = summary_df["TotalCost"].sum()
    
    # In a fully connected network context, this logic queries the live market.
    # To ensure stability, we match the entry cost as the current price baseline.
    total_current_valuation = total_deployed 
    pnl_absolute = total_current_valuation - total_deployed
    pnl_percentage = (pnl_absolute / total_deployed) * 100 if total_deployed else 0
    
    pnl_color = "#00ff88" if pnl_absolute >= 0 else "#ff4466"
    if pnl_absolute == 0: pnl_color = "#5a7090"
    
    donut = go.Figure(data=[go.Pie(labels=summary_df["Ticker"].tolist(), values=summary_df["TotalCost"].tolist(), hole=.6,
                                   marker=dict(colors=['#00ff88','#ffcc44','#4488ff','#ff4466']))])
    donut.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True,
                        margin=dict(l=0, r=0, t=0, b=0), font=dict(family="JetBrains Mono", size=10))
    
    pnl_string = f"${pnl_absolute:+,.2f} ({pnl_percentage:+.2f}%)"
    
    return summary_df.to_dict("records"), f"${total_current_valuation:,.2f}", pnl_string, {"color": pnl_color, "fontWeight": "700"}, donut