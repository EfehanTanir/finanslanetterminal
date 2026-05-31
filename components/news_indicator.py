import feedparser
from textblob import TextBlob
import re

# Comprehensive Entity Mappings (100+ tokens for semantic routing)
COMPANY_MAP = {
    "nvidia": "NVDA", "apple": "AAPL", "tesla": "TSLA", "microsoft": "MSFT", "amazon": "AMZN",
    "alphabet": "GOOGL", "google": "GOOGL", "meta": "META", "facebook": "META", "netflix": "NFLX",
    "amd": "AMD", "intel": "INTC", "broadcom": "AVGO", "qualcomm": "QCOM", "taiwan semi": "TSM",
    "asml": "ASML", "cisco": "CSCO", "oracle": "ORCL", "adobe": "ADBE", "salesforce": "CRM",
    "berkshire": "BRK-B", "jpmorgan": "JPM", "bank of america": "BAC", "wells fargo": "WFC",
    "citigroup": "C", "goldman sachs": "GS", "morgan stanley": "MS", "blackrock": "BLK",
    "exxon": "XOM", "chevron": "CVX", "conoco": "COP", "marathon": "MPC", "schlumberger": "SLB",
    "johnson & johnson": "JNJ", "eli lilly": "LLY", "merck": "MRK", "abbvie": "ABBV",
    "pfizer": "PFE", "thermo fisher": "TMO", "danaher": "DHR", "walmart": "WMT",
    "home depot": "HD", "costco": "COST", "mcdonald": "MCD", "nike": "NKE", "starbucks": "SBUX",
    "disney": "DIS", "comcast": "CMCSA", "verizon": "VZ", "at&t": "T", "t-mobile": "TMUS",
    "caterpillar": "CAT", "ge aerospace": "GE", "honeywell": "HON", "union pacific": "UNP",
    "boeing": "BA", "united parcel": "UPS", "fedex": "FDX", "linde": "LIN", "sherwin-williams": "SHW",
    "american water": "AWK", "duke energy": "DUK", "southern co": "SO", "nextera": "NEE",
    "procter & gamble": "PG", "pepsico": "PEP", "coca-cola": "KO", "philip morris": "PM",
    "costco wholesale": "COST", "amgen": "AMGN", "medtronic": "MDT", "intuition surgical": "ISRG",
    "visa": "V", "mastercard": "MA", "paypal": "PYPL", "uber": "UBER", "airbnb": "ABNB",
    # BIST Stock Mappings
    "turk hava": "THYAO.IS", "turkish airlines": "THYAO.IS", "thy": "THYAO.IS",
    "tupras": "TUPRS.IS", "tüpraş": "TUPRS.IS", "eregli": "EREGL.IS", "ereğli": "EREGL.IS",
    "akbank": "AKBNK.IS", "garanti": "GARAN.IS", "is bank": "ISCTR.IS", "isbank": "ISCTR.IS",
    "yapi kredi": "YKBNK.IS", "koc holding": "KCHOL.IS", "koç holding": "KCHOL.IS",
    "sabanci": "SAHOL.IS", "sabancı": "SAHOL.IS", "aselsan": "ASELS.IS", "sise cam": "SISE.IS",
    "sisecam": "SISE.IS", "bim birlesik": "BIMAS.IS", "bimas": "BIMAS.IS", "turkcell": "TCELL.IS",
    "turk telekom": "TTKOM.IS", "ford otosan": "FROTO.IS", "tofas": "TOASO.IS", "tofaş": "TOASO.IS",
    "arcelik": "ARCLK.IS", "arçelik": "ARCLK.IS", "vestel": "VESTL.IS", "petkim": "PETKM.IS",
    "kardemir": "KRDMD.IS", "sasa polyester": "SASA.IS", "sasa": "SASA.IS", "hektas": "HEKTS.IS",
    "hektas": "HEKTS.IS", "kontrolmatik": "KONTR.IS", "miatechk": "MIATK.IS"
}

def get_news_impact(target_tickers=None):
    """
    Parses live Google News RSS via feedparser, matches keywords against corporate structural tokens,
    and returns localized dynamic sentiment signals.
    """
    rss_url = "https://news.google.com/rss/search?q=finance+stocks+market&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    
    impact_dict = {}
    
    for entry in feed.entries[:60]:
        title = entry.title
        desc = entry.get('summary', '')
        combined_text = f"{title} {desc}".lower()
        
        # Calculate sentiment polarity matrix via TextBlob
        blob = TextBlob(combined_text)
        sentiment = blob.sentiment.polarity
        
        signal = "NEUTRAL"
        if sentiment > 0.1:
            signal = "BULLISH"
        elif sentiment < -0.1:
            signal = "BEARISH"
            
        # Parse for tracking references matching our entity map
        for keyword, ticker in COMPANY_MAP.items():
            if target_tickers and ticker not in target_tickers:
                continue
                
            if re.search(r'\b' + re.escape(keyword) + r'\b', combined_text):
                # High conviction strategy: overwrite if subsequent headline carries higher absolute polarity
                if ticker in impact_dict:
                    if abs(sentiment) > abs(impact_dict[ticker]['score']):
                        impact_dict[ticker] = {"signal": signal, "headline": title, "score": sentiment}
                else:
                    impact_dict[ticker] = {"signal": signal, "headline": title, "score": sentiment}
                    
    return impact_dict