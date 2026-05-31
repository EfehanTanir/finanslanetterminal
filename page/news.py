import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, register_page
import feedparser
from textblob import TextBlob
from datetime import datetime

register_page(__name__, path="/news")

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("STRATEGIC NLP REAL-TIME FILTER PRESETS", className="terminal-header"),
                dbc.RadioItems(
                    id="news-sentiment-filter",
                    options=[
                        {"label": "COMPREHENSIVE SYSTEMS FEED", "value": "ALL"},
                        {"label": "HIGH-CONVICTION BULLISH METRICS", "value": "BULLISH"},
                        {"label": "SYSTEMIC RISK BEARISH CHANNELS", "value": "BEARISH"}
                    ],
                    value="ALL",
                    inline=True,
                    style={"color": "#c8d8f0", "fontSize": "12px"}
                )
            ], className="terminal-panel")
        ], width=12)
    ], className="mb-4"),
    
    dbc.Spinner(html.Div(id="news-feed-target-mount"), color="warning"),
    dcc.Interval(id="news-page-refresh", interval=300000, n_intervals=0)
])

@callback(
    Output("news-feed-target-mount", "children"),
    [Input("news-sentiment-filter", "value"), Input("news-page-refresh", "n_intervals")]
)
def refresh_intelligence_feed(sentiment_filter, n):
    rss_url = "https://news.google.com/rss/search?q=finance+stock+market&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    
    cards = []
    for entry in feed.entries[:40]:
        title = entry.title
        link = entry.link
        pub_str = entry.get('published', datetime.now().strftime("%Y-%m-%d"))
        
        blob = TextBlob(title)
        polarity = blob.sentiment.polarity
        
        sig = "NEUTRAL"
        badge_color = "secondary"
        text_color = "#4488ff"
        
        if polarity > 0.08:
            sig = "BULLISH"
            badge_color = "success"
            text_color = "#00ff88"
        elif polarity < -0.08:
            sig = "BEARISH"
            badge_color = "danger"
            text_color = "#ff4466"
            
        if sentiment_filter != "ALL" and sig != sentiment_filter:
            continue
            
        cards.append(html.Div([
            dbc.Row([
                dbc.Col([
                    html.Span(f"[{sig}]", style={"color": text_color, "fontWeight": "700", "marginRight": "10px"}),
                    html.A(title, href=link, target="_blank", style={"color": "#c8d8f0", "textDecoration": "none", "fontWeight": "500", "fontSize": "14px"}),
                    html.Div(f"SOURCE FEED OVERLAY MONITOR | TIMESTAMP: {pub_str}", style={"color": "#5a7090", "fontSize": "10px", "marginTop": "5px"})
                ], width=10),
                dbc.Col([
                    html.Div(f"SCORE: {polarity:+.2f}", style={"color": text_color, "fontSize": "11px", "textAlign": "right", "fontWeight": "700"})
                ], width=2)
            ])
        ], className="terminal-panel", style={"padding": "12px", "marginBottom": "10px"}))
        
    return cards if cards else html.Div("No tracking parameters matched criteria current structural system snapshot.", style={"color": "#5a7090"})