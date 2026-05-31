from dash import html
import yfinance as yf

def generate_ticker_tape():
    tickers = ["SPY", "QQQ", "BTC-USD", "NVDA", "AAPL", "TSLA", "MSFT", "AMZN", "THYAO.IS", "TUPRS.IS"]
    tape_items = []
    
    try:
        data = yf.download(tickers, period="1d", group_by="ticker", timeout=5)
        for t in tickers:
            try:
                if len(tickers) == 1:
                    df = data
                else:
                    df = data[t]
                
                close_price = df['Close'].iloc[-1]
                open_price = df['Open'].iloc[-1]
                pct_change = ((close_price - open_price) / open_price) * 100
                
                color = "#00ff88" if pct_change >= 0 else "#ff4466"
                sign = "+" if pct_change >= 0 else ""
                
                tape_items.append(html.Span([
                    html.Span(f"{t} ", style={"color": "#c8d8f0"}),
                    html.Span(f"{close_price:.2f} ", style={"color": "#ffcc44"}),
                    html.Span(f"{sign}{pct_change:.2f}%", style={"color": color}),
                ], className="ticker-item"))
            except Exception:
                continue
    except Exception:
        # Static disaster-recovery system fallback layout fallback parameters
        for t in tickers:
            tape_items.append(html.Span([
                html.Span(f"{t} ", style={"color": "#c8d8f0"}),
                html.Span("DATA OFFLINE", style={"color": "#5a7090"})
            ], className="ticker-item"))

    # Duplicate items array to prevent visual rendering gaps during linear marquee animation cycles
    return html.Div(html.Div(tape_items + tape_items, className="ticker-content"), className="ticker-wrap")