import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, register_page
import dash_ag-grid as dag
import yfinance as yf
import pandas as pd

from components.news_indicator import get_news_impact

register_page(__name__, path="/")

def get_index_card_data():
    indices = {"^GSPC": "S&P 500", "^IXIC": "NASDAQ", "^DJI": "DOW JONES", "^VIX": "VOLATILITY INDEX"}
    cards = []
    try:
        data = yf.download(list(indices.keys()), period="2d", group_by="ticker", timeout=5)
        for ticker, name in indices.items():
            df = data[ticker]
            close = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            diff = close - prev
            pct = (diff / prev) * 100
            
            color = "#00ff88" if diff >= 0 else "#ff4466"
            if ticker == "^VIX": color = "#ff4466" if diff >= 0 else "#00ff88" # Inverse tracking configuration
            sign = "+" if diff >= 0 else ""
            
            cards.append(dbc.Col(html.Div([
                html.Div(name, className="terminal-header"),
                html.H3(f"{close:,.2f}", style={"color": "#c8d8f0", "fontWeight": "700"}),
                html.Div(f"{sign}{diff:,.2f} ({sign}{pct:.2f}%)", style={"color": color, "fontSize": "12px", "fontWeight": "600"})
            ], className="terminal-panel"), width=3))
    except Exception:
        for ticker, name in indices.items():
            cards.append(dbc.Col(html.Div([
                html.Div(name, className="terminal-header"),
                html.H3("OFFLINE", style={"color": "#5a7090"}),
            ], className="terminal-panel"), width=3))
    return cards

layout = html.Div([
    dbc.Row(id="index-cards-row", className="mb-4"),
    
    html.Div([
        html.Div("CORE WATCHLIST MATRIX INDICATOR MONITOR", className="terminal-header"),
        dbc.Spinner(
            dag.AgGrid(
                id="markets-grid",
                className="ag-theme-alpine-dark",
                columnSize="sizeToFit",
                dashGridOptions={"rowSelection": "single", "animateRows": True},
                style={"height": "500px", "width": "100%"}
            ), color="warning"
        )
    ], className="terminal-panel"),
    
    dcc.Interval(id="markets-refresh-interval", interval=60000, n_intervals=0)
])

@callback(
    [Output("index-cards-row", "children"), Output("markets-grid", "rowData"), Output("markets-grid", "columnDefs")],
    Input("markets-refresh-interval", "n_intervals")
)
def update_markets_page_data(n):
    cards = get_index_card_data()
    
    tickers = ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN", "THYAO.IS", "TUPRS.IS", "EREGL.IS", "AKBNK.IS"]
    news_impact = get_news_impact(tickers)
    
    row_data = []
    try:
        for t in tickers:
            ticker_obj = yf.Ticker(t)
            info = ticker_obj.fast_info
            hist = ticker_obj.history(period="7d")
            
            # Formulating functional miniature Sparkline charts using custom scalable raw SVG vectors inside grids
            prices = hist['Close'].tolist() if not hist.empty else [1,1,1,1,1,1,1]
            min_p, max_p = min(prices), max(prices)
            rng = (max_p - min_p) if max_p != min_p else 1
            points = " ".join([f"{(i*15)},{int(30 - ((p - min_p)/rng)*25)}" for i, p in enumerate(prices)])
            sparkline_svg = f"<div><svg width='110' height='30'><polyline fill='none' stroke='#ffcc44' stroke-width='1.5' points='{points}'/></svg></div>"
            
            impact_meta = news_impact.get(t, {"signal": "NEUTRAL", "headline": "No recent systemic impact news detected."})
            
            row_data.append({
                "ticker": t,
                "price": info.last_price,
                "change": ((info.last_price - info.open) / info.open) * 100 if info.open else 0,
                "volume": info.last_volume,
                "mcap": info.market_cap,
                "sparkline": sparkline_svg,
                "impact": f"● {impact_meta['signal']}"
            })
    except Exception:
        pass
        
    column_defs = [
        {"field": "ticker", "headerName": "TICKER", "sortable": True, "filter": True, "checkboxSelection": True},
        {"field": "price", "headerName": "LAST PRICE", "valueFormatter": {"function": "d3.format(',.2f')(params.value)"}},
        {"field": "change", "headerName": "DAILY CHANGE %", "valueFormatter": {"function": "d3.format('+.2f')(params.value) + '%'"},
         "cellStyle": {"styleConditions": [{"condition": "params.value >= 0", "style": {"color": "#00ff88"}}, {"condition": "params.value < 0", "style": {"color": "#ff4466"}}]}},
        {"field": "volume", "headerName": "VOLUME (24H)", "valueFormatter": {"function": "d3.format(',.0f')(params.value)"}},
        {"field": "mcap", "headerName": "MARKET CAP", "valueFormatter": {"function": "d3.format(',.0f')(params.value)"}},
        {"field": "sparkline", "headerName": "7D TREND", "cellRenderer": "markdown", "width": 130},
        {"field": "impact", "headerName": "NEWS IMPACT SIGNAL", "cellStyle": {"styleConditions": [
            {"condition": "params.value.includes('BULLISH')", "style": {"backgroundColor": "rgba(0,255,136,0.15)", "color": "#00ff88", "fontWeight": "700"}},
            {"condition": "params.value.includes('BEARISH')", "style": {"backgroundColor": "rgba(255,68,102,0.15)", "color": "#ff4466", "fontWeight": "700"}}
        ]}}
    ]
    
    return cards, row_data, column_defs

@callback(
    Output("url", "pathname"),
    Input("markets-grid", "selectedRows"),
    prevent_initial_call=True
)
def navigate_to_stock_detail(selected_rows):
    if selected_rows:
        return "/stock"
    return dash.no_update