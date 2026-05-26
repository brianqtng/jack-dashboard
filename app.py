"""JACK – The Moat Reaper  |  Yahoo Finance (Stufe 3) + SEC EDGAR (Stufe 1)"""
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import requests

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JACK – The Moat Reaper",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""<style>
/* ── Base & Layout ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
}
.main .block-container { padding-top: 0.8rem; padding-bottom: 1rem; max-width: 1440px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #21262d !important;
}
[data-testid="stSidebar"] * { color: #e6edf3 !important; }

/* ── Header & Titles ── */
.jack-title { color: #e94560; font-size: 1.7em; font-weight: 900; letter-spacing: -0.5px; margin: 0; line-height: 1.2; }
.jack-sub   { color: #8b949e; font-size: 0.8em; margin: 2px 0 0 0; }

/* ── Badges ── */
.badge { display:inline-block; padding:5px 18px; border-radius:5px; font-weight:700; font-size:1em; letter-spacing:0.6px; }
.badge-KAUFEN     { background:#238636; color:#fff; }
.badge-BEOBACHTEN { background:#d29922; color:#0d1117; }
.badge-SCHROTT    { background:#da3633; color:#fff; }

/* ── Score Bar ── */
.score-wrap { margin:8px 0; }
.score-bg   { background:#21262d; border-radius:4px; height:10px; overflow:hidden; }
.score-fill { height:100%; border-radius:4px; }

/* ── Metric Tiles ── */
.mtile  { background:#161b22; border:1px solid #21262d; border-radius:6px; padding:9px 11px; text-align:center; margin-bottom:5px; }
.mlabel { font-size:0.65em; color:#8b949e; text-transform:uppercase; letter-spacing:0.9px; }
.mvalue { font-size:1.25em; font-weight:700; color:#e6edf3; margin-top:2px; }

/* ── Welcome Screen ── */
.welcome { background:#161b22; border:1px dashed #30363d; border-radius:8px; padding:28px; text-align:center; color:#8b949e; }

/* ── Inputs (Text, Select, Radio) ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
div[data-baseweb="input"] input {
    background-color: #161b22 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #e94560 !important;
    box-shadow: 0 0 0 2px #e9456033 !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #161b22 !important;
    border-bottom: 1px solid #21262d !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: #8b949e !important;
    border-bottom: 2px solid transparent !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #e6edf3 !important;
    border-bottom: 2px solid #e94560 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary {
    color: #e6edf3 !important;
    background: #161b22 !important;
}

/* ── DataFrames / Tables ── */
[data-testid="stDataFrame"] { background-color: #161b22 !important; border-radius: 8px; }
[data-testid="stDataFrame"] [data-testid="glideDataGridContainer"] { background: #161b22 !important; }
/* Column headers */
[data-testid="stDataFrame"] .dvn-scroller .gdg-header-row,
[data-testid="stDataFrame"] .header-cell { background: #21262d !important; color: #8b949e !important; }
/* Cell text — explicitly light on dark */
[data-testid="stDataFrame"] .cell-container,
[data-testid="stDataFrame"] .dvn-scroller { color: #e6edf3 !important; }
/* Fallback for plain HTML tables inside st.table() */
table { border-collapse: collapse; width: 100%; }
table th { background: #21262d !important; color: #8b949e !important; padding: 6px 10px; font-size: 0.78em; text-transform: uppercase; border: 1px solid #30363d; }
table td { background: #161b22 !important; color: #e6edf3 !important; padding: 6px 10px; border: 1px solid #21262d; font-size: 0.85em; }
table tr:hover td { background: #1c2128 !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 10px 12px;
}
[data-testid="stMetricLabel"] { color: #8b949e !important; font-size: 0.72em !important; }
[data-testid="stMetricValue"] { color: #e6edf3 !important; }
[data-testid="stMetricDelta"] { font-size: 0.8em !important; }

/* ── Alerts / Info / Warning / Error ── */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left-width: 4px !important;
}

/* ── Buttons ── */
[data-testid="stButton"] button {
    background: #21262d !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    transition: all 0.15s;
}
[data-testid="stButton"] button:hover {
    background: #30363d !important;
    border-color: #e94560 !important;
}
[data-testid="stButton"] button[kind="primary"] {
    background: #e94560 !important;
    border-color: #e94560 !important;
    color: #fff !important;
}

/* ── Radio & Checkbox ── */
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label { color: #e6edf3 !important; }

/* ── Divider ── */
hr { border-color: #21262d !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #484f58; }

/* ── Caption / Small text ── */
[data-testid="stCaptionContainer"] { color: #8b949e !important; }
small, .stCaption { color: #8b949e !important; }

/* ── Progress Bar ── */
[data-testid="stProgress"] > div { background: #21262d !important; }
[data-testid="stProgress"] > div > div { background: #e94560 !important; }
</style>""", unsafe_allow_html=True)

# ── Low-level helpers ─────────────────────────────────────────────────────────
def _v(df: pd.DataFrame, *rows, col: int = 0):
    """Safely read a float from a yfinance DataFrame by row name(s) and column index."""
    for row in rows:
        try:
            if row in df.index:
                val = df.loc[row].iloc[col]
                if pd.notna(val):
                    return float(val)
        except Exception:
            pass
    return None

def _i(info: dict, *keys):
    """Safely read a value from yfinance info dict."""
    for k in keys:
        v = info.get(k)
        if v is not None and v != "N/A":
            if isinstance(v, float) and np.isnan(v):
                continue
            return v
    return None

def pct(v):
    return f"{v:.1%}" if v is not None else "N/V"

def xfmt(v):
    return f"{v:.1f}x" if v is not None else "N/V"

def dfmt(v):
    return f"{v:.0f}d" if v is not None else "N/V"

def nfmt(v):
    return f"{v:.1f}" if v is not None else "N/V"

def cap_fmt(v):
    if v is None:
        return "N/V"
    if v >= 1e12:
        return f"${v/1e12:.2f}T"
    if v >= 1e9:
        return f"${v/1e9:.1f}B"
    if v >= 1e6:
        return f"${v/1e6:.0f}M"
    return f"${v:.0f}"

# ══════════════════════════════════════════════════════════════════════════════
# SEC EDGAR  –  Stufe 1 Primärquelle (kostenlos, kein API-Key)
# data.sec.gov  |  XBRL-Finanzdaten aus 10-K / 10-Q
# ══════════════════════════════════════════════════════════════════════════════

_SEC_HEADERS = {"User-Agent": "JACK-Dashboard research@jack-moat-reaper.com"}

@st.cache_data(ttl=86400, show_spinner=False)   # 24h Cache für CIK-Lookup
def _sec_cik(ticker: str) -> object:
    """CIK aus SEC company_tickers.json ermitteln."""
    try:
        r = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers=_SEC_HEADERS, timeout=8)
        if r.status_code == 200:
            for v in r.json().values():
                if v.get("ticker", "").upper() == ticker.upper():
                    return str(v["cik_str"]).zfill(10)
    except Exception:
        pass
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def _sec_facts(cik: str) -> dict:
    """XBRL Company Facts aus SEC EDGAR laden."""
    try:
        r = requests.get(
            f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
            headers=_SEC_HEADERS, timeout=12)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {}

def _sec_annual(facts: dict, *concepts: str) -> object:
    """Letzten Jahreswert (10-K) für ein GAAP-Konzept extrahieren."""
    us = facts.get("facts", {}).get("us-gaap", {})
    for c in concepts:
        entries = us.get(c, {}).get("units", {}).get("USD", [])
        annual  = [e for e in entries if e.get("form") == "10-K"]
        if annual:
            return float(sorted(annual, key=lambda x: x["end"], reverse=True)[0]["val"])
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_sec(ticker: str) -> dict:
    """Vollständiger SEC-Fetch für einen US-Ticker. Gibt [STUFE1] Daten zurück."""
    cik = _sec_cik(ticker)
    if not cik:
        return {"available": False,
                "reason": "Kein CIK — nicht-US Aktie oder Ticker unbekannt bei SEC"}

    facts = _sec_facts(cik)
    if not facts:
        return {"available": False, "reason": "SEC EDGAR API nicht erreichbar"}

    entity = facts.get("entityName", ticker)

    # Umsatz — verschiedene GAAP-Bezeichnungen
    revenue = _sec_annual(facts,
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
        "SalesRevenueNet",
        "SalesRevenueGoodsNet")

    net_inc  = _sec_annual(facts, "NetIncomeLoss")
    op_inc   = _sec_annual(facts, "OperatingIncomeLoss")
    gross_p  = _sec_annual(facts, "GrossProfit")
    assets   = _sec_annual(facts, "Assets")
    equity   = _sec_annual(facts,
        "StockholdersEquity",
        "StockholdersEquityAttributableToParent")
    lt_debt  = _sec_annual(facts,
        "LongTermDebt",
        "LongTermDebtNoncurrent",
        "LongTermDebtAndCapitalLeaseObligations")
    r_and_d  = _sec_annual(facts, "ResearchAndDevelopmentExpense")
    sbc_sec  = _sec_annual(facts, "ShareBasedCompensation",
        "ShareBasedCompensationArrangementByShareBasedPaymentAwardEquityInstrumentsOtherThanOptionsGrantsInPeriodWeightedAverageGrantDateFairValue")

    return {
        "available": True,
        "cik": cik,
        "entity": entity,
        "revenue": revenue,
        "net_income": net_inc,
        "op_income": op_inc,
        "gross_profit": gross_p,
        "assets": assets,
        "equity": equity,
        "lt_debt": lt_debt,
        "r_and_d": r_and_d,
        "sbc": sbc_sec,
        "sec_url": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-K&owner=include&count=10",
        "edgar_url": f"https://data.sec.gov/submissions/CIK{cik}.json",
        "source": "[STUFE 1] SEC EDGAR / 10-K Filing",
    }


def _cross_validate(yf_val, sec_val) -> dict:
    """Vergleicht yfinance vs SEC-Wert und bestimmt Abweichungs-Tag."""
    if yf_val is None or sec_val is None or sec_val == 0:
        return {"tag": "N/V", "color": "#8b949e", "delta_pct": None, "note": "Kein Vergleich möglich"}
    delta = abs(yf_val - sec_val) / abs(sec_val)
    if delta <= 0.10:
        return {"tag": "SAUBER", "color": "#3fb950", "delta_pct": delta,
                "note": f"≤10% Abweichung ({delta:.1%}) — [VERIFIED] ohne Einschränkung"}
    elif delta <= 0.20:
        return {"tag": "DISKREPANZ", "color": "#d29922", "delta_pct": delta,
                "note": f"10–20% Abweichung ({delta:.1%}) — [VERIFIED] + ⚠️ DISKREPANZ-FLAG (SEC dominiert)"}
    else:
        return {"tag": "ERKLÄRUNGSPFLICHT", "color": "#da3633", "delta_pct": delta,
                "note": f">20% Abweichung ({delta:.1%}) — prüfe Definitionen (TTM vs FY, Adjustments)"}


# ── SMART TICKER RESOLVER (ISIN / WKN / Firmenname → Ticker) ─────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def _search_ticker_yahoo(query: str) -> str:
    """Yahoo Finance Suche: Firmenname → bester Ticker-Treffer."""
    try:
        resp = requests.get(
            "https://query2.finance.yahoo.com/v1/finance/search",
            params={"q": query, "quotesCount": 6, "newsCount": 0, "enableFuzzyQuery": True},
            headers={"User-Agent": "Mozilla/5.0 (compatible; JACK/1.0)"},
            timeout=6,
        )
        data = resp.json()
        quotes = data.get("quotes", [])
        # Bevorzuge Aktien (EQUITY) und ETFs, dann alles andere
        for q in quotes:
            if q.get("quoteType") in ("EQUITY", "ETF"):
                return q.get("symbol", "")
        return quotes[0].get("symbol", "") if quotes else ""
    except Exception:
        return ""


@st.cache_data(ttl=3600, show_spinner=False)
def _isin_to_ticker(isin: str) -> str:
    """OpenFIGI API: ISIN → Yahoo Finance Ticker."""
    try:
        resp = requests.post(
            "https://api.openfigi.com/v3/mapping",
            json=[{"idType": "ID_ISIN", "idValue": isin}],
            headers={"Content-Type": "application/json"},
            timeout=6,
        )
        data = resp.json()
        if not data or not data[0].get("data"):
            # Fallback: Yahoo Finance Search mit ISIN direkt
            return _search_ticker_yahoo(isin)
        # Bevorzuge US/bekannte Börsen
        _pref = ("US", "UW", "UN", "UA", "GQ", "GS", "GM", "NA", "LN", "PA", "EB")
        for exch in _pref:
            for item in data[0]["data"]:
                if item.get("exchCode", "") == exch:
                    return item.get("ticker", "")
        return data[0]["data"][0].get("ticker", "")
    except Exception:
        return _search_ticker_yahoo(isin)


def resolve_input(raw: str) -> tuple:
    """
    Löst Ticker / ISIN / WKN / Firmenname zu einem yfinance-Ticker auf.
    Returns: (ticker: str, label: str, error: str|None)
    """
    inp = raw.strip()
    up  = inp.upper()

    # ── Bereits ein Ticker (kurz, alphanumerisch + Punkt/Bindestrich) ─────────
    if len(up) <= 8 and all(c.isalnum() or c in ".-^=" for c in up):
        return up, "", None

    # ── ISIN: 2 Buchstaben + 10 alphanumerische Zeichen = 12 Zeichen ─────────
    if len(up) == 12 and up[:2].isalpha() and up[2:].isalnum():
        ticker = _isin_to_ticker(up)
        if ticker:
            return ticker, f"ISIN {up} → **{ticker}**", None
        return None, "", f"ISIN {up} konnte nicht aufgelöst werden."

    # ── WKN: 6 alphanumerische Zeichen (keine reine Buchstabenfolge) ──────────
    if len(up) == 6 and up.isalnum():
        # WKN via Yahoo-Suche (füge .DE als Hinweis hinzu)
        ticker = _search_ticker_yahoo(inp)
        if ticker:
            return ticker, f"WKN/Suche '{up}' → **{ticker}**", None
        return None, "", f"WKN {up} nicht gefunden."

    # ── Firmenname: Yahoo Finance Volltext-Suche ──────────────────────────────
    ticker = _search_ticker_yahoo(inp)
    if ticker:
        return ticker, f"'{inp}' → **{ticker}**", None

    return None, "", f"'{inp}' — kein Ticker gefunden."


# ── Data fetching ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch(symbol: str) -> dict:
    try:
        t = yf.Ticker(symbol)
        info = t.info or {}
        if not _i(info, "currentPrice", "regularMarketPrice", "previousClose"):
            hist_check = t.history(period="5d")
            if hist_check.empty:
                return {"error": f"Ticker '{symbol}' nicht gefunden oder kein Handel."}
        fin   = t.financials
        bs    = t.balance_sheet
        cf    = t.cashflow
        q_fin   = t.quarterly_financials
        q_cf    = t.quarterly_cashflow
        hist    = t.history(period="3y")
        try:
            eps_hist = t.earnings_history
        except Exception:
            eps_hist = pd.DataFrame()
        # SEC EDGAR (Stufe 1) — nur für US-Ticker (kein Punkt im Symbol)
        sec = {"available": False, "reason": "Nicht-US Ticker"}
        if "." not in symbol:
            try:
                sec = fetch_sec(symbol)
            except Exception:
                sec = {"available": False, "reason": "SEC-Fetch Fehler"}

        return {
            "info": info, "fin": fin, "bs": bs, "cf": cf,
            "q_fin": q_fin, "q_cf": q_cf,
            "hist": hist, "eps_hist": eps_hist,
            "symbol": symbol.upper(), "sec": sec,
        }
    except Exception as exc:
        return {"error": str(exc)}

# ── Metric calculation ─────────────────────────────────────────────────────────
def calc_metrics(raw: dict) -> dict:  # noqa: C901
    info  = raw.get("info", {})
    fin   = raw.get("fin",  pd.DataFrame())
    bs    = raw.get("bs",   pd.DataFrame())
    cf    = raw.get("cf",   pd.DataFrame())
    m     = {}

    # Revenues (up to 4 annual columns)
    revenues = [r for r in [_v(fin, "Total Revenue", col=i) for i in range(4)] if r]
    m["revenue"]  = revenues[0] if revenues else None
    m["revenues"] = revenues

    # Revenue CAGR
    if len(revenues) >= 3:
        m["rev_cagr"] = (revenues[0] / revenues[-1]) ** (1 / (len(revenues) - 1)) - 1

    # Gross Margin
    gp = _v(fin, "Gross Profit")
    if gp and m["revenue"]:
        m["gross_margin"] = gp / m["revenue"]
    m["_gp"] = gp; m["_gp_prev"] = _v(fin, "Gross Profit", col=1)

    # Operating Income + Margin
    op_inc = _v(fin, "Operating Income", "EBIT")
    if op_inc and m["revenue"]:
        m["op_margin"] = op_inc / m["revenue"]
    m["_op_inc"] = op_inc

    # Net Income
    net_inc = _v(fin, "Net Income")
    m["_net_inc"] = net_inc

    # OCF / Capex / FCF
    ocf   = _v(cf, "Total Cash From Operating Activities",
                   "Operating Cash Flow",
                   "Cash Flow From Continuing Operating Activities")
    capex = _v(cf, "Capital Expenditures",
                   "Purchase Of Property Plant And Equipment")
    m["_ocf"] = ocf; m["_capex"] = capex
    if ocf is not None and capex is not None:
        fcf = ocf - abs(capex)
        m["fcf"] = fcf
        if m["revenue"]:
            m["fcf_margin"] = fcf / m["revenue"]

    # SBC
    sbc = _v(cf, "Stock Based Compensation")
    if sbc and m["revenue"]:
        m["sbc_intensity"] = abs(sbc) / m["revenue"]
    m["sbc_abs"] = abs(sbc) if sbc else 0   # raw SBC amount for Real-FCF calc

    # Capex ratio
    if capex and m["revenue"]:
        m["capex_ratio"] = abs(capex) / m["revenue"]

    # Balance sheet items
    assets     = _v(bs, "Total Assets")
    equity     = _v(bs, "Total Stockholder Equity", "Stockholders Equity", "Common Stock Equity")
    total_debt = _v(bs, "Total Debt")
    if total_debt is None:
        std = _v(bs, "Short Long Term Debt", "Current Debt") or 0
        ltd = _v(bs, "Long Term Debt") or 0
        total_debt = (std + ltd) if (std or ltd) else None
    cash      = _v(bs, "Cash And Cash Equivalents",
                      "Cash Cash Equivalents And Short Term Investments")
    cur_assets = _v(bs, "Current Assets", "Total Current Assets")
    cur_liab   = _v(bs, "Current Liabilities", "Total Current Liabilities")
    inventory  = _v(bs, "Inventory")
    ar         = _v(bs, "Net Receivables", "Receivables")
    ap         = _v(bs, "Accounts Payable", "Payables")
    lt_debt    = _v(bs, "Long Term Debt")

    m.update({
        "_assets": assets, "_equity": equity, "_total_debt": total_debt,
        "_cash": cash, "_cur_assets": cur_assets, "_cur_liab": cur_liab,
        "_lt_debt": lt_debt, "_inventory": inventory, "_ar": ar, "_ap": ap,
    })

    # Current Ratio
    if cur_assets and cur_liab:
        m["current_ratio"] = cur_assets / cur_liab

    # EBITDA → Net Debt / EBITDA
    ebitda = _i(info, "ebitda")
    if ebitda is None and op_inc:
        da     = _v(cf, "Depreciation", "Depreciation And Amortization") or 0
        ebitda = op_inc + da
    if total_debt is not None and cash is not None:
        net_debt = total_debt - cash
        m["net_debt"] = net_debt
        if ebitda and ebitda > 0:
            m["nd_ebitda"] = net_debt / ebitda

    # ROIC  = NOPAT / Invested Capital
    if op_inc and equity is not None and total_debt is not None and cash is not None:
        pretax = _v(fin, "Pretax Income", "Income Before Tax")
        tax    = _v(fin, "Income Tax Expense", "Tax Provision")
        tr     = max(0.0, min(0.5, tax / pretax)) if (pretax and tax and pretax > 0) else 0.25
        nopat  = op_inc * (1 - tr)
        ic     = equity + (total_debt or 0) - (cash or 0)
        if ic > 0:
            m["roic"] = nopat / ic

    # EPS growth (1Y proxy from yfinance info)
    eg = _i(info, "earningsGrowth")
    if eg is not None:
        m["eps_cagr"] = float(eg)

    # Operating Leverage
    if len(revenues) >= 2 and revenues[1] and revenues[1] > 0:
        rev_g  = revenues[0] / revenues[1] - 1
        op_prev = _v(fin, "Operating Income", "EBIT", col=1)
        if op_inc and op_prev and op_prev != 0:
            op_g = (op_inc - op_prev) / abs(op_prev)
            m["op_leverage"] = bool(op_g > rev_g and rev_g > 0)

    # CCC
    cogs = _v(fin, "Cost Of Revenue", "Cost of Revenue")
    if inventory and cogs and cogs > 0:
        m["dio"] = (inventory / cogs) * 365
    if ar and m.get("revenue") and m["revenue"] > 0:
        m["dso"] = (ar / m["revenue"]) * 365
    if ap and cogs and cogs > 0:
        m["dpo"] = (ap / cogs) * 365
    if "dio" in m and "dso" in m and "dpo" in m:
        m["ccc"] = m["dio"] + m["dso"] - m["dpo"]

    # Market data from info
    m["price"]    = _i(info, "currentPrice", "regularMarketPrice", "previousClose")
    m["currency"] = _i(info, "currency") or "USD"
    m["name"]     = _i(info, "longName", "shortName")
    m["sector"]   = _i(info, "sector")
    m["industry"] = _i(info, "industry")
    m["mktcap"]   = _i(info, "marketCap")
    m["ev"]       = _i(info, "enterpriseValue")
    m["pe"]       = _i(info, "trailingPE")
    m["fwd_pe"]   = _i(info, "forwardPE")
    m["beta"]     = _i(info, "beta")
    m["hi52"]     = _i(info, "fiftyTwoWeekHigh")
    m["lo52"]     = _i(info, "fiftyTwoWeekLow")
    m["dividend"] = _i(info, "dividendYield")

    if m.get("fcf") and m.get("ev") and m["ev"] > 0 and m["fcf"] > 0:
        m["ev_fcf"] = m["ev"] / m["fcf"]

    # Netto Cash (positiv = Cash-reich, negativ = verschuldet)
    if cash is not None and total_debt is not None:
        m["net_cash"] = cash - total_debt

    # Jährliche EBITDA-Reihe (für Chart)
    ebitda_series = []
    for i in range(4):
        oi = _v(fin, "Operating Income", "EBIT", col=i)
        da = _v(cf, "Depreciation", "Depreciation And Amortization", col=i) or 0
        if oi is not None:
            ebitda_series.append(oi + abs(da))
        else:
            ebitda_series.append(None)
    m["ebitda_series"] = ebitda_series

    # EBITDA-Marge-Reihe
    m["ebitda_margin_series"] = [
        (e / r) if (e and r) else None
        for e, r in zip(ebitda_series, revenues + [None] * 4)
    ]

    # Quartalsdaten (letzte 4 Quartale)
    q_fin = raw.get("q_fin", pd.DataFrame())
    q_cf  = raw.get("q_cf",  pd.DataFrame())
    quarters = []
    for i in range(min(4, len(q_fin.columns) if not q_fin.empty else 0)):
        q_rev  = _v(q_fin, "Total Revenue", col=i)
        q_oi   = _v(q_fin, "Operating Income", "EBIT", col=i)
        q_da   = _v(q_cf,  "Depreciation", "Depreciation And Amortization", col=i) or 0
        q_ni   = _v(q_fin, "Net Income", col=i)
        q_gp   = _v(q_fin, "Gross Profit", col=i)
        q_ebitda = (q_oi + abs(q_da)) if q_oi is not None else None
        # YoY: compare with same quarter last year (col i+4)
        q_rev_yoy = None
        if not q_fin.empty and i + 4 < len(q_fin.columns):
            rev_prev_yoy = _v(q_fin, "Total Revenue", col=i + 4)
            if q_rev and rev_prev_yoy and rev_prev_yoy != 0:
                q_rev_yoy = (q_rev - rev_prev_yoy) / abs(rev_prev_yoy)
        if not q_fin.empty and i < len(q_fin.columns):
            ts  = q_fin.columns[i]
            qn  = (ts.month - 1) // 3 + 1
            col_label = f"Q{qn} '{ts.strftime('%y')}"
        else:
            col_label = f"Q-{i}"
        quarters.append({
            "Quartal":      col_label,
            "Umsatz ($M)":  round(q_rev  / 1e6, 1) if q_rev   else None,
            "YoY %":        f"{q_rev_yoy:+.1%}" if q_rev_yoy is not None else "N/V",
            "EBITDA ($M)":  round(q_ebitda / 1e6, 1) if q_ebitda else None,
            "EBITDA-Marge": f"{q_ebitda/q_rev:.1%}" if (q_ebitda and q_rev) else "N/V",
            "Nettogew. ($M)": round(q_ni / 1e6, 1) if q_ni else None,
        })
    m["quarters"] = quarters

    # Piotroski F-Score
    m["piotroski"] = _calc_piotroski(fin, bs, cf)

    # Extra fundamentals from info
    m["employees"]       = _i(info, "fullTimeEmployees")
    m["country"]         = _i(info, "country")
    m["city"]            = _i(info, "city")
    m["description"]     = _i(info, "longBusinessSummary")
    m["target_price"]    = _i(info, "targetMeanPrice")
    m["recommendation"]  = _i(info, "recommendationKey")
    m["analyst_count"]   = _i(info, "numberOfAnalystOpinions")
    m["profit_margin"]   = _i(info, "profitMargins")
    m["roe"]             = _i(info, "returnOnEquity")
    m["roa"]             = _i(info, "returnOnAssets")
    m["debt_to_equity"]  = _i(info, "debtToEquity")
    m["price_to_book"]   = _i(info, "priceToBook")
    m["price_to_sales"]  = _i(info, "priceToSalesTrailingTwelveMonths")
    m["revenue_growth"]  = _i(info, "revenueGrowth")
    m["shares_out"]      = _i(info, "sharesOutstanding")
    m["float_pct"]       = _i(info, "floatShares")
    m["short_ratio"]     = _i(info, "shortRatio")
    m["ex_dividend"]     = _i(info, "exDividendDate")
    m["payout_ratio"]    = _i(info, "payoutRatio")
    m["website"]         = _i(info, "website")

    # Equity-Quote (EK-Quote)
    assets_val = _v(bs, "Total Assets")
    equity_val = _v(bs, "Total Stockholder Equity", "Stockholders Equity", "Common Stock Equity")
    if assets_val and equity_val:
        m["equity_ratio"] = equity_val / assets_val

    # EV/EBITDA
    ev_val     = m.get("ev")
    ebitda_val = ebitda_series[0] if ebitda_series else None
    if ev_val and ebitda_val and ebitda_val > 0:
        m["ev_ebitda"] = ev_val / ebitda_val

    # P/FCF  (Preis × Aktien / FCF)
    price_val  = m.get("price")
    shares_val = m.get("shares_out")
    fcf_val    = m.get("fcf")
    if price_val and shares_val and fcf_val and fcf_val > 0:
        mktcap_val   = price_val * shares_val
        m["p_fcf"]   = mktcap_val / fcf_val

    # SBC-Einschätzung
    sbc_i = m.get("sbc_intensity")
    if sbc_i is None:
        m["sbc_flag"] = ("N/V", "#8b949e")
    elif sbc_i > 0.15:
        m["sbc_flag"] = ("HOCH ⚠️", "#da3633")
    elif sbc_i > 0.08:
        m["sbc_flag"] = ("MITTEL", "#d29922")
    else:
        m["sbc_flag"] = ("NIEDRIG", "#3fb950")

    # WACC inputs
    pretax   = _v(fin, "Pretax Income", "Income Before Tax")
    tax_exp  = _v(fin, "Income Tax Expense", "Tax Provision")
    interest = _v(fin, "Interest Expense")
    if pretax and tax_exp and pretax > 0:
        m["tax_rate"] = max(0.0, min(0.50, tax_exp / pretax))
    m["interest_expense"] = interest
    m["total_debt"]       = total_debt
    m["shares"]           = _i(info, "sharesOutstanding") or 1

    # Share count history (3 Jahre) aus Bilanz
    _sh_rows = ["Ordinary Shares Number", "Share Issued",
                "Common Stock", "Common Shares Outstanding"]
    _sh_hist = []
    if not bs.empty:
        for _col in bs.columns[:4]:
            _sh_val = None
            for _row in _sh_rows:
                try:
                    _v2 = bs.loc[_row, _col]
                    if _v2 is not None and pd.notna(_v2) and float(_v2) > 1e6:
                        _sh_val = float(_v2)
                        break
                except (KeyError, TypeError, ValueError):
                    continue
            if _sh_val:
                _sh_hist.append({"date": str(_col)[:10], "shares": _sh_val})
    m["share_history"] = _sh_hist

    # Insider / Institutional / Short
    m["insider_pct"] = _i(info, "heldPercentInsiders")
    m["inst_pct"]    = _i(info, "heldPercentInstitutions")
    m["short_pct"]   = _i(info, "shortPercentOfFloat")

    # Buyback / Shareholder Return (cashflow)
    buyback = _v(cf, "Repurchase Of Capital Stock", "Common Stock Repurchased")
    if buyback and m.get("revenue"):
        m["buyback_yield_est"] = abs(buyback) / (m.get("mktcap") or 1)

    # Daten-Hierarchie Tags per Metrik
    m["_tag_price"]   = "LIVE"      # yfinance live price
    m["_tag_fin"]     = "VERIFIED"  # audited annual financials
    m["_tag_est"]     = "ESTIMATE"  # analyst estimates
    m["_tag_train"]   = "TRAINING"  # model knowledge

    # ── SEC EDGAR Stufe-1 Integration & Kreuzvalidierung ──────────────────────
    sec = raw.get("sec", {"available": False})
    m["sec"] = sec

    if sec.get("available"):
        # Kreuzvalidierung: yfinance vs SEC (Primärquelle)
        m["_cv_revenue"]    = _cross_validate(m.get("revenue"),    sec.get("revenue"))
        m["_cv_net_income"] = _cross_validate(m.get("_net_inc"),   sec.get("net_income"))
        m["_cv_op_income"]  = _cross_validate(m.get("_op_inc"),    sec.get("op_income"))
        m["_cv_gross"]      = _cross_validate(m.get("_gp"),        sec.get("gross_profit"))
        m["_cv_assets"]     = _cross_validate(m.get("_assets"),    sec.get("assets"))

        # SEC-Werte als Primärquelle verwenden wo verfügbar (überschreiben yfinance)
        if sec.get("revenue") and m.get("_cv_revenue", {}).get("delta_pct", 1) <= 0.20:
            m["_sec_revenue_used"] = True   # Flag: SEC-Wert für K-Kriterien genutzt

        # Daten-Qualitäts-Tag upgraden wenn SEC-Kreuzvalidierung bestanden
        cv_ok = all(
            m.get(f"_cv_{k}", {}).get("delta_pct", 1) is not None and
            m.get(f"_cv_{k}", {}).get("delta_pct", 1) <= 0.20
            for k in ["revenue", "net_income"]
        )
        m["_stufe"] = "1+3" if cv_ok else "3"  # Daten-Stufe
        m["_stufe_label"] = "[STUFE 1+3] SEC+Yahoo [VERIFIED]" if cv_ok else "[STUFE 3] Yahoo Finance"
    else:
        m["_stufe"] = "3"
        m["_stufe_label"] = "[STUFE 3] Yahoo Finance"
        if "." in raw.get("symbol", ""):
            m["_stufe_label"] += " (Nicht-US: SEC nicht verfügbar)"

    return m

def _calc_piotroski(fin, bs, cf) -> dict:
    s = 0
    d = {}

    assets    = _v(bs, "Total Assets")
    assets_p  = _v(bs, "Total Assets", col=1)
    net_inc   = _v(fin, "Net Income")
    net_inc_p = _v(fin, "Net Income", col=1)
    ocf       = _v(cf, "Total Cash From Operating Activities",
                      "Operating Cash Flow",
                      "Cash Flow From Continuing Operating Activities")
    gp        = _v(fin, "Gross Profit")
    gp_p      = _v(fin, "Gross Profit", col=1)
    rev       = _v(fin, "Total Revenue")
    rev_p     = _v(fin, "Total Revenue", col=1)
    lt_debt   = _v(bs, "Long Term Debt")
    lt_debt_p = _v(bs, "Long Term Debt", col=1)
    ca        = _v(bs, "Current Assets", "Total Current Assets")
    cl        = _v(bs, "Current Liabilities", "Total Current Liabilities")
    ca_p      = _v(bs, "Current Assets", "Total Current Assets", col=1)
    cl_p      = _v(bs, "Current Liabilities", "Total Current Liabilities", col=1)

    roa   = (net_inc   / assets)   if (net_inc   and assets)   else None
    roa_p = (net_inc_p / assets_p) if (net_inc_p and assets_p) else None

    def chk(name, val):
        nonlocal s
        result = bool(val)
        d[name] = result
        s += int(result)

    if roa is not None:              chk("ROA > 0",           roa > 0)
    if ocf is not None:              chk("OCF > 0",           ocf > 0)
    if roa is not None and roa_p:    chk("ΔROA ↑",            roa > roa_p)
    if ocf and assets and roa:       chk("OCF/Assets > ROA",  ocf / assets > roa)
    if lt_debt is not None and lt_debt_p and assets and assets_p:
        chk("Leverage ↓", lt_debt / assets < lt_debt_p / assets_p)
    if ca and cl and ca_p and cl_p:  chk("Liquidität ↑",      ca / cl > ca_p / cl_p)
    if gp and rev and gp_p and rev_p and rev > 0 and rev_p > 0:
        chk("Bruttomarge ↑", gp / rev > gp_p / rev_p)
    if rev and assets and rev_p and assets_p and assets > 0 and assets_p > 0:
        chk("Asset Turnover ↑", rev / assets > rev_p / assets_p)

    return {"score": s, "max": len(d), "details": d}

# ══════════════════════════════════════════════════════════════════════════════
# JACK FRAMEWORK ENGINE  –  DATA INTEGRITY · FLAGS · KONFIDENZ · REAPER SCORE
# ══════════════════════════════════════════════════════════════════════════════

# ── DATA INTEGRITY SYSTEM ─────────────────────────────────────────────────────
TAG_COLOR = {
    # ── JACK Daten-Hierarchie (Stufe 1–4) ─────────────────────────────────────
    "S1":        "#3fb950",   # Stufe 1: SEC-Filings / Investor Relations (Primärquelle)
    "S2":        "#79c0ff",   # Stufe 2: Koyfin / TIKR / StockAnalysis / Macrotrends
    "S3":        "#e3b341",   # Stufe 3: marketscreener / Traderfox (nur Bestätigung)
    "S4":        "#d29922",   # Stufe 4: [ESTIMATE] — nur E-Kriterien & WACC
    "LIVE":      "#388bfd",   # Echtzeitkurs (yfinance)
    "N/V":       "#da3633",   # nicht verfügbar
    # ── Legacy-Aliases (Rückwärtskompatibilität) ───────────────────────────────
    "VERIFIED":  "#3fb950",   # = S1
    "ESTIMATE":  "#d29922",   # = S4
    "TRAINING":  "#8b949e",   # Modell-Trainingsdaten
    "SKIP":      "#8b949e",   # übersprungen (z.B. Beneish ohne SEC-Live)
}

def _tag(label: str) -> str:
    color = TAG_COLOR.get(label, "#8b949e")
    return (f'<span style="background:{color}22;border:1px solid {color};'
            f'color:{color};border-radius:3px;padding:1px 5px;'
            f'font-size:0.68em;font-weight:700;">[{label}]</span>')


# ── SONDERREGELN: K-BASIS AUTO-DETECTION ENGINE ──────────────────────────────
_K_MODE_COLORS = {
    "5S Standard":        "#1f6feb",
    "5F Finanz":          "#d29922",
    "5SaaS":              "#7ee787",
    "5I Infrastruktur":   "#79c0ff",
    "5V Versorger":       "#56d364",
    "5K Sachwerte":       "#e3b341",
    "4P Piotroski":       "#f0883e",
    "5T (Transformation)":"#388bfd",
}

def _auto_detect_k_basis(m: dict) -> tuple:
    """
    Auto-Detection Engine — Prioritäten-Reihenfolge (höhere Priorität gewinnt):
      1. 5F Finanz      → Banking / Insurance / Capital Markets
      2. 5V Versorger   → Utilities (Strom/Wasser/Gas)
      3. 5I Infrastruktur → Airports / Toll / Railways / Pipelines / Towers
      4. 5K Sachwerte   → Mining / Energy / REIT / Basic Materials
      5. 5SaaS          → Software/Tech + Bruttomarge ≥ 65%
      6. 4P Piotroski   → Value-Override: Piotroski ≥ 7 + ROIC < 15% + P/B < 2
      7. 5S Standard    → Default (alle anderen)
      8. 5T Transformation → Wird NACH diesem Call in calc_jack() überschrieben

    Returns: (k_basis: int, mode_label: str, mode_reason: str)
    """
    sector   = (m.get("sector")   or "").lower()
    industry = (m.get("industry") or "").lower()
    gm       = m.get("gross_margin")  or 0
    roic     = m.get("roic")          or 0
    ps       = (m.get("piotroski") or {}).get("score")
    pb       = m.get("price_to_book") or 0

    # ── 1. FINANZSEKTOR (5F) ─────────────────────────────────────────────────
    _fin = ["financial", "bank", "insurance", "diversified financ",
            "capital market", "credit service", "mortgage", "savings",
            "versicherung", "finanzdienstleist"]
    if any(kw in sector or kw in industry for kw in _fin):
        return 5, "5F Finanz", \
            f"Sektor: Finanzbranche ({m.get('sector','—')}) → ROE-basierte K-Kriterien aktiv"

    # ── 2. VERSORGER (5V) ────────────────────────────────────────────────────
    _util = ["utilities", "electric util", "water util", "gas util",
             "gas distribution", "multi-util", "independent power",
             "renewable electric", "power producers"]
    if any(kw in sector or kw in industry for kw in _util):
        return 5, "5V Versorger", \
            f"Sektor: Versorger ({m.get('industry','—')}) → Dividende/EBITDA-Hürden aktiv"

    # ── 3. INFRASTRUKTUR (5I) ────────────────────────────────────────────────
    _infra = ["infrastructure", "airport", "railway", "railroad", "pipeline",
              "toll road", "seaport", "container terminal", "logistics hub",
              "telecom tower", "data center reit", "industrial reit",
              "transportation infrastructure"]
    if any(kw in sector or kw in industry for kw in _infra):
        return 5, "5I Infrastruktur", \
            f"Sektor: Infrastruktur ({m.get('industry','—')}) → EBITDA/Konzessions-Hürden aktiv"

    # ── 4. KAPITALINTENSIVE SACHWERTE (5K) ───────────────────────────────────
    _asset = ["basic material", "energy", "oil", "natural gas", "mining",
              "gold", "silver", "steel", "aluminum", "copper",
              "reit", "real estate", "commodit", "forest", "agriculture"]
    if any(kw in sector or kw in industry for kw in _asset):
        return 5, "5K Sachwerte", \
            f"Sektor: Kapitalintensive Sachwerte ({m.get('sector','—')}) → FCF-Yield/EV-EBITDA aktiv"

    # ── 5. SaaS / HIGH-MARGIN TECH (5SaaS) ───────────────────────────────────
    _tech = ["technology", "software", "saas", "semiconductor", "cloud",
             "internet content", "application software", "systems software"]
    if any(kw in sector or kw in industry for kw in _tech) and gm >= 0.65:
        return 5, "5SaaS", \
            f"SaaS/High-Margin-Tech (GM={pct(gm)}) → Bruttomarge/NRR/ARR-Hürden aktiv"

    # ── 6. PIOTROSKI-OVERRIDE (4P) ───────────────────────────────────────────
    # Value-Play: hoher Piotroski-Score, aber ROIC noch niedrig → Deep Value
    if ps is not None and ps >= 7 and 0 < roic < 0.15 and 0 < pb < 2.0:
        return 4, "4P Piotroski", \
            f"Value-Override: Piotroski={ps}/8, ROIC={pct(roic)}, P/B={pb:.1f}x → Piotroski ist primäres Gate"

    # ── 7. STANDARD (5S) ─────────────────────────────────────────────────────
    return 5, "5S Standard", \
        "Standard-Modus: Alle JACK-Kriterien gemäß 5S-Framework (ROIC/FCF/Leverage/Piotroski/EPS/SBC)"


# ── KLASSE-A FLAGS ─────────────────────────────────────────────────────────────
def _detect_flags(m: dict) -> list[dict]:
    """Returns list of active flag dicts {name, color, reason}."""
    flags = []

    def flag(name, color, reason):
        flags.append({"name": name, "color": color, "reason": reason})

    nd = m.get("nd_ebitda")
    if nd is not None and nd > 4.0:
        flag("DEBT-TRAP", "#da3633", f"Net Debt/EBITDA = {nd:.1f}x (>4x)")

    sbc = m.get("sbc_intensity")
    if sbc is not None and sbc > 0.15:
        flag("SBC-ALARM", "#d29922", f"SBC/Revenue = {pct(sbc)} (>15%)")

    rev_cagr = m.get("rev_cagr")
    if rev_cagr is not None and rev_cagr < 0:
        flag("UMSATZ-RÜCKGANG", "#da3633", f"Rev-CAGR = {pct(rev_cagr)}")

    fcf = m.get("fcf_margin")
    if fcf is not None and fcf < -0.10:
        flag("FCF-NEGATIV", "#da3633", f"FCF-Marge = {pct(fcf)} (<-10%)")

    roic = m.get("roic")
    if roic is not None and roic < 0.05:
        flag("ROIC-SCHWÄCHE", "#d29922", f"ROIC = {pct(roic)} (<5%)")

    return flags


# ── DATEN-KONFIDENZ (SCHRITT 2B) ──────────────────────────────────────────────
def _calc_daten_konfidenz(m: dict) -> dict:
    """
    Schritt 2B — Daten-Konfidenz-Assessment.
    JACK Daten-Hierarchie:
      S1 = SEC-Filings / Investor Relations (Primärquelle)
      S2 = Koyfin / TIKR / StockAnalysis / Macrotrends
      S3 = marketscreener / Traderfox (nur Bestätigung)
      S4 = [ESTIMATE] — nur E-Kriterien & WACC
      LIVE = Echtzeitkurs
      N/V  = nicht verfügbar
    """
    def _item(name: str, field, source_if_avail: str) -> dict:
        avail = field is not None
        tag   = source_if_avail if avail else "N/V"
        conf  = "HOCH"   if avail and tag in ("LIVE", "S1", "S2") else \
                "MITTEL"  if avail and tag in ("S3", "S4") else \
                "NIEDRIG"
        return {"Datenpunkt": name, "✓": "✅" if avail else "❌",
                "Quelle": tag, "Konfidenz": conf}

    piotr = m.get("piotroski", {})
    _rev3 = (m.get("revenues") or [])
    items = [
        # S1 — SEC-Filings (via yfinance annual statements)
        _item("Kursdaten / Preis",       m.get("price"),            "LIVE"),
        _item("Marktkapitalisierung",    m.get("mktcap"),           "LIVE"),
        _item("Umsatz (3+ Jahre)",       _rev3[0] if len(_rev3) >= 3 else None, "S1"),
        _item("Brutto-/Op. Marge",       m.get("gross_margin"),     "S1"),
        _item("FCF-Marge (real/SBC)",    m.get("real_fcf_margin"),  "S1"),
        _item("ROIC",                    m.get("roic"),             "S1"),
        _item("Verschuldung (ND/EBITDA)",m.get("nd_ebitda"),        "S1"),
        _item("Piotroski F-Score",       piotr.get("score") if piotr.get("details") else None, "S1"),
        _item("SBC-Quote",               m.get("sbc_intensity"),    "S1"),
        # S4 — Estimates / berechnete Metriken
        _item("EPS-CAGR",                m.get("eps_cagr"),         "S4"),
        _item("Rev-CAGR",                m.get("rev_cagr"),         "S4"),
        _item("Analysten-Konsens",       m.get("target_price"),     "S4"),
    ]

    available  = sum(1 for it in items if it["✓"] == "✅")
    total      = len(items)
    pct_avail  = available / total if total else 0

    if pct_avail >= 0.85:
        quality, color = "HOCH",    "#3fb950"
    elif pct_avail >= 0.65:
        quality, color = "MITTEL",  "#d29922"
    else:
        quality, color = "NIEDRIG", "#da3633"

    return {
        "items":     items,
        "quality":   quality,
        "color":     color,
        "available": available,
        "total":     total,
        "pct":       pct_avail,
    }


# ── KONFIDENZ-DECKEL ──────────────────────────────────────────────────────────
def _calc_konfidenz_deckel(k_avail: int, k_basis: int, flags: list[dict]) -> tuple:
    """Returns (icon, label, hex_color). Lowest ceiling wins."""
    red_flags = [f for f in flags if f["color"] == "#da3633"]
    if red_flags or k_avail < k_basis - 2:
        return "🔴", "NIEDRIG", "#da3633"
    elif k_avail < k_basis - 1 or len(flags) > 0:
        return "🟡", "MITTEL", "#d29922"
    else:
        return "🟢", "HOCH", "#238636"


# ── REAPER SCORE MIT ANKER-SYSTEM ─────────────────────────────────────────────
def _calc_reaper_score(k_met: int, k_basis: int, e_met: int, e_total: int,
                       m: dict, flags: list[dict]) -> int:
    """Anchor first, then score within the anchor range.
    Anchors: 9–10 (Elite), 6–8 (Solid), 3–5 (Schwach), 1–2 (Schrott)"""
    red_flags   = [f for f in flags if f["color"] == "#da3633"]
    yellow_flags = [f for f in flags if f["color"] == "#d29922"]

    # --- Anchor determination ---
    if k_met >= k_basis and not red_flags:
        anchor_lo, anchor_hi = 9, 10        # Elite
    elif k_met >= k_basis - 1 and not red_flags:
        anchor_lo, anchor_hi = 6, 8         # Solid
    elif k_met >= k_basis - 3 and len(red_flags) <= 1:
        anchor_lo, anchor_hi = 3, 5         # Schwach
    else:
        anchor_lo, anchor_hi = 1, 2         # Schrott

    # --- Fine-score within anchor range ---
    e_ratio  = e_met / e_total if e_total else 0
    ev_fcf   = m.get("ev_fcf")
    pe       = m.get("pe")
    val_pts  = 0.0
    if ev_fcf and 0 < ev_fcf < 20:   val_pts += 1.0
    elif ev_fcf and ev_fcf < 30:      val_pts += 0.5
    if pe and 0 < pe < 20:           val_pts += 0.5

    raw = anchor_lo + (e_ratio * (anchor_hi - anchor_lo)) + val_pts * 0.5
    raw -= len(yellow_flags) * 0.3
    score = max(anchor_lo, min(anchor_hi, round(raw)))

    # ── JACK-Regel: Maximum bei 🔴 Konfidenz = 6/10 ─────────────────────────
    # 🔴 Konfidenz tritt auf bei: roten Flags ODER K-Kriterien stark lückenhaft
    if red_flags:
        score = min(score, 6)

    return score


# ── PERSONA & MANDAT VERDICT ───────────────────────────────────────────────────
def _jack_verdict(rating: str, rs: int, k_met: int, k_basis: int,
                  flags: list[dict], m: dict) -> str:
    """Returns the JACK verdict text block (Persona & Mandat output)."""
    sym   = "€" if m.get("currency") == "EUR" else "$"
    name  = m.get("name", "Dieses Unternehmen")
    mode  = m.get("_k_basis_mode", "5S Standard")

    if rating == "KAUFEN":
        return (f"**{name}** erfüllt alle {k_basis} K-Kriterien ({mode}). "
                f"Der Reaper Score {rs}/10 signalisiert eine **qualitativ hochwertige "
                f"Kapitalanlage** mit nachweisbarem wirtschaftlichem Burggraben. "
                f"Das Unternehmen zeigt strukturelle Überrendite-Eigenschaften.")
    elif rating == "BEOBACHTEN":
        missing = k_basis - k_met
        flag_names = ", ".join(f["name"] for f in flags) if flags else "keine kritischen Flags"
        return (f"**{name}** verfehlt {missing} von {k_basis} K-Kriterien ({mode}). "
                f"Aktive Flags: {flag_names}. "
                f"Reaper Score {rs}/10 – Position auf **Watchlist**, kein Sofortkauf.")
    else:
        flag_names = ", ".join(f["name"] for f in flags) if flags else "strukturelle Schwächen"
        return (f"**{name}** besteht die K-Prüfung nicht ({k_met}/{k_basis} K-Kriterien). "
                f"Flags: {flag_names}. "
                f"Reaper Score {rs}/10. **Kein Investment** – außerhalb des JACK-Universums.")


# ── DREI-KLASSEN PANEL ────────────────────────────────────────────────────────
def _render_drei_klassen(j: dict, m: dict):
    """Rendert das Globale Regeln Drei-Klassen-System als expandierbares Panel."""
    rating = j.get("rating", "SCHROTT")
    rs     = j.get("reaper_score", 1)
    flags  = j.get("flags", [])

    if rating == "KAUFEN":
        klasse, k_color, k_icon = "KLASSE A – KAUFEN",    "#3fb950", "🟢"
        desc = "Alle Pflicht-K-Kriterien erfüllt · Reaper Score ≥ 7 · Keine roten Flags"
    elif rating == "BEOBACHTEN":
        klasse, k_color, k_icon = "KLASSE B – BEOBACHTEN","#d29922", "🟡"
        desc = "1–2 K-Kriterien verfehlt · Reaper Score 4–6 · Watchlist-Kandidat"
    else:
        klasse, k_color, k_icon = "KLASSE C – SCHROTT",   "#da3633", "🔴"
        desc = "≥3 K-Kriterien verfehlt ODER rote Flags aktiv · Kein Investment"

    with st.expander(f"{k_icon} Drei-Klassen-System: **{klasse}**", expanded=False):
        st.markdown(f"<span style='color:{k_color};font-weight:700;'>{desc}</span>",
                    unsafe_allow_html=True)
        st.markdown("---")

        cols = st.columns(3)
        with cols[0]:
            st.markdown("**🟢 Klasse A – KAUFEN**")
            st.markdown("- Alle K erfüllt\n- Score ≥ 7\n- Keine roten Flags\n- Sizing Tier 1–2")
        with cols[1]:
            st.markdown("**🟡 Klasse B – BEOBACHTEN**")
            st.markdown("- 1–2 K fehlen\n- Score 4–6\n- Watchlist\n- Sizing Tier 3")
        with cols[2]:
            st.markdown("**🔴 Klasse C – SCHROTT**")
            st.markdown("- ≥3 K fehlen\n- Score 1–3\n- Rote Flags\n- Sizing Tier 4 (0%)")

        if flags:
            st.markdown("---")
            st.markdown("**⚑ Aktive Flags:**")
            for f in flags:
                st.markdown(
                    f"<span style='color:{f['color']};font-weight:700;'>"
                    f"{f['name']}</span> — {f['reason']}",
                    unsafe_allow_html=True)


# ── JACK SUMMARY BLOCK (OUTPUT-PFLICHT vollständig) ──────────────────────────
def _render_jack_summary(j: dict, m: dict):
    """OUTPUT-PFLICHT: vollständiger JACK-SUMMARY Block per Prompt-Spezifikation."""
    rs      = j.get("reaper_score", 1)
    rating  = j.get("rating", "SCHROTT")
    sizing  = j.get("sizing", "Tier 4 (0%)")
    k_icon, k_label, k_color = j.get("konfidenz", ("🔴", "NIEDRIG", "#da3633"))
    verdict = j.get("verdict", "")
    mode    = m.get("_k_basis_mode", "5S Standard")
    k_met   = j.get("k_met", 0)
    k_basis = j.get("k_basis", 5)
    flags   = j.get("flags", [])
    ab      = j.get("abstauber", "—")
    ec      = j.get("edge_catalyst", {})
    dm      = j.get("debt_maturity", {})
    konv    = j.get("konvergenz", {})
    tiefe   = j.get("analyse_tiefe", "FULL DEEP DIVE")
    wacc_d  = j.get("wacc_data", {})

    # Anker bestimmen
    if rs >= 9:    anker = "9–10 AUSNAHME-COMPOUNDER"
    elif rs >= 6:  anker = "6–8 QUALITÄTS-KERN"
    elif rs >= 3:  anker = "3–5 GRENZFALL/SPEKULATION"
    else:          anker = "1–2 FINGER WEG"

    flags_str = ", ".join(f["name"] for f in flags) if flags else "Keine"

    if rating == "KAUFEN":      r_color, r_bg = "#3fb950", "#1a3a1a"
    elif rating == "BEOBACHTEN":r_color, r_bg = "#d29922", "#3a2f00"
    else:                        r_color, r_bg = "#da3633", "#3a1010"

    bar_c = "#3fb950" if rs >= 7 else "#d29922" if rs >= 4 else "#da3633"
    wf    = wacc_d.get("flag", "🟢")
    dm_ic = dm.get("icon", "🟢")
    dm_st = dm.get("status", "—")
    k_lbl = konv.get("label", "⚪ KEINE DATEN")

    st.markdown(f"""
<div style="background:#0d1117;border:1px solid #30363d;border-radius:12px;
            padding:22px 26px;margin:12px 0;font-family:monospace;">
  <div style="color:#8b949e;font-size:0.72em;letter-spacing:1.5px;margin-bottom:6px;">
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br>
    📋 JACK-SUMMARY: {m.get("name","—")} | {m.get("_k_basis_mode","5S")} | {tiefe}<br>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px 20px;font-size:0.88em;color:#c9d1d9;">
    <div><span style="color:#8b949e;">RATING:</span> &nbsp;
      <span style="background:{r_bg};border:1px solid {r_color};border-radius:4px;
        padding:1px 10px;color:{r_color};font-weight:800;">{rating}</span>
    </div>
    <div><span style="color:#8b949e;">SIZING:</span> &nbsp; <b>{sizing}</b></div>
    <div><span style="color:#8b949e;">ABSTAUBER:</span> &nbsp; <b>{ab}</b></div>
    <div><span style="color:#8b949e;">REAPER SCORE:</span> &nbsp;
      <b style="color:{bar_c};">{rs}/10</b> &nbsp;
      <span style="color:#8b949e;font-size:0.85em;">· Anker: {anker}</span>
    </div>
    <div><span style="color:#8b949e;">KONFIDENZ:</span> &nbsp;
      <span style="color:{k_color};font-weight:700;">{k_icon} {k_label}</span>
    </div>
    <div><span style="color:#8b949e;">WACC-FLAG:</span> &nbsp; <b>{wf} {pct(wacc_d.get("wacc"))}</b></div>
    <div><span style="color:#8b949e;">DEBT-MATURITY:</span> &nbsp;
      <span style="color:{dm.get("color","#8b949e")};font-weight:700;">{dm_ic} {dm_st}</span>
    </div>
    <div><span style="color:#8b949e;">KONVERGENZ:</span> &nbsp;
      <span style="color:{konv.get("color","#8b949e")};font-weight:700;">{k_lbl}</span>
    </div>
    <div><span style="color:#8b949e;">EDGE SCORE:</span> &nbsp; <b>{ec.get("edge","—")}</b></div>
    <div><span style="color:#8b949e;">CATALYST SCORE:</span> &nbsp; <b>{ec.get("catalyst","—")}</b></div>
    <div><span style="color:#8b949e;">TIEFE:</span> &nbsp; <b>{tiefe}</b></div>
    <div><span style="color:#8b949e;">K-BASIS:</span> &nbsp; <b>{mode} · {k_met}/{k_basis}</b></div>
    <div style="grid-column:1/-1;">
      <span style="color:#8b949e;">FLAGS AKTIV:</span> &nbsp;
      <span style="color:{"#da3633" if flags else "#3fb950"};">{flags_str}</span>
    </div>
  </div>
  <div style="height:6px;background:#21262d;border-radius:3px;margin:14px 0;">
    <div style="width:{rs*10}%;background:{bar_c};height:6px;border-radius:3px;"></div>
  </div>
  <div style="color:#c9d1d9;font-size:0.88em;line-height:1.7;border-top:1px solid #21262d;padding-top:10px;">
    {verdict}
  </div>
  <div style="color:#8b949e;font-size:0.65em;margin-top:8px;">
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  </div>
</div>""", unsafe_allow_html=True)


# ── JACK scoring ──────────────────────────────────────────────────────────────
def calc_jack(m: dict) -> dict:
    j = {}

    # --- K-BASIS auto-detect (Sonderregeln) — Prioritäten-Logik ---
    k_basis, mode, mode_reason = _auto_detect_k_basis(m)
    m["_k_basis_mode"]   = mode
    m["_k_basis_reason"] = mode_reason

    # --- Real FCF-Marge (nach SBC) — JACK-Spec: FCF-Marge must be "real" --------
    # Reported FCF-Marge ignores stock-based compensation; real FCF = FCF − SBC
    _fcf_raw    = m.get("fcf") or 0
    _sbc_deduct = m.get("sbc_abs") or 0
    _rev_base   = m.get("revenue") or 1
    _real_fcf_m = (_fcf_raw - _sbc_deduct) / _rev_base if _rev_base > 0 \
                  else (m.get("fcf_margin") or 0)
    m["real_fcf_margin"] = _real_fcf_m        # stored for DNA-CHECK display
    # Real FCF available flag (both fcf and revenue must be present)
    _real_fcf_avail = m.get("fcf") is not None and m.get("revenue") is not None

    # --- K-Kriterien (Gatekeeper) — mode-spezifisch ---
    K = {}
    def k(name, passed, val, avail=True):
        K[name] = {"pass": passed, "val": val, "avail": avail}

    p  = m.get("piotroski", {})
    ps = p.get("score")
    _ps_str = f"{ps if ps is not None else 'N/V'}/{p.get('max', 8)}"
    _sbc_ok  = (m.get("sbc_intensity") or 0) < 0.10
    _sbc_val = pct(m.get("sbc_intensity"))
    _sbc_av  = m.get("sbc_intensity") is not None

    if mode == "5F Finanz":
        # ── Finanzsektor: ROE-basiert, keine klassischen Kapitalrenditen ──────
        k("ROE > 12%",        (m.get("roe") or 0) > 0.12,           pct(m.get("roe")),           m.get("roe") is not None)
        k("FCF-Marge ≥ 15%",  _real_fcf_m >= 0.15,                  pct(_real_fcf_m) + " (real)", _real_fcf_avail)
        k("Op. Leverage",     m.get("op_leverage", False),           "Ja" if m.get("op_leverage") else "Nein", True)
        k("Piotroski ≥ 7",    (ps or 0) >= 7,                       _ps_str,                     ps is not None)
        k("EPS-CAGR ≥ 10%",   (m.get("eps_cagr") or 0) >= 0.10,     pct(m.get("eps_cagr")),      m.get("eps_cagr") is not None)
        k("SBC < 10%",        _sbc_ok,                               _sbc_val,                    _sbc_av)

    elif mode == "5SaaS":
        # ── SaaS / High-Margin Tech: Bruttomarge + ARR-Wachstum dominant ─────
        k("ROIC > 15%",       (m.get("roic") or 0) > 0.15,          pct(m.get("roic")),          m.get("roic") is not None)
        k("FCF-Marge ≥ 20%",  _real_fcf_m >= 0.20,                  pct(_real_fcf_m) + " (real)", _real_fcf_avail)
        k("Bruttomarge ≥65%", (m.get("gross_margin") or 0) >= 0.65, pct(m.get("gross_margin")),  m.get("gross_margin") is not None)
        k("Rev-CAGR ≥ 15%",   (m.get("rev_cagr") or 0) >= 0.15,    pct(m.get("rev_cagr")),      m.get("rev_cagr") is not None)
        k("EPS-CAGR ≥ 15%",   (m.get("eps_cagr") or 0) >= 0.15,    pct(m.get("eps_cagr")),      m.get("eps_cagr") is not None)
        k("SBC < 15%",        (m.get("sbc_intensity") or 0) < 0.15,  pct(m.get("sbc_intensity")), m.get("sbc_intensity") is not None)

    elif mode == "5I Infrastruktur":
        # ── Infrastruktur: EBITDA-Marge + Schuldentragfähigkeit + SBC dominant
        # k_basis=5, 6 Kriterien → darf 1 verfehlen (SBC meist sehr niedrig)
        _real_fcf_pos = (_fcf_raw - _sbc_deduct) > 0
        k("Op. Marge ≥ 40%",  (m.get("op_margin") or 0) >= 0.40,    pct(m.get("op_margin")),     m.get("op_margin") is not None)
        k("ND/EBITDA < 6x",   (m.get("nd_ebitda") or 99) < 6.0,     xfmt(m.get("nd_ebitda")),    m.get("nd_ebitda") is not None)
        k("FCF > 0",          _real_fcf_pos,                         cap_fmt(_fcf_raw - _sbc_deduct) + " (real)", _real_fcf_avail)
        k("Capex ≤ 30%",      (m.get("capex_ratio") or 99) <= 0.30, pct(m.get("capex_ratio")),   m.get("capex_ratio") is not None)
        k("Piotroski ≥ 5",    (ps or 0) >= 5,                       _ps_str,                     ps is not None)
        k("SBC < 10%",        _sbc_ok,                               _sbc_val,                    _sbc_av)

    elif mode == "5V Versorger":
        # ── Versorger: Dividenden-Stabilität + Regulierungsqualität + SBC ─────
        # k_basis=5, 6 Kriterien → darf 1 verfehlen
        k("ROE ≥ 10%",        (m.get("roe") or 0) >= 0.10,          pct(m.get("roe")),           m.get("roe") is not None)
        k("Div.-Rendite ≥4%", (m.get("dividend") or 0) >= 0.04,     pct(m.get("dividend")),      m.get("dividend") is not None)
        k("Payout ≤ 80%",     0 < (m.get("payout_ratio") or 0) <= 0.80, pct(m.get("payout_ratio")), m.get("payout_ratio") is not None)
        k("Op. Marge ≥ 30%",  (m.get("op_margin") or 0) >= 0.30,   pct(m.get("op_margin")),     m.get("op_margin") is not None)
        k("ND/EBITDA < 5x",   (m.get("nd_ebitda") or 99) < 5.0,    xfmt(m.get("nd_ebitda")),    m.get("nd_ebitda") is not None)
        k("SBC < 10%",        _sbc_ok,                               _sbc_val,                    _sbc_av)

    elif mode == "5K Sachwerte":
        # ── Kapitalintensive Sachwerte: FCF-Yield + EV-Bewertung + SBC ────────
        # k_basis=5, 6 Kriterien → darf 1 verfehlen
        k("FCF-Marge ≥ 5%",   _real_fcf_m >= 0.05,                  pct(_real_fcf_m) + " (real)", _real_fcf_avail)
        k("EV/EBITDA ≤ 8x",   0 < (m.get("ev_ebitda") or 99) <= 8.0, xfmt(m.get("ev_ebitda")),  m.get("ev_ebitda") is not None)
        k("ND/EBITDA < 3x",   (m.get("nd_ebitda") or 99) < 3.0,    xfmt(m.get("nd_ebitda")),    m.get("nd_ebitda") is not None)
        k("ROA > 5%",         (m.get("roa") or 0) > 0.05,          pct(m.get("roa")),           m.get("roa") is not None)
        k("Piotroski ≥ 5",    (ps or 0) >= 5,                      _ps_str,                     ps is not None)
        k("SBC < 10%",        _sbc_ok,                               _sbc_val,                    _sbc_av)

    elif mode == "4P Piotroski":
        # ── Piotroski-Override: Deep Value — Piotroski ist primäres Gate ──────
        # k_basis=4, 5 Kriterien → darf 1 verfehlen (SBC als zusätzlicher Check)
        _real_fcf_pos = (_fcf_raw - _sbc_deduct) > 0
        k("Piotroski ≥ 7",    (ps or 0) >= 7,                       _ps_str,                     ps is not None)
        k("ROIC ≥ 10%",       (m.get("roic") or 0) >= 0.10,         pct(m.get("roic")),          m.get("roic") is not None)
        k("FCF > 0",          _real_fcf_pos,                         cap_fmt(_fcf_raw - _sbc_deduct) + " (real)", _real_fcf_avail)
        k("ND/EBITDA < 4x",   (m.get("nd_ebitda") or 99) < 4.0,    xfmt(m.get("nd_ebitda")),    m.get("nd_ebitda") is not None)
        k("SBC < 10%",        _sbc_ok,                               _sbc_val,                    _sbc_av)

    else:
        # ── 5S Standard (Default) ────────────────────────────────────────────
        k("ROIC > 20%",       (m.get("roic") or 0) > 0.20,          pct(m.get("roic")),          m.get("roic") is not None)
        k("FCF-Marge ≥ 20%",  _real_fcf_m >= 0.20,                  pct(_real_fcf_m) + " (real)", _real_fcf_avail)
        k("Op. Leverage",     m.get("op_leverage", False),           "Ja" if m.get("op_leverage") else "Nein", True)
        k("Piotroski ≥ 7",    (ps or 0) >= 7,                       _ps_str,                     ps is not None)
        k("EPS-CAGR ≥ 12%",   (m.get("eps_cagr") or 0) >= 0.12,    pct(m.get("eps_cagr")),      m.get("eps_cagr") is not None)
        k("SBC < 10%",        _sbc_ok,                               _sbc_val,                    _sbc_av)

    # --- E-Kriterien — teils mode-spezifisch ---
    E = {}
    def e(name, passed, val):
        E[name] = {"pass": passed, "val": val}

    if mode == "5F Finanz":
        e("Bruttomarge ≥ 30%",  (m.get("gross_margin") or 0) >= 0.30, pct(m.get("gross_margin")))
        e("ROE ≥ 15%",           (m.get("roe") or 0) >= 0.15,         pct(m.get("roe")))
        e("Rev-CAGR ≥ 6%",       (m.get("rev_cagr") or 0) >= 0.06,    pct(m.get("rev_cagr")))
        e("ND/EBITDA < 4x",      (m.get("nd_ebitda") or 99) < 4.0,   xfmt(m.get("nd_ebitda")))
        e("Op. Marge ≥ 20%",     (m.get("op_margin") or 0) >= 0.20,  pct(m.get("op_margin")))
        e("Piotroski ≥ 5",       (ps or 0) >= 5,                     _ps_str)
    elif mode == "5SaaS":
        e("Bruttomarge ≥ 70%",  (m.get("gross_margin") or 0) >= 0.70, pct(m.get("gross_margin")))
        e("Op. Marge ≥ 15%",     (m.get("op_margin") or 0) >= 0.15,  pct(m.get("op_margin")))
        e("Rev-CAGR ≥ 20%",      (m.get("rev_cagr") or 0) >= 0.20,   pct(m.get("rev_cagr")))
        e("ND/EBITDA < 2x",      (m.get("nd_ebitda") or 99) < 2.0,   xfmt(m.get("nd_ebitda")))
        e("SBC < 10%",           (m.get("sbc_intensity") or 0) < 0.10, pct(m.get("sbc_intensity")))
        e("CCC < 0d",            (m.get("ccc") or 999) < 0,          dfmt(m.get("ccc")))
    elif mode in ("5I Infrastruktur", "5V Versorger"):
        e("Bruttomarge ≥ 40%",  (m.get("gross_margin") or 0) >= 0.40, pct(m.get("gross_margin")))
        e("EBITDA > 0",          (m.get("fcf") or 0) > 0,             cap_fmt(m.get("fcf")))
        e("Rev-CAGR ≥ 3%",       (m.get("rev_cagr") or 0) >= 0.03,   pct(m.get("rev_cagr")))
        e("Piotroski ≥ 5",       (ps or 0) >= 5,                     _ps_str)
        e("ROA > 3%",            (m.get("roa") or 0) > 0.03,         pct(m.get("roa")))
        e("Capex ≤ 35%",         (m.get("capex_ratio") or 99) <= 0.35, pct(m.get("capex_ratio")))
    elif mode == "5K Sachwerte":
        e("Op. Marge ≥ 15%",     (m.get("op_margin") or 0) >= 0.15,  pct(m.get("op_margin")))
        e("Rev-CAGR ≥ 0%",       (m.get("rev_cagr") or -99) >= 0,    pct(m.get("rev_cagr")))
        e("Piotroski ≥ 5",       (ps or 0) >= 5,                     _ps_str)
        e("P/B < 2x",            0 < (m.get("price_to_book") or 99) < 2, f"{(m.get('price_to_book') or 0):.1f}x")
        e("Div.-Rendite ≥ 2%",   (m.get("dividend") or 0) >= 0.02,   pct(m.get("dividend")))
        e("Op. Leverage",        m.get("op_leverage", False),         "Ja" if m.get("op_leverage") else "Nein")
    elif mode == "4P Piotroski":
        e("P/B < 1.5x",          0 < (m.get("price_to_book") or 99) < 1.5, f"{(m.get('price_to_book') or 0):.1f}x")
        e("ROA > 3%",            (m.get("roa") or 0) > 0.03,         pct(m.get("roa")))
        e("Rev-CAGR ≥ 0%",       (m.get("rev_cagr") or -99) >= 0,    pct(m.get("rev_cagr")))
        e("Op. Marge ≥ 10%",     (m.get("op_margin") or 0) >= 0.10,  pct(m.get("op_margin")))
        e("Bruttomarge ≥ 30%",  (m.get("gross_margin") or 0) >= 0.30, pct(m.get("gross_margin")))
        e("SBC < 10%",           (m.get("sbc_intensity") or 0) < 0.10, pct(m.get("sbc_intensity")))
    else:
        # 5S Standard E-Kriterien
        e("Bruttomarge ≥ 60%",  (m.get("gross_margin") or 0) >= 0.60,  pct(m.get("gross_margin")))
        e("Op. Marge ≥ 20%",    (m.get("op_margin")    or 0) >= 0.20,  pct(m.get("op_margin")))
        e("Rev-CAGR ≥ 8%",      (m.get("rev_cagr")     or 0) >= 0.08,  pct(m.get("rev_cagr")))
        e("Net Debt/EBITDA<2x", (m.get("nd_ebitda") or 99) < 2.0,      xfmt(m.get("nd_ebitda")))
        e("Capex/Umsatz ≤ 5%",  (m.get("capex_ratio")  or 99) <= 0.05, pct(m.get("capex_ratio")))
        e("CCC < 30d",          (m.get("ccc") or 999) < 30,            dfmt(m.get("ccc")))

    j["K"] = K; j["E"] = E

    k_met   = sum(1 for v in K.values() if v["pass"])
    k_avail = sum(1 for v in K.values() if v["avail"])
    e_met   = sum(1 for v in E.values() if v["pass"])
    j.update({"k_met": k_met, "k_avail": k_avail, "e_met": e_met, "k_basis": k_basis})

    # --- DATEN-KONFIDENZ (Schritt 2B) ---
    j["daten_konfidenz"] = _calc_daten_konfidenz(m)

    # --- FLAGS (Klasse A) ---
    flags = _detect_flags(m)
    j["flags"] = flags

    # --- KONFIDENZ-DECKEL ---
    j["konfidenz"] = _calc_konfidenz_deckel(k_avail, k_basis, flags)

    # --- REAPER SCORE mit Anker ---
    rs = _calc_reaper_score(k_met, k_basis, e_met, len(E), m, flags)
    j["reaper_score"] = rs

    # --- Rating (Drei-Klassen) ---
    red_flags = [f for f in flags if f["color"] == "#da3633"]
    if k_met >= k_basis and rs >= 7 and not red_flags:
        j["rating"] = "KAUFEN"
    elif k_met >= k_basis - 2 and rs >= 4 and len(red_flags) == 0:
        j["rating"] = "BEOBACHTEN"
    else:
        j["rating"] = "SCHROTT"

    # --- Sizing ---
    if j["rating"] == "KAUFEN" and rs >= 9:    j["sizing"] = "Tier 1 (5–8%)"
    elif j["rating"] == "KAUFEN":               j["sizing"] = "Tier 2 (3–5%)"
    elif j["rating"] == "BEOBACHTEN":           j["sizing"] = "Tier 3 (1–2%)"
    else:                                        j["sizing"] = "Tier 4 (0%)"

    # --- Legacy flags for render ---
    nd = m.get("nd_ebitda")
    j["debt_flag"] = "🟢 NIEDRIG" if (nd is None or nd < 1.0) else ("🟡 ERHÖHT" if nd < 2.5 else "🔴 KRITISCH")
    j["wacc_flag"] = "🟢" if (nd is None or nd < 1.0) else ("🟡" if nd < 2.0 else "🔴")

    # --- Verdict text (Persona & Mandat) ---
    j["verdict"] = _jack_verdict(j["rating"], rs, k_met, k_basis, flags, m)

    # --- Abstauber-Preis (Margin of Safety) ---
    price = m.get("price")
    if price:
        disc = 0.15 if j["rating"] == "KAUFEN" else 0.25
        sym  = "€" if m.get("currency") == "EUR" else "$"
        j["abstauber"] = f"{sym}{price * (1 - disc):.2f}"

    # --- TRANSFORMATION-PROTOKOLL ---
    j["transformation"] = _calc_transformation_flag(m)
    if j["transformation"]["active"] and mode == "5S Standard":
        m["_k_basis_mode"] = "5T (Transformation)"

    # --- MOAT-VERIFIKATION ---
    j["moat"] = _calc_moat_score(m)

    # --- MANAGEMENT-SCORE ---
    j["management"] = _calc_management_score(m)

    # --- CAPEX-CHECK ---
    j["capex_check"] = _calc_capex_check(m)

    # --- DEBT MATURITY CHECK ---
    j["debt_maturity"] = _calc_debt_maturity(m)

    # --- EXIT-STRATEGIE ---
    j["exit_strategy"] = _calc_exit_strategy(m, j)

    # --- EDGE & CATALYST SCORE ---
    j["edge_catalyst"] = _calc_edge_catalyst(m, j)

    # --- ABBRUCH-LOGIK ---
    j["abbruch"] = _calc_abbruch(j, mode="FULL")

    # --- WACC + DCF + REVERSE-DCF + STRESS-TEST ---
    wacc_d = _calc_wacc(m)
    j["wacc_data"]    = wacc_d
    j["dcf"]          = _calc_dcf(m, wacc_d)
    j["reverse_dcf"]  = _calc_reverse_dcf(m, wacc_d)
    j["stress_test"]  = _calc_stress_test(m, wacc_d)
    j["konvergenz"]   = _calc_konvergenz(m, j["dcf"], j["reverse_dcf"])

    # --- SHAREHOLDER YIELD ---
    j["shareholder_yield"] = _calc_shareholder_yield(m)

    # --- ANALYSE-TIEFE ---
    _tiefe_data = _calc_analyse_tiefe(m)
    j["analyse_tiefe"]      = _tiefe_data["tiefe"]   # String für JACK-SUMMARY
    j["analyse_tiefe_data"] = _tiefe_data            # Dict für bedingte Render-Logik

    # --- TECHNICAL ALIGNMENT ---
    j["technical"] = _calc_technical(m)

    # --- DEVIL'S ADVOCATE ---
    j["devils_advocate"] = _calc_devils_advocate(m, j)

    # --- WACC-FLAG update (now dynamic) ---
    wacc_val = wacc_d.get("wacc", 0)
    j["wacc_flag"] = wacc_d.get("flag", "🟢")

    return j

# ── UI Helpers ────────────────────────────────────────────────────────────────
def tile(label, value, color="#e6edf3"):
    st.markdown(
        f'<div class="mtile"><div class="mlabel">{label}</div>'
        f'<div class="mvalue" style="color:{color};">{value}</div></div>',
        unsafe_allow_html=True,
    )

def score_bar(score: int):
    c = "#238636" if score >= 7 else "#d29922" if score >= 4 else "#da3633"
    st.markdown(f"""
<div class="score-wrap">
  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
    <span style="font-size:0.75em;color:#8b949e;text-transform:uppercase;letter-spacing:.8px;">Reaper Score</span>
    <span style="font-weight:700;color:{c};">{score}/10</span>
  </div>
  <div class="score-bg"><div class="score-fill" style="width:{score*10}%;background:{c};"></div></div>
</div>""", unsafe_allow_html=True)

def kcolor(passed, typ="K"):
    if typ == "K":
        return "#3fb950" if passed else "#da3633"
    return "#388bfd" if passed else "#8b949e"

def _html_table(df: pd.DataFrame, col_colors: dict = None) -> str:
    """Render a pandas DataFrame as a styled HTML table with dark theme."""
    col_colors = col_colors or {}
    th_style = "background:#21262d;color:#8b949e;padding:7px 12px;text-align:left;font-size:12px;font-weight:600;border-bottom:1px solid #30363d;"
    td_base  = "background:#161b22;color:#e6edf3;padding:6px 12px;font-size:12px;border-bottom:1px solid #21262d;"
    rows_html = ""
    for i, row in df.iterrows():
        cells = ""
        for col in df.columns:
            val = row[col]
            color_style = f"color:{col_colors[col]};" if col in col_colors else ""
            # detect per-cell color overrides stored as tuples (text, color)
            if isinstance(val, tuple) and len(val) == 2:
                val, cell_color = val
                color_style = f"color:{cell_color};"
            cells += f'<td style="{td_base}{color_style}">{val}</td>'
        rows_html += f"<tr>{cells}</tr>"
    headers = "".join(f'<th style="{th_style}">{c}</th>' for c in df.columns)
    return (f'<div style="overflow-x:auto;border-radius:8px;border:1px solid #30363d;margin-bottom:12px;">'
            f'<table style="width:100%;border-collapse:collapse;">'
            f'<thead><tr>{headers}</tr></thead>'
            f'<tbody>{rows_html}</tbody></table></div>')

def _sector_benchmarks(sector: str) -> dict:
    """Grobe Peer-Benchmarks nach Sektor für Bewertungs-Multiples."""
    tech    = {"kuv": (4, 10),  "kgv": (25, 45), "ev_ebitda": (18, 30), "p_fcf": (25, 40)}
    saas    = {"kuv": (6, 15),  "kgv": (40, 80), "ev_ebitda": (25, 45), "p_fcf": (30, 55)}
    value   = {"kuv": (1, 3),   "kgv": (12, 22), "ev_ebitda": (8,  15), "p_fcf": (12, 20)}
    health  = {"kuv": (3, 8),   "kgv": (20, 35), "ev_ebitda": (15, 25), "p_fcf": (20, 35)}
    finance = {"kuv": (2, 5),   "kgv": (10, 18), "ev_ebitda": (10, 18), "p_fcf": (12, 22)}
    mapping = {
        "Technology": tech, "Communication Services": saas,
        "Consumer Cyclical": value, "Consumer Defensive": value,
        "Industrials": value, "Basic Materials": value,
        "Healthcare": health, "Financial Services": finance,
        "Energy": value, "Utilities": value, "Real Estate": value,
    }
    return mapping.get(sector, tech)

def _valuation_label(val, low, high):
    if val is None:     return "—",       "#8b949e"
    if val < 0:         return "neg.",     "#8b949e"
    if val < low:       return "✅ günstig", "#3fb950"
    if val <= high:     return "⚖️ fair",   "#d29922"
    return              "❌ teuer",        "#da3633"

def _render_kapitaleffizienz(m: dict, j: dict):
    st.markdown("### 2️⃣ Kapitaleffizienz & Bilanzstärke")
    p        = m.get("piotroski", {})
    ps       = p.get("score")
    ps_max   = p.get("max", 8)
    nc       = m.get("net_cash")
    sbc_lbl, sbc_col = m.get("sbc_flag", ("N/V", "#8b949e"))
    eq_ratio = m.get("equity_ratio")

    k1, k2, k3 = st.columns(3)
    with k1:
        roe = m.get("roe")
        c   = "#3fb950" if (roe or 0) > 0.15 else "#d29922" if (roe or 0) > 0 else "#da3633"
        tile("ROE", pct(roe), c)
    with k2:
        roic = m.get("roic")
        c    = "#3fb950" if (roic or 0) > 0.20 else "#d29922" if (roic or 0) > 0.10 else "#da3633"
        tile("ROIC", pct(roic), c)
    with k3:
        ps_comment = "Stark" if (ps or 0) >= 7 else "Solide" if (ps or 0) >= 5 else "Schwach"
        ps_col     = "#3fb950" if (ps or 0) >= 7 else "#d29922" if (ps or 0) >= 5 else "#da3633"
        tile(f"Piotroski ({ps_comment})", f"{ps if ps is not None else 'N/V'}/{ps_max}", ps_col)

    k4, k5, k6 = st.columns(3)
    with k4:
        if nc is not None:
            nc_col = "#3fb950" if nc > 0 else "#da3633"
            nc_str = f"+{cap_fmt(nc)}" if nc > 0 else f"-{cap_fmt(abs(nc))}"
            nc_lbl = "Netto-Cash 💰" if nc > 0 else "Netto-Schuld"
        else:
            nc_col, nc_str, nc_lbl = "#8b949e", "N/V", "Net Cash"
        tile(nc_lbl, nc_str, nc_col)
    with k5:
        eq_c = "#3fb950" if (eq_ratio or 0) > 0.3 else "#d29922" if (eq_ratio or 0) > 0 else "#da3633"
        tile("EK-Quote", pct(eq_ratio), eq_c)
    with k6:
        tile("SBC-Belastung", sbc_lbl, sbc_col)
    st.markdown("")

def _render_valuation_multiples(m: dict):
    st.markdown("### 📐 Bewertungs-Multiples")
    sector = m.get("sector", "")
    bm     = _sector_benchmarks(sector)

    kuv      = m.get("price_to_sales")
    kgv      = m.get("pe")
    ev_ebitda= m.get("ev_ebitda")
    p_fcf    = m.get("p_fcf")

    rows = []
    for name, val, (low, high), period in [
        ("KUV",        kuv,       bm["kuv"],       "TTM"),
        ("KGV (GAAP)", kgv,       bm["kgv"],       "trailing"),
        ("EV/EBITDA",  ev_ebitda, bm["ev_ebitda"], "TTM"),
        ("P/FCF",      p_fcf,     bm["p_fcf"],     "TTM"),
    ]:
        lbl, col = _valuation_label(val, low, high)
        rows.append({
            "Multiple":       f"{name} ({period})",
            "Aktuell":        f"{val:.1f}x" if val and val > 0 else "N/V",
            "Peer-Benchmark": f"{low}–{high}x ({sector or 'Sektor'})",
            "Einschätzung":   (lbl, col),   # tuple → colored cell
        })
    st.markdown(_html_table(pd.DataFrame(rows)), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 🧬 DNA-CHECK — Vollständige Implementierung per JACK-Spezifikation
# ══════════════════════════════════════════════════════════════════════════════
_DNA_TAG_SOURCES = {
    # ── K-Kriterien — Stufe 1 (SEC/Annual Statements via yfinance) ──────────
    "ROIC > 20%":        ("S1",  "Annual IS/BS"),
    "FCF-Marge ≥ 20%":   ("S1",  "Annual CF · nach SBC"),
    "FCF-Marge ≥ 15%":   ("S1",  "Annual CF · nach SBC"),
    "FCF-Marge ≥ 5%":    ("S1",  "Annual CF · nach SBC"),
    "FCF > 0":           ("S1",  "Annual CF · nach SBC"),
    "Op. Leverage":      ("S4",  "Derived from IS"),
    "Piotroski ≥ 7":     ("S1",  "Annual IS/BS/CF"),
    "Piotroski ≥ 5":     ("S1",  "Annual IS/BS/CF"),
    "EPS-CAGR ≥ 12%":    ("S4",  "Multi-year calc"),
    "EPS-CAGR ≥ 10%":    ("S4",  "Multi-year calc"),
    "EPS-CAGR ≥ 15%":    ("S4",  "Multi-year calc"),
    "SBC < 10%":         ("S1",  "Annual CF"),
    "SBC < 15%":         ("S1",  "Annual CF"),
    "ROE > 12%":         ("S1",  "Annual IS/BS"),
    "ROE ≥ 10%":         ("S1",  "Annual IS/BS"),
    "ROIC > 15%":        ("S1",  "Annual IS/BS"),
    "ROIC ≥ 10%":        ("S1",  "Annual IS/BS"),
    "Bruttomarge ≥65%":  ("S1",  "Annual IS"),
    "Rev-CAGR ≥ 15%":    ("S4",  "Multi-year calc"),
    "Op. Marge ≥ 40%":   ("S1",  "Annual IS"),
    "Op. Marge ≥ 30%":   ("S1",  "Annual IS"),
    "ND/EBITDA < 6x":    ("S1",  "Annual BS"),
    "ND/EBITDA < 5x":    ("S1",  "Annual BS"),
    "ND/EBITDA < 4x":    ("S1",  "Annual BS"),
    "ND/EBITDA < 3x":    ("S1",  "Annual BS"),
    "Capex ≤ 30%":       ("S1",  "Annual CF"),
    "Div.-Rendite ≥4%":  ("LIVE","yfinance info"),
    "Payout ≤ 80%":      ("S4",  "yfinance info"),
    "EV/EBITDA ≤ 8x":    ("S4",  "Calc: EV/EBITDA"),
    "ROA > 5%":          ("S1",  "Annual IS/BS"),
    # ── E-Kriterien ─────────────────────────────────────────────────────────
    "Bruttomarge ≥ 60%": ("S1",  "Annual IS"),
    "Bruttomarge ≥ 40%": ("S1",  "Annual IS"),
    "Bruttomarge ≥ 30%": ("S1",  "Annual IS"),
    "Bruttomarge ≥ 70%": ("S1",  "Annual IS"),
    "Op. Marge ≥ 20%":   ("S1",  "Annual IS"),
    "Op. Marge ≥ 15%":   ("S1",  "Annual IS"),
    "Op. Marge ≥ 10%":   ("S1",  "Annual IS"),
    "Rev-CAGR ≥ 8%":     ("S4",  "Multi-year calc"),
    "Rev-CAGR ≥ 6%":     ("S4",  "Multi-year calc"),
    "Rev-CAGR ≥ 3%":     ("S4",  "Multi-year calc"),
    "Rev-CAGR ≥ 20%":    ("S4",  "Multi-year calc"),
    "Rev-CAGR ≥ 0%":     ("S4",  "Multi-year calc"),
    "Net Debt/EBITDA<2x":("S1",  "Annual BS"),
    "ND/EBITDA < 2x":    ("S1",  "Annual BS"),
    "Capex/Umsatz ≤ 5%": ("S1",  "Annual CF"),
    "Capex ≤ 35%":       ("S1",  "Annual CF"),
    "CCC < 30d":         ("S4",  "Derived from BS"),
    "CCC < 0d":          ("S4",  "Derived from BS"),
    "ROE ≥ 15%":         ("S1",  "Annual IS/BS"),
    "ROA > 3%":          ("S1",  "Annual IS/BS"),
    "P/B < 2x":          ("LIVE","yfinance info"),
    "P/B < 1.5x":        ("LIVE","yfinance info"),
    "Div.-Rendite ≥ 2%": ("LIVE","yfinance info"),
    "EBITDA > 0":        ("S1",  "Annual IS+CF"),
    "ROIC > 20%":        ("S1",  "Annual IS/BS"),
}

# Warn-Zonen per K/E-Kriterium (innerhalb XX% des Schwellenwerts)
_DNA_WARN_ZONE = {
    "ROIC > 20%":        lambda v: 0.15 <= (v or 0) <= 0.20,
    "FCF-Marge ≥ 20%":   lambda v: 0.12 <= (v or 0) < 0.20,
    "FCF-Marge ≥ 15%":   lambda v: 0.10 <= (v or 0) < 0.15,
    "Piotroski ≥ 7":     lambda v: 5 <= (v or 0) <= 6,
    "Piotroski ≥ 5":     lambda v: 3 <= (v or 0) <= 4,
    "EPS-CAGR ≥ 12%":    lambda v: 0.08 <= (v or 0) < 0.12,
    "EPS-CAGR ≥ 10%":    lambda v: 0.06 <= (v or 0) < 0.10,
    "EPS-CAGR ≥ 15%":    lambda v: 0.10 <= (v or 0) < 0.15,
    "SBC < 10%":         lambda v: 0.10 <= (v or 0) <= 0.15,
    "SBC < 15%":         lambda v: 0.15 <= (v or 0) <= 0.20,
    "Bruttomarge ≥ 60%": lambda v: 0.45 <= (v or 0) < 0.60,
    "Bruttomarge ≥65%":  lambda v: 0.55 <= (v or 0) < 0.65,
    "Op. Marge ≥ 20%":   lambda v: 0.12 <= (v or 0) < 0.20,
    "Op. Marge ≥ 15%":   lambda v: 0.08 <= (v or 0) < 0.15,
    "Rev-CAGR ≥ 8%":     lambda v: 0.04 <= (v or 0) < 0.08,
    "Rev-CAGR ≥ 6%":     lambda v: 0.03 <= (v or 0) < 0.06,
    "Net Debt/EBITDA<2x":lambda v: 2.0 <= (v or 0) <= 3.0,
    "ND/EBITDA < 3x":    lambda v: 3.0 <= (v or 0) <= 4.0,
    "Capex/Umsatz ≤ 5%": lambda v: 0.05 <= (v or 0) <= 0.10,
    "CCC < 30d":         lambda v: 30 <= (v or 999) <= 60,
    "ROE > 12%":         lambda v: 0.08 <= (v or 0) <= 0.12,
    "ROIC > 15%":        lambda v: 0.10 <= (v or 0) <= 0.15,
    "ROIC ≥ 10%":        lambda v: 0.07 <= (v or 0) <= 0.10,
}


def _dna_status(name: str, passed: bool, raw_val=None) -> tuple:
    """Returns (status_str, color) with ⚠️ borderline support."""
    if passed:
        return "✅", "#3fb950"
    # Check warn zone
    warn_fn = _DNA_WARN_ZONE.get(name)
    if warn_fn and raw_val is not None:
        try:
            if warn_fn(raw_val):
                return "⚠️", "#d29922"
        except Exception:
            pass
    return "❌", "#da3633"


def _dna_raw_val(name: str, m: dict):
    """Map K/E name → raw numeric value for borderline check."""
    _map = {
        "ROIC > 20%": m.get("roic"), "ROIC > 15%": m.get("roic"), "ROIC ≥ 10%": m.get("roic"),
        "FCF-Marge ≥ 20%": m.get("fcf_margin"), "FCF-Marge ≥ 15%": m.get("fcf_margin"),
        "FCF-Marge ≥ 5%": m.get("fcf_margin"),
        "Piotroski ≥ 7": (m.get("piotroski") or {}).get("score"),
        "Piotroski ≥ 5": (m.get("piotroski") or {}).get("score"),
        "EPS-CAGR ≥ 12%": m.get("eps_cagr"), "EPS-CAGR ≥ 10%": m.get("eps_cagr"),
        "EPS-CAGR ≥ 15%": m.get("eps_cagr"),
        "SBC < 10%": m.get("sbc_intensity"), "SBC < 15%": m.get("sbc_intensity"),
        "Bruttomarge ≥ 60%": m.get("gross_margin"), "Bruttomarge ≥65%": m.get("gross_margin"),
        "Bruttomarge ≥ 40%": m.get("gross_margin"), "Bruttomarge ≥ 70%": m.get("gross_margin"),
        "Op. Marge ≥ 20%": m.get("op_margin"), "Op. Marge ≥ 15%": m.get("op_margin"),
        "Rev-CAGR ≥ 8%": m.get("rev_cagr"), "Rev-CAGR ≥ 6%": m.get("rev_cagr"),
        "Net Debt/EBITDA<2x": m.get("nd_ebitda"), "ND/EBITDA < 3x": m.get("nd_ebitda"),
        "Capex/Umsatz ≤ 5%": m.get("capex_ratio"),
        "CCC < 30d": m.get("ccc"),
        "ROE > 12%": m.get("roe"), "ROE ≥ 10%": m.get("roe"),
        "ROIC > 15%": m.get("roic"),
    }
    return _map.get(name)


def _render_dna_check(j: dict, m: dict):
    """
    🧬 DNA-CHECK — vollständige JACK-Spezifikation:
    K-BASIS Header · Tabelle mit Quelle/Tag/Status(✅⚠️❌) ·
    SBC + Shareholder Yield · Beneish OPT · DNA-URTEIL · ESTIMATE-COUNT
    """
    mode        = m.get("_k_basis_mode",   "5S Standard")
    mode_reason = m.get("_k_basis_reason", "Standard-Modus")
    k_basis     = j.get("k_basis", 5)
    k_met       = j.get("k_met",   0)
    e_met       = j.get("e_met",   0)
    K           = j.get("K", {})
    E           = j.get("E", {})
    sy          = j.get("shareholder_yield", {})
    sbc_i       = m.get("sbc_intensity") or 0
    mc          = _K_MODE_COLORS.get(mode, "#8b949e")

    # ── K-BASIS Header Block ─────────────────────────────────────────────────
    _mode_desc = {
        "5S Standard":        f"Standard K-BASIS = {k_basis} (ROIC · FCF · Leverage · Piotroski · EPS · SBC)",
        "5F Finanz":          f"Finanz-Override K-BASIS = {k_basis} (ROE ersetzt ROIC · FCF-Marge 15%)",
        "5SaaS":              f"SaaS-Override K-BASIS = {k_basis} (Bruttomarge ≥65% · NRR/ARR-Wachstum)",
        "5I Infrastruktur":   f"Infrastruktur-Override K-BASIS = {k_basis} (EBITDA-Marge · DSCR · Konzessions-Schutz aktiv)",
        "5V Versorger":       f"Versorger-Override K-BASIS = {k_basis} (ROE · Dividende · Payout · Regulierungsschutz aktiv)",
        "5K Sachwerte":       f"Sachwerte-Override K-BASIS = {k_basis} (FCF-Yield · EV/EBITDA · Rohstoff-Zyklus)",
        "4P Piotroski":       f"Piotroski-Override K-BASIS = {k_basis} (Piotroski primäres Gate · ROIC ≥10% · FCF>0)",
        "5T (Transformation)":f"Transformation-Flag K-BASIS = {k_basis} (FCF-Marge temporär E · EPS-CAGR normalisiert)",
    }
    desc_text = _mode_desc.get(mode, f"K-BASIS = {k_basis}")

    st.markdown(
        f'<div style="background:{mc}22;border:1px solid {mc};border-radius:6px;'
        f'padding:8px 14px;margin:6px 0 10px;">'
        f'<span style="color:#8b949e;font-size:0.72em;letter-spacing:1px;">AKTIVE K-BASIS</span><br>'
        f'<span style="color:{mc};font-weight:700;font-size:0.88em;">→ {desc_text}</span><br>'
        f'<span style="color:#8b949e;font-size:0.75em;">{mode_reason}</span>'
        f'</div>',
        unsafe_allow_html=True)

    # ── Build rows ───────────────────────────────────────────────────────────
    rows_html = ""
    estimate_count = 0

    def _row(typ, name, threshold, ist, tag, source, status_str, status_color,
             note="", typ_color="#388bfd"):
        nonlocal estimate_count
        if tag == "ESTIMATE":
            estimate_count += 1
        tag_c  = TAG_COLOR.get(tag, "#8b949e")
        return (
            f'<tr>'
            f'<td style="padding:5px 8px;text-align:center;">'
            f'<span style="background:{typ_color}22;color:{typ_color};border:1px solid {typ_color};'
            f'border-radius:3px;padding:1px 5px;font-size:0.7em;font-weight:700;">{typ}</span></td>'
            f'<td style="color:#c9d1d9;padding:5px 8px;font-size:0.82em;">{name}'
            + (f'<br><span style="color:#6e7681;font-size:0.72em;">{note}</span>' if note else "")
            + f'</td>'
            f'<td style="color:#8b949e;padding:5px 8px;font-size:0.8em;">{threshold}</td>'
            f'<td style="color:#e6edf3;padding:5px 8px;font-size:0.82em;font-weight:500;">{ist}</td>'
            f'<td style="padding:5px 8px;">'
            f'<span style="background:{tag_c}22;border:1px solid {tag_c};color:{tag_c};'
            f'border-radius:3px;padding:1px 5px;font-size:0.68em;font-weight:700;">{tag}</span>'
            f'<span style="color:#6e7681;font-size:0.68em;margin-left:4px;">{source}</span></td>'
            f'<td style="text-align:center;padding:5px 8px;">'
            f'<span style="color:{status_color};font-size:1em;">{status_str}</span></td>'
            f'</tr>'
        )

    # K rows
    for name, v in K.items():
        raw    = _dna_raw_val(name, m)
        st_str, st_col = _dna_status(name, v["pass"], raw)
        if not v.get("avail", True):
            st_str, st_col = "N/V", "#8b949e"
        tag, src = _DNA_TAG_SOURCES.get(name, ("ESTIMATE", "Calculated"))
        rows_html += _row("K", name, _k_threshold(name), v["val"],
                          tag, src, st_str, st_col,
                          typ_color="#388bfd")

    # E rows
    for name, v in E.items():
        raw    = _dna_raw_val(name, m)
        st_str, st_col = _dna_status(name, v["pass"], raw)
        tag, src = _DNA_TAG_SOURCES.get(name, ("ESTIMATE", "Calculated"))
        # GAAP-GAP-FLAG for Op. Margin
        note_e = ""
        if "Op. Marg" in name and m.get("op_margin") is not None:
            note_e = "[GAAP] — Non-GAAP-Delta: prüfen"
        rows_html += _row("E", name, _e_threshold(name), v["val"],
                          tag, src, st_str, st_col, note=note_e,
                          typ_color="#d29922")

    # Shareholder Yield (E-OPT, always show)
    sy_total = sy.get("total", 0)
    sy_pass  = sy_total > 0
    sy_str, sy_col = ("✅", "#3fb950") if sy_pass else ("❌", "#da3633")
    rows_html += _row("E",  "Shareholder Yield",
                      "Positiv (Div+Buyback−SBC)",
                      f"{pct(sy_total)} ({sy.get('label','—').split(' ',1)[-1] if sy.get('label') else '—'})",
                      "ESTIMATE", "Derived",
                      sy_str, sy_col,
                      note=f"Div {pct(sy.get('div',0))} + Buyback {pct(sy.get('buyback',0))} − SBC {pct(sy.get('sbc',0))}",
                      typ_color="#d29922")

    # Beneish M-Score (OPT)
    rows_html += _row("OPT", "Beneish M-Score",
                      "< −1.78",
                      "SKIP",
                      "SKIP", "Benötigt alle 8 SEC-Live-Pulls",
                      "⏭️ SKIP", "#8b949e",
                      note="Nur wenn alle 8 Komponenten [LIVE] — sonst SKIP per Klasse B Regel",
                      typ_color="#8b949e")

    # ── Full Table ───────────────────────────────────────────────────────────
    th = lambda t: (f'<th style="background:#21262d;color:#8b949e;padding:6px 8px;'
                    f'text-align:left;font-size:0.72em;font-weight:600;border-bottom:1px solid #30363d;">{t}</th>')
    st.markdown(
        f'<table style="width:100%;border-collapse:collapse;">'
        f'<thead><tr>'
        + th("Typ") + th("Kennzahl") + th("Schwelle") + th("Ist-Wert") + th("Quelle / Tag") + th("Status")
        + f'</tr></thead>'
        f'<tbody style="background:#161b22;">{rows_html}</tbody>'
        f'</table>',
        unsafe_allow_html=True)

    # ── DNA-URTEIL ───────────────────────────────────────────────────────────
    e_total      = len(E) + 1   # +1 für Shareholder Yield
    e_pass_total = e_met + (1 if sy_pass else 0)
    conf_deckel  = estimate_count >= 3
    conf_txt     = "🟡 Ja" if conf_deckel else "🟢 Nein"
    conf_col     = "#d29922" if conf_deckel else "#3fb950"
    k_col        = "#3fb950" if k_met >= k_basis else ("#d29922" if k_met >= k_basis - 2 else "#da3633")

    st.markdown(
        f'<div style="background:#0d1117;border:1px solid #30363d;border-radius:6px;'
        f'padding:8px 14px;margin-top:8px;font-family:monospace;font-size:0.82em;">'
        f'<span style="color:#8b949e;">DNA-URTEIL: </span>'
        f'<span style="color:{k_col};font-weight:700;">K: {k_met}/{k_basis}</span>'
        f'<span style="color:#8b949e;"> · </span>'
        f'<span style="color:#d29922;">E: {e_pass_total}/{e_total}</span>'
        f'<span style="color:#8b949e;"> · </span>'
        f'<span style="color:#8b949e;">Beneish: ⏭️ SKIP</span>'
        f'<br>'
        f'<span style="color:#8b949e;">ESTIMATE-COUNT: </span>'
        f'<span style="color:{conf_col};">{estimate_count} Datenpunkte [ESTIMATE]</span>'
        f'<span style="color:#8b949e;"> → Konfidenz-Deckel 🟡 aktiv? </span>'
        f'<span style="color:{conf_col};font-weight:700;">{conf_txt}</span>'
        f'</div>',
        unsafe_allow_html=True)


def _render_eps_beats(eps_hist: pd.DataFrame):
    if eps_hist is None or eps_hist.empty:
        return
    st.markdown("### 📋 EPS Beat/Miss (letzte Quartale)")
    try:
        df = eps_hist.copy().head(6)
        rename = {
            "epsEstimate": "EPS Estimate", "epsActual": "EPS Actual",
            "epsDifference": "Differenz",  "surprisePercent": "Surprise %",
        }
        df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})
        if "Surprise %" in df.columns:
            df["Beat/Miss"] = df["Surprise %"].apply(
                lambda x: f"✅ +{x:.1f}%" if (x or 0) > 0 else (f"❌ {x:.1f}%" if x is not None else "—")
            )
        # format numeric columns
        for col in ["EPS Estimate", "EPS Actual", "Differenz", "Surprise %"]:
            if col in df.columns:
                df[col] = df[col].apply(lambda v: f"{v:.2f}" if isinstance(v, (int, float)) and pd.notna(v) else "—")
        # reset index for display
        df = df.reset_index(drop=False)
        if "index" in df.columns:
            df = df.rename(columns={"index": "Quartal"})
        st.markdown(_html_table(df), unsafe_allow_html=True)
    except Exception:
        pass
    st.markdown("")

# ── Main Render ────────────────────────────────────────────────────────────────
def render(symbol: str, m: dict, j: dict, hist: pd.DataFrame, eps_hist: pd.DataFrame = None):
    sym_sign = "€" if m.get("currency") == "EUR" else "$"
    price    = m.get("price")
    name     = m.get("name", symbol)

    # Company header
    price_str = f" · {sym_sign}{price:.2f} {m.get('currency','USD')}" if price else ""
    st.markdown(f"### {name} `{symbol}`{price_str}")
    parts = [x for x in [m.get("sector"), m.get("industry")] if x]
    if parts:
        st.caption(" · ".join(parts))

    hi52 = m.get("hi52"); lo52 = m.get("lo52")
    if price and hi52 and lo52:
        from_high = (price - hi52) / hi52
        from_low  = (price - lo52) / lo52
        st.caption(f"52W Hoch: {sym_sign}{hi52:.2f} ({from_high:+.1%})  ·  52W Tief: {sym_sign}{lo52:.2f} ({from_low:+.1%})")

    # ── Unternehmensbeschreibung (ganz oben) ───────────────────────────────────
    desc = m.get("description")
    if desc:
        with st.expander("📖 Unternehmensbeschreibung", expanded=False):
            st.markdown(desc)
        if m.get("website"):
            st.caption(f"🌐 {m['website']}")

    st.markdown("---")

    # ── Row 1: Rating / Score / Top metrics ──────────────────────────────────
    c_r, c_s, c1, c2, c3, c4 = st.columns([1.3, 1.6, 1, 1, 1, 1])

    with c_r:
        rating = j["rating"]
        st.markdown(f'<span class="badge badge-{rating}">{rating}</span>', unsafe_allow_html=True)
        st.caption(j.get("sizing", ""))
        em, lbl, col = j["konfidenz"]
        st.markdown(f'<span style="color:{col};font-weight:700;">{em} {lbl}</span>', unsafe_allow_html=True)
        if ab := j.get("abstauber"):
            st.caption(f"🎯 Abstauber: **{ab}**")

    with c_s:
        score_bar(j["reaper_score"])
        st.caption(f"K-Kriterien: {j['k_met']}/{j['k_basis']}  ·  E-Kriterien: {j['e_met']}/{len(j['E'])}")
        st.caption(f"WACC: {j['wacc_flag']}  ·  Debt: {j['debt_flag']}")

    roic = m.get("roic"); fcf_m = m.get("fcf_margin")
    op_m = m.get("op_margin"); gm = m.get("gross_margin")
    with c1: tile("ROIC",       pct(roic), kcolor((roic or 0) > 0.20))
    with c2: tile("FCF-Marge",  pct(fcf_m), kcolor((fcf_m or 0) >= 0.20))
    with c3: tile("Op. Marge",  pct(op_m),  "#3fb950" if (op_m or 0) >= 0.20 else "#d29922")
    with c4: tile("Bruttomt.",  pct(gm),    "#3fb950" if (gm   or 0) >= 0.60 else "#d29922")

    # ── Row 2: Snapshot-Metriken (Screenshot 5-Stil) ─────────────────────────
    p        = m.get("piotroski", {})
    net_cash = m.get("net_cash")
    ebitda0  = m.get("ebitda_series", [None])[0]
    nc_color = "#3fb950" if (net_cash or 0) > 0 else "#da3633"
    nc_label = cap_fmt(abs(net_cash)) if net_cash is not None else "N/V"
    nc_str   = f"+{nc_label}" if (net_cash or 0) > 0 else f"-{nc_label}"

    c5, c6, c7, c8, c9, c10 = st.columns(6)
    with c5:  tile("Netto Cash",  nc_str,                   nc_color)
    with c6:  tile("EBITDA",      cap_fmt(ebitda0),          "#e6edf3")
    with c7:  tile("Piotroski",   f"{p.get('score','N/V')}/{p.get('max',8)}", kcolor((p.get("score") or 0) >= 7))
    with c8:  tile("Rev-CAGR",    pct(m.get("rev_cagr")),   "#3fb950" if (m.get("rev_cagr") or 0) >= 0.08 else "#d29922")
    with c9:  tile("EV/FCF",      xfmt(m.get("ev_fcf")),    "#3fb950" if 0 < (m.get("ev_fcf") or 999) < 25 else "#d29922")
    with c10: tile("Beta",        nfmt(m.get("beta"))        if m.get("beta") else "N/V", "#e6edf3")

    st.markdown("---")

    # ── JACK SUMMARY (OUTPUT-PFLICHT) ─────────────────────────────────────────
    _render_jack_summary(j, m)
    _render_globale_regeln(j, m)

    st.markdown("---")

    # ── Quartalstabelle (Screenshot 1-Stil) ──────────────────────────────────
    quarters = m.get("quarters", [])
    if quarters:
        st.markdown("**📅 Quartals-Übersicht (letzte 4 Quartale)**")
        q_df = pd.DataFrame(quarters)
        st.markdown(_html_table(q_df), unsafe_allow_html=True)
        st.markdown("---")

    # ── Revenue + EBITDA-Chart (Screenshot 2-Stil) ────────────────────────────
    revenues     = m.get("revenues", [])
    ebitda_s     = m.get("ebitda_series", [])
    ebitda_marg  = m.get("ebitda_margin_series", [])

    if len(revenues) >= 2:
        n      = min(len(revenues), len(ebitda_s))
        years  = [f"FY-{n-1-i}" for i in range(n)][::-1]
        rev_v  = [revenues[n-1-i]  / 1e6 for i in range(n)][::-1]
        ebi_v  = [(ebitda_s[n-1-i] / 1e6 if ebitda_s[n-1-i] else None) for i in range(n)][::-1]
        mar_v  = [(ebitda_marg[n-1-i] * 100 if ebitda_marg[n-1-i] else None) for i in range(n)][::-1]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=years, y=rev_v, name="Umsatz ($M)",
            marker_color="#388bfd", opacity=0.85,
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=years, y=ebi_v, name="EBITDA ($M)",
            mode="lines+markers", line=dict(color="#3fb950", width=2),
            marker=dict(size=7),
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=years, y=mar_v, name="EBITDA-Marge %",
            mode="lines+markers", line=dict(color="#f0c040", width=2, dash="dot"),
            marker=dict(size=6),
        ), secondary_y=True)

        fig.update_layout(
            title="Umsatz & EBITDA Trajectory",
            paper_bgcolor="#0d1117", plot_bgcolor="#161b22",
            font=dict(color="#c9d1d9"),
            legend=dict(orientation="h", y=-0.2),
            margin=dict(l=0, r=0, t=40, b=0),
            height=320,
        )
        fig.update_yaxes(title_text="$M", secondary_y=False,
                         gridcolor="#21262d", showgrid=True)
        fig.update_yaxes(title_text="EBITDA-Marge %", secondary_y=True,
                         gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, width="stretch")
        st.markdown("---")

    # ── Kapitaleffizienz (Screenshot 2) ──────────────────────────────────────
    _render_kapitaleffizienz(m, j)
    st.markdown("---")

    # ── Bewertungs-Multiples (Screenshot 3) ──────────────────────────────────
    _render_valuation_multiples(m)
    st.markdown("---")

    # ── EPS Beat/Miss (Screenshot 1 – EPS-Teil) ──────────────────────────────
    _render_eps_beats(eps_hist)
    st.markdown("---")

    # ── 🧬 DNA-CHECK (vollständige JACK-Spezifikation) ────────────────────────
    dna_col, chart_col = st.columns([1.2, 1], gap="large")

    with dna_col:
        st.markdown("**🧬 DNA-CHECK**")
        _render_dna_check(j, m)

        # DATA INTEGRITY SYSTEM legend
        legend_html = " &nbsp; ".join(
            f'<span style="background:{c}22;border:1px solid {c};color:{c};'
            f'border-radius:3px;padding:1px 5px;font-size:0.65em;font-weight:700;">[{t}]</span>'
            for t, c in TAG_COLOR.items()
        )
        st.markdown(
            f'<div style="margin:8px 0 6px 0;line-height:2;">'
            f'<span style="color:#8b949e;font-size:0.7em;">DATA INTEGRITY: </span>{legend_html}</div>',
            unsafe_allow_html=True)

        # Piotroski detail breakdown
        st.markdown(f"**Piotroski F-Score: {p.get('score','N/V')}/{p.get('max',8)}**")
        pdet = p.get("details", {})
        if pdet:
            pcols = st.columns(2)
            for i, (pk, pv) in enumerate(pdet.items()):
                pcols[i % 2].markdown(f"{'✅' if pv else '❌'} {pk}")

    with chart_col:
        if not hist.empty and "Close" in hist.columns:
            st.markdown("**📈 Kursverlauf (3 Jahre)**")
            chart_df = hist[["Close"]].rename(columns={"Close": f"{symbol}"})
            st.line_chart(chart_df, width="stretch", height=200)

        # Revenue trend bar chart
        revenues = m.get("revenues", [])
        if len(revenues) >= 2:
            st.markdown("**📊 Umsatz-Trend (letzte Jahre)**")
            rev_years = [f"FY-{i}" for i in range(len(revenues) - 1, -1, -1)]
            rev_df = pd.DataFrame({"Jahr": rev_years, "Umsatz (Mrd)": [r / 1e9 for r in reversed(revenues)]})
            st.bar_chart(rev_df.set_index("Jahr"), width="stretch", height=160)

        # Fundamentals table — two columns
        st.markdown("**📋 Fundamentaldaten**")
        sym2 = "€" if m.get("currency") == "EUR" else "$"
        rec  = (m.get("recommendation") or "").upper()
        rec_color = {"BUY": "🟢", "STRONG_BUY": "🟢", "HOLD": "🟡", "SELL": "🔴", "UNDERPERFORM": "🔴"}.get(rec, "")
        target = m.get("target_price")
        price  = m.get("price")
        upside = f" ({(target/price - 1):+.1%})" if (target and price and price > 0) else ""

        extra = [
            ("Marktkapitalisierung",   cap_fmt(m.get("mktcap"))),
            ("Enterprise Value",       cap_fmt(m.get("ev"))),
            ("KGV (trailing)",         nfmt(m.get("pe"))      if m.get("pe")      else "N/V"),
            ("KGV (forward)",          nfmt(m.get("fwd_pe"))  if m.get("fwd_pe")  else "N/V"),
            ("Kurs/Buchwert",          nfmt(m.get("price_to_book")) if m.get("price_to_book") else "N/V"),
            ("Kurs/Umsatz",            nfmt(m.get("price_to_sales")) if m.get("price_to_sales") else "N/V"),
            ("EV/FCF",                 xfmt(m.get("ev_fcf"))),
            ("Umsatz (TTM)",           cap_fmt(m.get("revenue"))),
            ("Umsatzwachstum (YoY)",   pct(m.get("revenue_growth"))),
            ("FCF",                    cap_fmt(m.get("fcf"))),
            ("Nettomarge",             pct(m.get("profit_margin"))),
            ("ROE",                    pct(m.get("roe"))),
            ("ROA",                    pct(m.get("roa"))),
            ("Debt/Equity",            nfmt(m.get("debt_to_equity")) if m.get("debt_to_equity") else "N/V"),
            ("SBC-Intensity",          pct(m.get("sbc_intensity"))),
            ("Capex/Umsatz",           pct(m.get("capex_ratio"))),
            ("CCC",                    dfmt(m.get("ccc"))),
            ("Current Ratio",          nfmt(m.get("current_ratio"))),
            ("Beta",                   nfmt(m.get("beta"))    if m.get("beta")    else "N/V"),
            ("Dividende",              pct(m.get("dividend"))  if m.get("dividend") else "N/V"),
            ("Analysten-Ziel",         f"{sym2}{target:.2f}{upside}" if target else "N/V"),
            ("Empfehlung",             f"{rec_color} {rec}"   if rec else "N/V"),
            ("# Analysten",            str(int(m["analyst_count"])) if m.get("analyst_count") else "N/V"),
            ("Mitarbeiter",            f"{int(m['employees']):,}" if m.get("employees") else "N/V"),
            ("Hauptsitz",              f"{m.get('city','')}, {m.get('country','')}".strip(", ")),
        ]
        st.markdown(_html_table(pd.DataFrame(extra, columns=["Kennzahl", "Wert"])),
                    unsafe_allow_html=True)

    st.markdown("---")

    # ── ANALYSE-TIEFE: bestimmt Quick vs. Full-Pfad ───────────────────────────
    _tiefe_d  = j.get("analyse_tiefe_data", {})
    _is_quick = _tiefe_d.get("is_quick", False)
    _is_full  = not _is_quick

    # Analyse-Tiefe Badge
    _tiefe_label    = _tiefe_d.get("tiefe",      "FULL DEEP DIVE")
    _tiefe_reason   = _tiefe_d.get("tiefe_reason","")
    _val_mode       = _tiefe_d.get("val_mode",   "FULL DCF")
    _tiefe_color    = "#da3633" if _is_quick else "#1f6feb"
    st.markdown(
        f'<div style="background:#0d1117;border:1px solid {_tiefe_color};border-radius:6px;'
        f'padding:8px 14px;margin:6px 0 14px;">'
        f'<span style="color:{_tiefe_color};font-weight:700;font-size:0.85em;letter-spacing:1px;">'
        f'🔬 ANALYSE-TIEFE: {_tiefe_label}</span>'
        f'<span style="color:#8b949e;font-size:0.78em;margin-left:12px;">{_tiefe_reason}</span>'
        f'<span style="background:{_tiefe_color}22;color:{_tiefe_color};border-radius:4px;'
        f'padding:1px 8px;font-size:0.75em;font-weight:600;margin-left:10px;">VALUATION: {_val_mode}</span>'
        f'</div>',
        unsafe_allow_html=True)

    # ── ANALYSE-MODULE ─────────────────────────────────────────────────────────
    # Schritt 2B: Daten-Konfidenz (immer zuerst — Datenqualität als Fundament)
    _render_daten_konfidenz(j, m)
    st.markdown("---")
    # Auto-Detection Engine + K-BASIS (zeigt Modus, Grund, K-Kriterien)
    _render_k_basis_engine(j, m)
    st.markdown("---")
    # Prioritäten-Logik + Reaper Anker-Skala
    _render_prioritaeten_reaper(j, m)
    st.markdown("---")
    _render_fx_pflicht(m)
    _render_flag_check(j, m)
    st.markdown("---")

    if _is_quick:
        # ── QUICK FILTER PATH (≤ $2B Mktcap) ───────────────────────────────────
        st.markdown("### ⚡ QUICK FILTER — Schritt 3+5")
        _render_moat_quick(j)
        _render_management_quick(j)
        st.markdown("---")
        _render_quick_valuation(j, m)
        st.markdown("---")

        # Financial Health (kompakt)
        st.markdown("### 4️⃣ Financial Health")
        _render_transformation(m, j)
        _render_sbc_check(j, m)
        _render_share_count_trend(m)
        _render_capex_check(j)
        _render_debt_maturity(j)
        _render_shareholder_yield(j)
        st.markdown("---")

        # Schritt 5B: SANITY-CHECK
        _render_sanity_check(j, m)
        st.markdown("---")

        # Schritt 6+7 (Quick: kein Edge/Catalyst Engine)
        st.markdown("### 6️⃣ Stress-Test · Verdict · Exit")
        _render_exit_strategy(j)
        _render_devil(j)
        _render_beneish()
        _render_technical_insider(j, m)
        _render_daten_hierarchie(m)
        _render_sec_crossval(m)

    else:
        # ── FULL DEEP DIVE PATH (> $2B Mktcap) ─────────────────────────────────
        _render_moat(j)
        _render_management(j)
        st.markdown("---")
        _render_wacc_dcf(j, m)
        st.markdown("---")

        # ── Schritt 5B: SANITY-CHECK ───────────────────────────────────────────
        _render_sanity_check(j, m)
        st.markdown("---")

        # ── Schritt 4: Financial Health ────────────────────────────────────────
        st.markdown("### 4️⃣ Financial Health")
        _render_transformation(m, j)
        _render_sbc_check(j, m)
        _render_share_count_trend(m)
        _render_capex_check(j)
        _render_debt_maturity(j)
        _render_shareholder_yield(j)
        _render_zyklus(m)
        st.markdown("---")

        # ── Schritt 5C + 5D: EDGE ENGINE · CATALYST ENGINE ────────────────────
        st.markdown("### ⚡ Schritt 5C + 5D — Edge & Catalyst Engine")
        _render_edge_engine(j, m)
        _render_catalyst_engine(j, m)
        st.markdown("---")

        # ── Schritt 6+7: Stress-Test · Devil's Advocate · Exit ─────────────────
        st.markdown("### 6️⃣ Stress-Test · Verdict · Exit")
        _render_exit_strategy(j)
        _render_prediction_tracking(j, m)
        _render_devil(j)
        _render_beneish()
        _render_technical_insider(j, m)
        _render_daten_hierarchie(m)
        _render_sec_crossval(m)


def _k_threshold(name):
    """Threshold-Text für K-Kriterien (alle Modi)."""
    t = {
        # 5S Standard
        "ROIC > 20%": "> 20%", "FCF-Marge ≥ 20%": "≥ 20%",
        "Op. Leverage": "Ja",  "Piotroski ≥ 7": "≥ 7/9",
        "EPS-CAGR ≥ 12%": "≥ 12%", "SBC < 10%": "< 10%",
        # 5F Finanz
        "ROE > 12%": "> 12%", "FCF-Marge ≥ 15%": "≥ 15%",
        "EPS-CAGR ≥ 10%": "≥ 10%",
        # 5SaaS
        "ROIC > 15%": "> 15%", "Bruttomarge ≥65%": "≥ 65%",
        "Rev-CAGR ≥ 15%": "≥ 15%", "EPS-CAGR ≥ 15%": "≥ 15%", "SBC < 15%": "< 15%",
        # 5I Infrastruktur
        "Op. Marge ≥ 40%": "≥ 40%", "ND/EBITDA < 6x": "< 6x",
        "FCF > 0": "> 0", "Capex ≤ 30%": "≤ 30%", "Piotroski ≥ 5": "≥ 5/9",
        # 5V Versorger
        "ROE ≥ 10%": "≥ 10%", "Div.-Rendite ≥4%": "≥ 4%",
        "Payout ≤ 80%": "≤ 80%", "Op. Marge ≥ 30%": "≥ 30%", "ND/EBITDA < 5x": "< 5x",
        # 5K Sachwerte
        "FCF-Marge ≥ 5%": "≥ 5%", "EV/EBITDA ≤ 8x": "≤ 8x",
        "ND/EBITDA < 3x": "< 3x", "ROA > 5%": "> 5%",
        # 4P Piotroski-Override
        "ROIC ≥ 10%": "≥ 10%", "ND/EBITDA < 4x": "< 4x",
    }
    return t.get(name, "—")

def _e_threshold(name):
    """Threshold-Text für E-Kriterien (alle Modi)."""
    t = {
        # 5S Standard
        "Bruttomarge ≥ 60%": "≥ 60%", "Op. Marge ≥ 20%": "≥ 20%",
        "Rev-CAGR ≥ 8%": "≥ 8%", "Net Debt/EBITDA<2x": "< 2x",
        "Capex/Umsatz ≤ 5%": "≤ 5%", "CCC < 30d": "< 30d",
        # 5F Finanz
        "Bruttomarge ≥ 30%": "≥ 30%", "ROE ≥ 15%": "≥ 15%",
        "Rev-CAGR ≥ 6%": "≥ 6%", "ND/EBITDA < 4x": "< 4x",
        "Piotroski ≥ 5": "≥ 5/9",
        # 5SaaS
        "Bruttomarge ≥ 70%": "≥ 70%", "Op. Marge ≥ 15%": "≥ 15%",
        "Rev-CAGR ≥ 20%": "≥ 20%", "ND/EBITDA < 2x": "< 2x",
        "SBC < 10%": "< 10%", "CCC < 0d": "< 0d",
        # 5I / 5V
        "Bruttomarge ≥ 40%": "≥ 40%", "EBITDA > 0": "> 0",
        "Rev-CAGR ≥ 3%": "≥ 3%", "ROA > 3%": "> 3%", "Capex ≤ 35%": "≤ 35%",
        # 5K
        "Rev-CAGR ≥ 0%": "≥ 0%", "P/B < 2x": "< 2x",
        "Div.-Rendite ≥ 2%": "≥ 2%", "Op. Leverage": "Ja",
        # 4P
        "P/B < 1.5x": "< 1.5x", "ROA > 3%": "> 3%",
        "Op. Marge ≥ 10%": "≥ 10%",
    }
    return t.get(name, "—")


# ══════════════════════════════════════════════════════════════════════════════
# JACK MODULE ENGINE  –  TRANSFORMATION · MOAT · MANAGEMENT · CAPEX · DEBT
# ══════════════════════════════════════════════════════════════════════════════

# ── TRANSFORMATION-PROTOKOLL ──────────────────────────────────────────────────
def _calc_transformation_flag(m: dict) -> dict:
    """Prüft ob TRANSFORMATION-PROTOKOLL aktiv wird (5T K-BASIS)."""
    fcf  = m.get("fcf_margin") or 0
    gm   = m.get("gross_margin") or 0
    ol   = m.get("op_leverage", False)
    nd   = m.get("nd_ebitda")
    cr   = m.get("current_ratio")
    eps  = m.get("eps_cagr") or 0

    if fcf >= 0.20:
        return {"active": False, "reason": "FCF-Marge ≥ 20% – kein Transformationsbedarf", "k_basis_mode": None}

    q1 = gm >= 0.50 and ol
    q2 = nd is None or nd < 3.0
    q3 = cr is None or cr >= 1.0

    reasons = []
    if not q1: reasons.append("Bruttomarge < 50% oder kein Op. Leverage")
    if not q2: reasons.append(f"Net Debt/EBITDA {nd:.1f}x ≥ 3x")
    if not q3: reasons.append(f"Current Ratio {cr:.2f} < 1x")

    active = q1 and q2 and q3
    return {
        "active": active,
        "q1_fcf_path": q1,   "q2_horizon": q2,   "q3_balance": q3,
        "reason": "FCF < 20% – Transformation qualifiziert" if active else f"FCF < 20% – NICHT qualifiziert: {'; '.join(reasons)}",
        "k_basis_mode": "5T (Transformation)" if active else None,
        "reasons_fail": reasons,
        "fcf": fcf, "gm": gm, "nd": nd, "cr": cr,
    }


# ── MOAT-VERIFIKATION ─────────────────────────────────────────────────────────
def _calc_moat_score(m: dict) -> dict:
    """4-Kriterien Moat Score. Quellen: yfinance-Proxies."""
    details = {}
    score = 0

    # 1. Preissetzungsmacht → Bruttomarge > 50%
    gm = m.get("gross_margin") or 0
    ok = gm > 0.50
    details["Preissetzungsmacht"] = {"pass": ok, "val": pct(gm), "note": "> 50% Bruttomarge"}
    if ok: score += 1

    # 2. Switching Cost → FCF-Marge > 15% (Customer-Lock-in Proxy)
    fcf = m.get("fcf_margin") or 0
    ok2 = fcf > 0.15
    details["Switching Cost (Proxy)"] = {"pass": ok2, "val": pct(fcf), "note": "> 15% FCF-Marge"}
    if ok2: score += 1

    # 3. Marktanteil-Trend → Rev-CAGR > 8%
    rc = m.get("rev_cagr") or 0
    ok3 = rc > 0.08
    details["Marktanteil-Trend"] = {"pass": ok3, "val": pct(rc), "note": "> 8% Rev-CAGR"}
    if ok3: score += 1

    # 4. Skaleneffekte → Op. Leverage vorhanden
    ol = m.get("op_leverage", False)
    details["Skaleneffekte"] = {"pass": ol, "val": "Ja" if ol else "Nein", "note": "Op. Leverage aktiv"}
    if ol: score += 1

    if score == 4:   label, color = "🟢 STARK",   "#3fb950"
    elif score >= 2: label, color = "🟡 SOLIDE",  "#d29922"
    else:            label, color = "🔴 SCHWACH",  "#da3633"

    return {"score": score, "max": 4, "details": details, "label": label, "color": color}


# ── MANAGEMENT-SCORE ──────────────────────────────────────────────────────────
def _calc_management_score(m: dict) -> dict:
    """5-Kriterien Management-Score (FULL DEEP DIVE)."""
    details = {}
    score = 0

    # 1. ROIC > 15% (Capital Allocation)
    roic = m.get("roic") or 0
    ok = roic > 0.15
    details["Capital Allocation (ROIC)"] = {"pass": ok, "val": pct(roic), "note": "> 15%"}
    if ok: score += 1

    # 2. SBC < 5% (Aktionärsfreundlich)
    sbc = m.get("sbc_intensity") or 0
    ok2 = sbc < 0.05
    details["SBC-Disziplin"] = {"pass": ok2, "val": pct(sbc), "note": "< 5% Umsatz"}
    if ok2: score += 1

    # 3. ROE > 15%
    roe = m.get("roe") or 0
    ok3 = roe > 0.15
    details["ROE-Qualität"] = {"pass": ok3, "val": pct(roe), "note": "> 15%"}
    if ok3: score += 1

    # 4. Equity Ratio > 30% (solide Bilanz-Führung)
    eq = m.get("equity_ratio") or 0
    ok4 = eq > 0.30
    details["Bilanzführung (EK-Quote)"] = {"pass": ok4, "val": pct(eq), "note": "> 30%"}
    if ok4: score += 1

    # 5. Rev-Wachstum UND Marge stabil (Execution)
    rc  = m.get("rev_cagr") or 0
    opm = m.get("op_margin") or 0
    ok5 = rc > 0.05 and opm > 0.10
    details["Execution (Wachstum+Marge)"] = {"pass": ok5, "val": f"{pct(rc)} / {pct(opm)}", "note": "Rev>5% & OpM>10%"}
    if ok5: score += 1

    if score >= 4:   label, color = "🟢 STARK",     "#3fb950"
    elif score >= 2: label, color = "🟡 SOLIDE",    "#d29922"
    else:            label, color = "🔴 SCHWACH",    "#da3633"

    return {"score": score, "max": 5, "details": details, "label": label, "color": color}


# ── CAPEX-CHECK ───────────────────────────────────────────────────────────────
def _calc_capex_check(m: dict) -> dict:
    """Triggered wenn Capex/Umsatz > 5%. Zeigt FCF-Qualitäts-Analyse."""
    cr  = m.get("capex_ratio") or 0
    fcf = m.get("fcf_margin") or 0
    gm  = m.get("gross_margin") or 0
    rev = m.get("revenue") or 0
    fcf_abs = m.get("fcf") or 0

    triggered = cr > 0.05
    intensity = "KRITISCH" if cr > 0.15 else ("ERHÖHT" if cr > 0.08 else "MODERAT")
    color = "#da3633" if cr > 0.15 else ("#d29922" if cr > 0.08 else "#3fb950")

    maintenance_est = rev * 0.03 if rev else None
    growth_capex_est = (rev * cr - maintenance_est) if (maintenance_est and rev) else None

    return {
        "triggered": triggered,
        "ratio": cr,
        "intensity": intensity,
        "color": color,
        "fcf_quality": "GUT" if fcf > 0.15 else ("MITTEL" if fcf > 0 else "NEGATIV"),
        "maintenance_est": maintenance_est,
        "growth_capex_est": growth_capex_est,
        "note": f"Capex {pct(cr)} > 5% Schwelle – FCF-Qualität prüfen" if triggered else f"Capex {pct(cr)} ≤ 5% – keine Auffälligkeiten",
    }


# ── DEBT MATURITY CHECK ───────────────────────────────────────────────────────
def _calc_debt_maturity(m: dict) -> dict:
    """Approximierter Debt Maturity Check (yfinance hat keine Fälligkeitspläne)."""
    nd     = m.get("nd_ebitda")
    cr     = m.get("current_ratio")
    de     = m.get("debt_to_equity")
    eq     = m.get("equity_ratio") or 0
    nc     = m.get("net_cash")

    red_conditions = []
    yellow_conditions = []

    if nd is not None and nd > 3.0:   red_conditions.append(f"Net Debt/EBITDA {nd:.1f}x > 3x")
    elif nd is not None and nd > 2.0: yellow_conditions.append(f"Net Debt/EBITDA {nd:.1f}x > 2x")

    if cr is not None and cr < 1.0:   red_conditions.append(f"Current Ratio {cr:.2f} < 1x (Liquiditätsrisiko)")
    elif cr is not None and cr < 1.5: yellow_conditions.append(f"Current Ratio {cr:.2f} < 1.5x")

    if eq < 0.20:   red_conditions.append(f"EK-Quote {pct(eq)} < 20% (hohes Fremdkapital)")
    elif eq < 0.35: yellow_conditions.append(f"EK-Quote {pct(eq)} < 35%")

    if nc is not None and nc < 0:
        if abs(nc) > 5e9: yellow_conditions.append(f"Netto-Schulden {cap_fmt(abs(nc))}")

    if red_conditions:
        status, color, icon = "KRITISCH", "#da3633", "🔴"
        fv_adj = "−10% FV-Abschlag (Pflicht per JACK-Regel #17)"
    elif yellow_conditions:
        status, color, icon = "ERHÖHT",   "#d29922", "🟡"
        fv_adj = "Risiko-Aufschlag im WACC empfohlen"
    else:
        status, color, icon = "NIEDRIG",  "#3fb950", "🟢"
        fv_adj = "Kein FV-Abschlag notwendig"

    return {
        "status": status, "color": color, "icon": icon,
        "fv_adj": fv_adj,
        "red": red_conditions, "yellow": yellow_conditions,
        "nd": nd, "cr": cr, "de": de, "eq": eq, "nc": nc,
    }


# ── EXIT-STRATEGIE ────────────────────────────────────────────────────────────
def _calc_exit_strategy(m: dict, j: dict) -> dict:
    """Generiert Exit-Strategie und Upgrade/Downgrade Trigger."""
    rating  = j.get("rating", "SCHROTT")
    rs      = j.get("reaper_score", 1)
    price   = m.get("price") or 0
    sym     = "€" if m.get("currency") == "EUR" else "$"
    roic    = m.get("roic") or 0
    fcf     = m.get("fcf_margin") or 0
    nd      = m.get("nd_ebitda")

    upgrade_triggers   = []
    downgrade_triggers = []
    exit_conditions    = []

    if rating in ("KAUFEN", "BEOBACHTEN"):
        if roic < 0.20:   upgrade_triggers.append("ROIC steigt dauerhaft über 20%")
        if fcf < 0.20:    upgrade_triggers.append("FCF-Marge erreicht ≥ 20%")
        if nd and nd > 2: upgrade_triggers.append(f"Net Debt/EBITDA sinkt unter 2x (aktuell {nd:.1f}x)")

        downgrade_triggers.append("ROIC fällt unter 10% für 2 Quartale")
        downgrade_triggers.append("FCF wird dauerhaft negativ")
        if nd: downgrade_triggers.append(f"Net Debt/EBITDA steigt über {max(3.0, (nd or 0) + 1.5):.1f}x")
        downgrade_triggers.append("Guidance-Senkung > 15% bei Kernmetrik")

        if price > 0:
            stop_loss = price * 0.80
            exit_conditions.append(f"Stop-Loss: {sym}{stop_loss:.2f} (−20% vom Kauf)")
            exit_conditions.append("Bewertung > 2× fairer Wert (signifikantes Überschreiten)")
            exit_conditions.append("Moat-Erosion: Bruttomarge −5pp über 4 Quartale")

    return {
        "upgrade": upgrade_triggers,
        "downgrade": downgrade_triggers,
        "exit": exit_conditions,
    }


# ── EDGE & CATALYST SCORE ─────────────────────────────────────────────────────
def _calc_edge_catalyst(m: dict, j: dict) -> dict:
    """
    JACK Schritt 5C + 5D: Edge Engine & Catalyst Engine.
    Vollständige 4-Teil EDGE + 6-Teil CATALYST Analyse.
    """
    moat   = j.get("moat", {})
    mgmt   = j.get("management", {})
    rs     = j.get("reaper_score", 1)
    rc     = m.get("rev_cagr") or 0
    fcf    = m.get("fcf_margin") or 0
    pe     = m.get("pe") or 999
    fwd_pe = m.get("fwd_pe") or 999
    price  = m.get("price") or 0
    target = m.get("target_price") or 0
    short  = m.get("short_pct") or 0
    beta   = m.get("beta") or 1.0
    tech   = j.get("technical", {})
    konfidenz = j.get("konfidenz", ("🔴", "NIEDRIG", "#da3633"))
    moat_s = moat.get("score", 0)
    mgmt_s = mgmt.get("score", 0)
    dcf    = j.get("dcf", {})
    rdcf   = j.get("reverse_dcf", {})

    # ── EDGE ENGINE (Schritt 5C) ─────────────────────────────────────────────
    # 1. Erwartungs-Check
    konsens_upside = (target / price - 1) if (target > 0 and price > 0) else None
    dcf_fv = dcf.get("iv") if dcf.get("available") else None
    dcf_upside = (dcf_fv / price - 1) if (dcf_fv and price > 0) else None
    implied_g  = rdcf.get("implied_g") if rdcf.get("available") else None
    actual_g   = rdcf.get("actual_g") if rdcf.get("available") else None
    # Delta: DCF vs Konsens
    if dcf_upside is not None and konsens_upside is not None:
        delta = dcf_upside - konsens_upside
    elif dcf_upside is not None:
        delta = dcf_upside
    else:
        delta = None

    if delta is not None and delta > 0.20:    erwartung_score = "🔥"; erwartung_lbl = f"DCF signifikant über Konsens (+{delta:.0%})"
    elif delta is not None and delta > 0.10:  erwartung_score = "🟢"; erwartung_lbl = f"DCF leicht über Konsens (+{delta:.0%})"
    elif delta is not None and delta > 0.05:  erwartung_score = "🟡"; erwartung_lbl = f"Minimaler Edge (+{delta:.0%})"
    elif delta is not None:                   erwartung_score = "❌"; erwartung_lbl = f"Kein Erwartungs-Edge ({delta:.0%})"
    else:                                     erwartung_score = "❌"; erwartung_lbl = "DCF nicht verfügbar – kein Check möglich"

    # 2. Narrativ-Status
    # Markt-Narrativ ableiten aus Bewertung + Beta
    if pe > 0 and pe < 12:      narrativ_markt = "Zykliker / Value Trap"
    elif pe > 0 and pe < 20:    narrativ_markt = "Reife Bewertung / Moderate Erwartungen"
    elif pe > 0 and pe < 35:    narrativ_markt = "Growth-Prämie erwartet"
    elif pe > 0:                narrativ_markt = "High-Growth / Hype-Preis"
    else:                       narrativ_markt = "Neg. Gewinn / Pre-Profit"

    if (rc or 0) > 0.15 and (fcf or 0) > 0.20:
        narrativ_real = "Strukturelles Wachstum + FCF-Qualität"
        if pe > 0 and pe < 25:  narrativ_shift = "🔥"; narrativ_thesis = "Markt unterschätzt FCF-Qualität bei moderater Bewertung"
        else:                   narrativ_shift = "🟡"; narrativ_thesis = "Qualität bestätigt – aber Bewertung bereits reflektiert"
    elif (rc or 0) > 0.08 and (fcf or 0) > 0.15:
        narrativ_real  = "Solides Wachstum + akzeptable FCF"
        narrativ_shift = "🟡"
        narrativ_thesis = "Markt-Narrativ weitgehend korrekt – kein klarer Shift"
    elif (rc or 0) < 0.02:
        narrativ_real  = "Stagnation / Umsatz-Risiko"
        narrativ_shift = "❌"
        narrativ_thesis = "Markt-Narrativ bestätigt – kein Edge in Wachstums-Story"
    else:
        narrativ_real  = "Gemischte Signale"
        narrativ_shift = "🟡"
        narrativ_thesis = "Narrativ noch nicht entschieden – Earnings-Katalysator nötig"

    # 3. Timing-Setup
    from_hi = tech.get("from_hi", 0) if tech.get("available") else 0
    overreaction = False
    if from_hi < -0.20 and beta < 1.3 and (j.get("k_met", 0) >= j.get("k_basis", 5)):
        timing_score = "🔥"; timing_lbl = f"Dislocation: −{abs(from_hi):.0%} vom 52W-Hoch, K-BASIS intakt"
        overreaction = True
    elif from_hi < -0.10:
        timing_score = "🟢"; timing_lbl = f"Akkumulations-Phase: −{abs(from_hi):.0%} vom 52W-Hoch"
    elif from_hi < -0.05:
        timing_score = "🟡"; timing_lbl = f"Leichter Rücksetzer: −{abs(from_hi):.0%} — Watchlist"
    else:
        timing_score = "❌"; timing_lbl = f"Nahe 52W-Hoch — kein günstiges Timing-Setup"

    # Zusatz: Short-Interest als contrarian Signal
    short_note = ""
    if short > 0.15:
        short_note = f"⚠️ Hohe Short-Quote ({short:.0%}) — Squeeze-Potenzial möglich"
    elif short > 0.05:
        short_note = f"Short Interest: {short:.0%} — moderat"

    # 4. Edge Score aggregieren (3-Felder Methode)
    e_scores = [erwartung_score, narrativ_shift, timing_score]
    fire_count  = e_scores.count("🔥")
    green_count = e_scores.count("🟢") + fire_count

    if fire_count >= 2:
        edge_final = "🔥 ELITE EDGE"; edge_thesis_final = f"Markt unterschätzt {m.get('name','diese Aktie')} massiv"
    elif green_count >= 3:
        edge_final = "🔥 ELITE EDGE"; edge_thesis_final = f"Alle 3 EDGE-Faktoren positiv – hohe Überzeugung"
    elif green_count >= 2:
        edge_final = "🟢 GUTER EDGE"; edge_thesis_final = narrativ_thesis
    elif green_count == 1:
        edge_final = "🟡 SCHWACH";    edge_thesis_final = "Einzelner Edge-Faktor – nicht ausreichend für High-Conviction"
    else:
        edge_final = "❌ KEIN EDGE";  edge_thesis_final = "Kein struktureller Marktfehler identifiziert"

    # EDGE-Deckel bei schlechter Konfidenz
    if konfidenz[1] == "NIEDRIG":
        if "ELITE" in edge_final or "GUTER" in edge_final:
            edge_final = "🟡 BEGRENZT (🔴 Konfidenz)"
            edge_thesis_final += " [Konfidenz-Deckel: max 🟡]"

    # ── CATALYST ENGINE (Schritt 5D) ─────────────────────────────────────────
    # Catalyst-Stärke
    cat_events = []
    if (m.get("analyst_count") or 0) > 0:
        cat_events.append({"event": "Earnings (nächstes Quartal)", "type": "Earnings",
                           "erwartung": "hoch" if (fwd_pe or 999) < (pe or 999) else "neutral",
                           "potenzial": "🟢" if (fwd_pe or 999) < (pe or 999) * 0.9 else "🟡"})
    if target > 0 and price > 0 and target / price > 1.15:
        cat_events.append({"event": f"Analysten-Ziel: {pct(target/price - 1)} Upside",
                           "type": "Analyst-Revision", "erwartung": "positiv", "potenzial": "🟢"})
    if short > 0.10:
        cat_events.append({"event": f"Short-Squeeze Potenzial ({short:.0%} short)",
                           "type": "Positionierung", "erwartung": "hoch", "potenzial": "🟡"})

    # Catalyst-Stärke Score
    cat_pts = 0.0
    if fwd_pe > 0 and pe > 0 and fwd_pe < pe * 0.9: cat_pts += 0.33  # EPS-Wachstum prognostiziert
    if rc > 0.12:                                    cat_pts += 0.25
    if fcf > 0.20:                                   cat_pts += 0.20
    if target > 0 and price > 0 and target / price > 1.10: cat_pts += 0.22

    if cat_pts >= 0.70:   catalyst_final = "🔥 HIGH IMPACT"; cat_thesis = "Mehrere Catalysts mit hohem Überraschungspotenzial"
    elif cat_pts >= 0.45: catalyst_final = "🟢 SOLIDE";      cat_thesis = "Earnings-Wachstum + Analyst-Upside als Treiber"
    elif cat_pts >= 0.25: catalyst_final = "🟡 MODERAT";     cat_thesis = "Einzelner Catalyst – Dead Money Risiko beachten"
    else:                 catalyst_final = "❌ KEIN";        cat_thesis = "Kein kurzfristiger Catalyst sichtbar – Dead Money Risiko"

    # Timing-Fenster
    if timing_score in ("🔥", "🟢"):  timing_fenster = "Kurzfristig (0–3 Monate)"
    elif timing_score == "🟡":         timing_fenster = "Mittelfristig (3–9 Monate)"
    else:                              timing_fenster = "Langfristig (>9 Monate) oder kein Setup"

    # Failure-Risiko
    if j.get("k_met", 0) < j.get("k_basis", 5):
        failure_note = f"K-BASIS nicht vollständig ({j.get('k_met',0)}/{j.get('k_basis',5)}) → Thesis-Bruch bei Miss"
        failure_kurs = "−15% bis −30%"
    elif (m.get("nd_ebitda") or 0) > 2.0:
        failure_note = "Hohe Verschuldung → bei Miss + steigenden Zinsen Kursreaktion verstärkt"
        failure_kurs = "−20% bis −35%"
    else:
        failure_note = "Solide Fundamentals – Reaktion bei Miss begrenzt"
        failure_kurs = "−5% bis −15%"

    # Catalyst Score (3-Felder: Stärke, Timing, Überraschung)
    overrpr_score = "🟢" if (implied_g is not None and actual_g is not None and actual_g > implied_g * 1.05) else (
                   "🟡" if (implied_g is not None and actual_g is not None and actual_g > implied_g * 0.95) else "🔴")
    c_scores = [("🔥" if cat_pts >= 0.70 else "🟢" if cat_pts >= 0.45 else "🟡" if cat_pts >= 0.25 else "❌"),
                ("🟢" if timing_score in ("🔥","🟢") else "🟡" if timing_score == "🟡" else "🔴"),
                overrpr_score]
    c_fire  = c_scores.count("🔥")
    c_green = c_scores.count("🟢") + c_fire
    if c_green >= 3:   catalyst_score_lbl = "🔥 HIGH IMPACT SETUP"
    elif c_green >= 2: catalyst_score_lbl = "🟢 SOLIDES SETUP"
    elif c_green >= 1: catalyst_score_lbl = "🟡 SCHWACH"
    else:              catalyst_score_lbl = "❌ KEIN CATALYST"

    return {
        # Simple labels for summary panel
        "edge":     edge_final,
        "catalyst": catalyst_final,
        # Edge Engine detail
        "edge_detail": {
            "erwartung_score": erwartung_score, "erwartung_lbl": erwartung_lbl,
            "narrativ_markt": narrativ_markt,   "narrativ_real":  narrativ_real,
            "narrativ_shift": narrativ_shift,   "narrativ_thesis": narrativ_thesis,
            "timing_score":   timing_score,     "timing_lbl":      timing_lbl,
            "short_note":     short_note,       "overreaction":    overreaction,
            "edge_final":     edge_final,       "edge_thesis":     edge_thesis_final,
            "e_scores":       e_scores,
            "dcf_upside":     dcf_upside,       "konsens_upside":  konsens_upside,
            "delta":          delta,
        },
        # Catalyst Engine detail
        "catalyst_detail": {
            "events":         cat_events,
            "cat_pts":        cat_pts,
            "catalyst_final": catalyst_final,   "cat_thesis":      cat_thesis,
            "timing_fenster": timing_fenster,
            "failure_note":   failure_note,     "failure_kurs":    failure_kurs,
            "overrpr_score":  overrpr_score,
            "c_scores":       c_scores,
            "catalyst_score_lbl": catalyst_score_lbl,
            "implied_g":      implied_g,        "actual_g":        actual_g,
        },
    }


# ── EDGE ENGINE RENDER (Schritt 5C) ──────────────────────────────────────────
def _render_edge_engine(j: dict, m: dict):
    """JACK Schritt 5C – Edge Engine: Erwartung · Narrativ · Timing · Score."""
    ec  = j.get("edge_catalyst", {})
    ed  = ec.get("edge_detail", {})
    if not ed:
        return
    sym = "€" if m.get("currency") == "EUR" else "$"
    price = m.get("price") or 0

    with st.expander(f"⚡ Schritt 5C — EDGE ENGINE: {ed.get('edge_final','—')}", expanded=False):
        st.caption("JACK Klasse B: Identifikation von Marktfehlbewertungen — subjektive Analysten-Einschätzung, kein Scoring-Modell")

        col1, col2, col3 = st.columns(3)

        # 1. Erwartungs-Check
        with col1:
            e_icon = ed.get("erwartung_score","❌")
            e_col  = "#3fb950" if e_icon in ("🟢","🔥") else "#d29922" if e_icon == "🟡" else "#da3633"
            st.markdown(f'<div style="border:1px solid #30363d;border-radius:8px;padding:12px;height:100%;">'
                        f'<div style="color:#8b949e;font-size:0.72em;letter-spacing:1px;margin-bottom:6px;">① ERWARTUNGS-CHECK</div>'
                        f'<div style="font-size:1.4em;">{e_icon}</div>'
                        f'<div style="color:{e_col};font-weight:700;font-size:0.85em;margin-top:4px;">{ed.get("erwartung_lbl","—")}</div>',
                        unsafe_allow_html=True)
            dcf_up  = ed.get("dcf_upside")
            kon_up  = ed.get("konsens_upside")
            if dcf_up is not None:
                st.markdown(f'<div style="color:#8b949e;font-size:0.75em;margin-top:6px;">'
                            f'DCF-Upside: <b style="color:#e6edf3;">{dcf_up:+.1%}</b>'
                            + (f' · Konsens: <b style="color:#e6edf3;">{kon_up:+.1%}</b>' if kon_up is not None else "")
                            + f'</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('</div>', unsafe_allow_html=True)

        # 2. Narrativ-Status
        with col2:
            n_icon = ed.get("narrativ_shift","❌")
            n_col  = "#3fb950" if n_icon in ("🟢","🔥") else "#d29922" if n_icon == "🟡" else "#da3633"
            st.markdown(f'<div style="border:1px solid #30363d;border-radius:8px;padding:12px;height:100%;">'
                        f'<div style="color:#8b949e;font-size:0.72em;letter-spacing:1px;margin-bottom:6px;">② NARRATIV-STATUS</div>'
                        f'<div style="font-size:1.4em;">{n_icon}</div>'
                        f'<div style="color:#8b949e;font-size:0.78em;margin-top:4px;">Markt: <i>{ed.get("narrativ_markt","—")}</i></div>'
                        f'<div style="color:#e6edf3;font-size:0.78em;">Realität: <b>{ed.get("narrativ_real","—")}</b></div>'
                        f'<div style="color:{n_col};font-size:0.8em;margin-top:6px;font-weight:600;">'
                        f'Shift: {ed.get("narrativ_thesis","—")}</div></div>',
                        unsafe_allow_html=True)

        # 3. Timing-Setup
        with col3:
            t_icon = ed.get("timing_score","❌")
            t_col  = "#3fb950" if t_icon in ("🟢","🔥") else "#d29922" if t_icon == "🟡" else "#da3633"
            overr  = ed.get("overreaction", False)
            st.markdown(f'<div style="border:1px solid #30363d;border-radius:8px;padding:12px;height:100%;">'
                        f'<div style="color:#8b949e;font-size:0.72em;letter-spacing:1px;margin-bottom:6px;">③ TIMING-SETUP</div>'
                        f'<div style="font-size:1.4em;">{t_icon}</div>'
                        f'<div style="color:{t_col};font-weight:700;font-size:0.85em;margin-top:4px;">{ed.get("timing_lbl","—")}</div>'
                        + (f'<div style="color:#3fb950;font-size:0.75em;margin-top:4px;">🔥 Überreaktion erkannt</div>' if overr else "")
                        + (f'<div style="color:#d29922;font-size:0.75em;margin-top:4px;">{ed.get("short_note","")}</div>' if ed.get("short_note") else "")
                        + '</div>', unsafe_allow_html=True)

        st.markdown("---")

        # 4. Edge Score
        e_final = ed.get("edge_final","❌ KEIN EDGE")
        e_thesis= ed.get("edge_thesis","—")
        ef_col  = "#3fb950" if "ELITE" in e_final or "GUT" in e_final else "#d29922" if "SCHWACH" in e_final else "#da3633"
        if "ELITE" in e_final or "🔥" in e_final:  ef_col = "#e94560"
        e_scores = ed.get("e_scores",[])
        score_str = " · ".join(["①"+s for s in e_scores[:1]] + ["②"+s for s in e_scores[1:2]] + ["③"+s for s in e_scores[2:3]])
        st.markdown(
            f'<div style="background:#0d1117;border:1px solid {ef_col};border-radius:8px;padding:14px 18px;">'
            f'<div style="color:#8b949e;font-size:0.72em;letter-spacing:1px;">EDGE SCORE</div>'
            f'<div style="color:{ef_col};font-size:1.3em;font-weight:800;">{e_final}</div>'
            f'<div style="color:#8b949e;font-size:0.8em;margin:4px 0;">{score_str}</div>'
            f'<div style="color:#c9d1d9;font-size:0.88em;font-style:italic;margin-top:8px;">'
            f'EDGE-THESIS: {e_thesis}</div>'
            f'<div style="color:#6e7681;font-size:0.7em;margin-top:6px;">'
            f'RULE: EDGE darf NIEMALS alleinige Kaufbasis sein · Nur gültig wenn DNA-CHECK + VERIFIED-Daten solide</div>'
            f'</div>', unsafe_allow_html=True)


# ── CATALYST ENGINE RENDER (Schritt 5D) ──────────────────────────────────────
def _render_catalyst_engine(j: dict, m: dict):
    """JACK Schritt 5D – Catalyst Engine: Events · Stärke · Timing · Failure Risk · Score."""
    ec  = j.get("edge_catalyst", {})
    cd  = ec.get("catalyst_detail", {})
    if not cd:
        return
    sym = "€" if m.get("currency") == "EUR" else "$"

    with st.expander(f"⚡ Schritt 5D — CATALYST ENGINE: {cd.get('catalyst_score_lbl','—')}", expanded=False):
        st.caption("Kursbewegenden Catalysts identifizieren · Klasse B Best Effort")

        col1, col2 = st.columns([1.4, 1])

        with col1:
            st.markdown("**① Nächste Catalysts (0–6 Monate)**")
            events = cd.get("events", [])
            if events:
                for ev in events:
                    pot = ev.get("potenzial","🟡")
                    pot_col = "#3fb950" if pot == "🟢" else "#d29922" if pot == "🟡" else "#da3633"
                    st.markdown(
                        f'<div style="background:#161b22;border-left:3px solid {pot_col};'
                        f'border-radius:0 4px 4px 0;padding:5px 10px;margin:3px 0;">'
                        f'<span style="color:{pot_col};font-weight:700;">{pot}</span> &nbsp;'
                        f'<span style="color:#e6edf3;font-size:0.9em;">{ev.get("event","—")}</span><br>'
                        f'<span style="color:#8b949e;font-size:0.78em;">Erwartung: {ev.get("erwartung","—")}</span>'
                        f'</div>', unsafe_allow_html=True)
            else:
                st.caption("Keine spezifischen kurzfristigen Catalysts aus Datenlage ableitbar")

            st.markdown("**② Catalyst-Stärke**")
            cat_pts = cd.get("cat_pts", 0)
            cat_bar = min(100, int(cat_pts * 100))
            bar_col = "#3fb950" if cat_pts >= 0.70 else "#d29922" if cat_pts >= 0.45 else "#da3633"
            st.markdown(
                f'<div style="background:#21262d;border-radius:4px;height:8px;margin:6px 0;">'
                f'<div style="width:{cat_bar}%;background:{bar_col};border-radius:4px;height:8px;"></div></div>'
                f'<span style="color:{bar_col};font-size:0.82em;font-weight:600;">{cd.get("catalyst_final","—")}</span>'
                f' — {cd.get("cat_thesis","—")}', unsafe_allow_html=True)

            st.markdown("**③ Timing-Fenster**")
            st.markdown(f"📅 {cd.get('timing_fenster','—')}")

        with col2:
            # 4. Markt vs Realität (Reverse-DCF basiert)
            st.markdown("**④ Markt-Erwartung vs. Realität**")
            ig = cd.get("implied_g"); ag = cd.get("actual_g")
            if ig is not None and ag is not None:
                overrpr = cd.get("overrpr_score","🔴")
                op_col = "#3fb950" if overrpr == "🟢" else "#d29922" if overrpr == "🟡" else "#da3633"
                st.markdown(
                    f'<div style="background:#161b22;border-radius:6px;padding:10px 12px;">'
                    f'<div style="color:#8b949e;font-size:0.8em;">Markt erwartet: <b style="color:#e6edf3;">{ig:.1%} Wachstum</b> (Reverse-DCF)</div>'
                    f'<div style="color:#8b949e;font-size:0.8em;">Realität (Hist.): <b style="color:#e6edf3;">{ag:.1%} Rev-CAGR</b></div>'
                    f'<div style="color:{op_col};font-size:0.85em;font-weight:700;margin-top:6px;">'
                    f'{overrpr} Überraschungspotenzial: {"Hoch" if overrpr == "🟢" else "Mittel" if overrpr == "🟡" else "Gering"}</div>'
                    f'</div>', unsafe_allow_html=True)
            else:
                st.caption("Reverse-DCF nicht verfügbar")

            # 5. Failure-Risiko
            st.markdown("**⑤ Failure-Risiko**")
            st.warning(f"Was wenn Catalyst NICHT zündet?\n{cd.get('failure_note','—')}\nKursreaktion: {cd.get('failure_kurs','—')}")

            # 6. Catalyst Score
            st.markdown("**⑥ Catalyst Score**")
            c_scores = cd.get("c_scores", [])
            c_lbl    = cd.get("catalyst_score_lbl","—")
            cs_col   = "#e94560" if "🔥" in c_lbl else "#3fb950" if "SOLID" in c_lbl or "SOLIDE" in c_lbl else "#d29922"
            score_line = ""
            for i, s in enumerate(c_scores):
                labels = ["Stärke", "Timing", "Überraschung"]
                score_line += f'<span style="margin-right:12px;">{labels[i] if i < len(labels) else "?"}: {s}</span>'
            st.markdown(
                f'<div style="background:#0d1117;border:1px solid {cs_col};border-radius:8px;padding:12px 16px;">'
                f'<div style="color:#8b949e;font-size:0.75em;">{score_line}</div>'
                f'<div style="color:{cs_col};font-weight:800;font-size:1.1em;margin-top:6px;">{c_lbl}</div>'
                f'<div style="color:#8b949e;font-size:0.78em;margin-top:4px;font-style:italic;">'
                f'CATALYST-THESIS: {cd.get("cat_thesis","—")}</div>'
                f'</div>', unsafe_allow_html=True)


# ── PREDICTION TRACKING & BEOBACHTEN-PROTOKOLL ──────────────────────────────
def _render_prediction_tracking(j: dict, m: dict):
    """PREDICTION TRACKING (Schritt 7) + BEOBACHTEN-PROTOKOLL."""
    rating  = j.get("rating","SCHROTT")
    rs      = j.get("reaper_score",1)
    sym     = "€" if m.get("currency") == "EUR" else "$"
    price   = m.get("price") or 0
    revenue = m.get("revenue") or 0
    rc      = m.get("rev_cagr") or 0
    op_m    = m.get("op_margin") or 0
    fcf_m   = m.get("fcf_margin") or 0
    fcf_abs = m.get("fcf") or 0
    target  = m.get("target_price") or 0
    ab      = j.get("abstauber","—")
    dcf     = j.get("dcf",{})
    konf    = j.get("konfidenz",("🔴","NIEDRIG","#da3633"))
    es      = j.get("exit_strategy",{})
    from datetime import date

    # 12M-Projektionen (Base Case)
    rev_12m = revenue * (1 + rc) if revenue and rc else None
    marge_12m = op_m  # Stable assumption
    fcf_12m   = fcf_abs * (1 + rc) if fcf_abs and rc else None
    kurs_12m  = target if target else (dcf.get("iv") or 0)

    with st.expander("📊 PREDICTION TRACKING & CHECKPOINT (Schritt 7)", expanded=False):
        st.caption("Feedback-Loop: These wird in 6–12 Monaten gemessen. Kein Kaufen ohne messbare Prognose.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📌 12M-Messgrößen (Base Case)**")
            rows = [
                ("Umsatz (12M-Ziel)", f"{sym}{rev_12m/1e9:.2f}B (+{rc:.0%})" if rev_12m else "N/V"),
                ("Op. Marge (12M)", f"{marge_12m:.1%}" if marge_12m else "N/V"),
                ("FCF (12M-Ziel)",   f"{sym}{fcf_12m/1e9:.2f}B" if fcf_12m else "N/V"),
                ("Kursziel (Base)",  f"{sym}{kurs_12m:.2f}" if kurs_12m else "N/V"),
                ("Upside-Erwartung", f"{(kurs_12m/price - 1):+.1%}" if (kurs_12m and price) else "N/V"),
            ]
            st.markdown(_html_table(pd.DataFrame(rows, columns=["Metrik","12M-Ziel"])),
                       unsafe_allow_html=True)
            checkpoint = f"Nächste 2 Earnings (ca. Q+1 & Q+2)"
            st.caption(f"Checkpoint: {checkpoint}")

        with col2:
            if rating == "BEOBACHTEN":
                k_met   = j.get("k_met",0)
                k_basis = j.get("k_basis",5)
                # BEOBACHTEN-PROTOKOLL (Pflicht laut Klasse A #13)
                st.markdown("**🔭 BEOBACHTEN-PROTOKOLL**")
                # Abstauber-Limit aus DCF Bear oder -15% vom Kurs
                stress = j.get("stress_test",{})
                bear_iv = stress.get("scenarios",{}).get("BEAR",{}).get("iv",0) if stress else 0
                abstauber_price = bear_iv if (bear_iv and bear_iv > 0 and bear_iv < price) else (price * 0.85 if price else 0)
                abstauber_str = f"{sym}{abstauber_price:.2f}" if abstauber_price else ab
                st.markdown(
                    f'<div style="background:#3a2f0022;border:1px solid #d29922;border-radius:8px;padding:12px 16px;">'
                    f'<div style="color:#8b949e;font-size:0.75em;letter-spacing:1px;">ABSTAUBER-LIMIT (PFLICHT)</div>'
                    f'<div style="color:#d29922;font-size:1.4em;font-weight:800;">{abstauber_str}</div>'
                    f'<div style="color:#8b949e;font-size:0.75em;">Kein offenes "irgendwann kaufen"</div>'
                    f'</div>', unsafe_allow_html=True)
                st.markdown("")

                # Upgrade-Trigger → KAUFEN (mind. 2 von 3)
                st.markdown("**⬆️ Upgrade-Trigger → KAUFEN (mind. 2/3):**")
                upgrades = [
                    f"Kurs erreicht Abstauber-Limit ({abstauber_str})",
                    f"Nächste Earnings bestätigen K-Kriterien ({k_met}/{k_basis} → vollständig)",
                    "Makro-Sentiment dreht positiv (VIX fällt, Fear & Greed steigt)",
                ]
                for u in upgrades:
                    st.markdown(f"→ {u}")

                # Downgrade-Trigger → SCHROTT (einer reicht)
                st.markdown("**⬇️ Downgrade-Trigger → SCHROTT (einer reicht):**")
                downgrades = es.get("downgrade", [])
                if not downgrades:
                    downgrades = [
                        "K-Kriterium bricht dauerhaft (2Q in Folge)",
                        f"Bewertung steigt >20% über Base Fair Value ({sym}{kurs_12m:.2f}) ohne Fundamental-Verbesserung" if kurs_12m else "Bewertungs-Expansion ohne Fundamentals",
                        "Insider-Nettoverkäufe >20% in 6M",
                    ]
                for d in downgrades[:3]:
                    st.markdown(f"🔴 {d}")

                # Horizont
                st.caption(f"Beobachtungs-Horizont: 2–4 Quartale | Kein BEOBACHTEN ohne dieses Protokoll (Klasse A Regel #13)")

            elif rating == "KAUFEN":
                st.markdown("**✅ KAUFEN – Exit-Strategie aktiv**")
                es_data = [
                    ("Take-Profit 1",   f"+15% über Bull FV → Teilverkauf 25–50%"),
                    ("Take-Profit 2",   f"+30% über Bull FV → Vollverkauf prüfen"),
                    ("Nachkauf-Limit",  ab),
                ]
                for k_s, v in es_data:
                    st.markdown(f"**{k_s}:** {v}")
                stop_triggers = es.get("exit", es.get("downgrade", []))
                if stop_triggers:
                    st.markdown("**🚨 Stop-These-Trigger (einer reicht):**")
                    for t in stop_triggers[:4]:
                        st.markdown(f"🔴 {t}")
            else:
                st.markdown("**🔴 SCHROTT — Kein Investment**")
                st.caption(f"Rating: {rating} · Score: {rs}/10 · Konfidenz: {konf[1]}")
                st.caption("Keine Exit-Strategie nötig — Position vermeiden")

    st.markdown(f'<div style="color:#6e7681;font-size:0.7em;margin:4px 0 12px 0;">'
                f'[ESTIMATE] 12M-Projektion basiert auf historischen Rev-CAGR/Margendaten · '
                f'nicht als Prognose zu verstehen · JACK Schritt 7 Feedback-Loop</div>',
                unsafe_allow_html=True)


# ── ABBRUCH-LOGIK ─────────────────────────────────────────────────────────────
def _calc_abbruch(j: dict, mode: str = "FULL") -> dict:
    """Prüft ob Analyse abgebrochen werden muss."""
    k_met   = j.get("k_met", 0)
    k_basis = j.get("k_basis", 5)
    flags   = j.get("flags", [])
    has_nv  = any(not v.get("avail", True) for v in j.get("K", {}).values())

    abort = False
    reason = ""

    if has_nv:
        abort = True
        reason = "K-Kriterium [N/V] → SOFORT-ABBRUCH (JACK Klasse A Regel)"
    elif mode == "FULL" and k_met <= k_basis - 2:
        abort = True
        reason = f"FULL DEEP DIVE: K={k_met} ≤ BASIS−2={k_basis-2} → ABBRUCH"
    elif mode == "QUICK" and k_met <= k_basis - 3:
        abort = True
        reason = f"QUICK FILTER: K={k_met} ≤ BASIS−3={k_basis-3} → ABBRUCH"

    grenzfall = (not abort) and (k_met == k_basis - 1)

    return {"abort": abort, "reason": reason, "grenzfall": grenzfall,
            "k_met": k_met, "k_basis": k_basis}


# ── AUTO-DETECTION ENGINE PANEL ──────────────────────────────────────────────
def _render_k_basis_engine(j: dict, m: dict):
    """
    Zeigt: erkannter K-BASIS-Modus · Erkennungsgrund · Prioritäten-Logik · aktive K-Kriterien.
    """
    mode        = m.get("_k_basis_mode",   "5S Standard")
    mode_reason = m.get("_k_basis_reason", "Standard-Modus")
    k_basis     = j.get("k_basis", 5)
    k_met       = j.get("k_met",   0)
    color       = _K_MODE_COLORS.get(mode, "#8b949e")

    with st.expander(f"🔬 AUTO-DETECTION ENGINE — K-BASIS: **{mode}**", expanded=True):
        col1, col2 = st.columns([1.3, 1])

        with col1:
            # Mode badge
            st.markdown(
                f'<div style="background:{color}22;border:1px solid {color};border-radius:8px;'
                f'padding:10px 16px;margin:4px 0 12px;">'
                f'<span style="color:{color};font-weight:800;font-size:0.95em;">🎯 {mode}</span><br>'
                f'<span style="color:#c9d1d9;font-size:0.82em;">{mode_reason}</span><br>'
                f'<span style="color:#8b949e;font-size:0.78em;margin-top:4px;display:inline-block;">'
                f'Gatekeeper: {k_met}/{k_basis} K-Kriterien erfüllt</span>'
                f'</div>',
                unsafe_allow_html=True)

            # K-criteria list for active mode
            st.markdown("**Aktive K-Kriterien (Gatekeeper)**")
            for name, v in j.get("K", {}).items():
                s_col  = "#3fb950" if v["pass"] else "#da3633"
                s_icon = "✅" if v["pass"] else "❌"
                n_note = "" if v.get("avail", True) else \
                    ' <span style="color:#6e7681;font-size:0.75em;">[N/V]</span>'
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:6px;padding:3px 0;">'
                    f'<span style="font-size:0.9em;">{s_icon}</span>'
                    f'<span style="color:{s_col};font-size:0.85em;font-weight:500;">{name}</span>'
                    f'<span style="color:#8b949e;font-size:0.8em;">({v["val"]})'
                    f'</span>{n_note}</div>',
                    unsafe_allow_html=True)

            # Transformation flag note
            transf = j.get("transformation", {})
            if transf.get("active"):
                st.markdown(
                    '<div style="background:#388bfd22;border:1px solid #388bfd;border-radius:5px;'
                    'padding:6px 10px;margin-top:8px;">'
                    '<span style="color:#388bfd;font-size:0.82em;">ℹ️ 5T-Override aktiv: '
                    'Transformation-Protokoll hat K-BASIS auf 5T (Transformation) gesetzt.</span>'
                    '</div>', unsafe_allow_html=True)

        with col2:
            # Priority order visual
            st.markdown("**Prioritäten-Reihenfolge**")
            _PRIO = [
                ("5F", "5F Finanz",          "Banking / Insurance"),
                ("5V", "5V Versorger",        "Utilities"),
                ("5I", "5I Infrastruktur",    "Airports / Toll / Rails"),
                ("5K", "5K Sachwerte",        "Mining / Energy / REIT"),
                ("5S", "5SaaS",              "Tech + GM ≥ 65%"),
                ("4P", "4P Piotroski",        "P ≥ 7 + ROIC < 15%"),
                ("5T", "5T Transformation",   "FCF < 20% – Override"),
                ("5D", "5S Standard",         "Default-Fallback"),
            ]
            for _code, _name, _cond in _PRIO:
                _is_act = (mode == _name) or \
                          (_code == "5T" and mode == "5T (Transformation)") or \
                          (_code == "5D" and mode == "5S Standard")
                _mc     = _K_MODE_COLORS.get(_name, _K_MODE_COLORS.get(mode, "#8b949e"))
                _bg     = f"background:{_mc}22;border:1px solid {_mc};" if _is_act else ""
                _tc     = _mc if _is_act else "#8b949e"
                _fw     = "700" if _is_act else "400"
                _arrow  = "▶ " if _is_act else ""
                st.markdown(
                    f'<div style="{_bg}border-radius:4px;padding:3px 8px;margin:2px 0;">'
                    f'<span style="color:{_tc};font-size:0.8em;font-weight:{_fw};">'
                    f'{_arrow}<b>{_code}</b> — {_name.split(" ",1)[-1]}</span>'
                    f'<span style="color:#6e7681;font-size:0.73em;margin-left:6px;">{_cond}</span>'
                    f'</div>',
                    unsafe_allow_html=True)

            st.markdown(
                '<div style="margin-top:10px;color:#8b949e;font-size:0.72em;">'
                '🔁 Evaluation top → bottom · erster Match gewinnt<br>'
                '5T wird NACH dem primären Modus in calc_jack() gesetzt</div>',
                unsafe_allow_html=True)


# ── DATEN-KONFIDENZ PANEL (SCHRITT 2B) ───────────────────────────────────────
def _render_daten_konfidenz(j: dict, m: dict):
    """Schritt 2B — Daten-Konfidenz-Block: zeigt Quellenqualität je Datenpunkt."""
    dk      = j.get("daten_konfidenz", {})
    if not dk:
        return
    quality = dk.get("quality",   "—")
    color   = dk.get("color",     "#8b949e")
    avail   = dk.get("available", 0)
    total   = dk.get("total",     0)
    items   = dk.get("items",     [])
    pct_a   = dk.get("pct",       0)

    with st.expander(
        f"📊 Schritt 2B — DATEN-KONFIDENZ  "
        f"({avail}/{total} · {quality})", expanded=False):

        col1, col2 = st.columns([1.4, 1])

        with col1:
            df_dk = pd.DataFrame(items)[["Datenpunkt", "✓", "Quelle", "Konfidenz"]]
            # Color-code each row
            html_rows = ""
            for _, row in df_dk.iterrows():
                c = {"HOCH": "#3fb950", "MITTEL": "#d29922", "NIEDRIG": "#da3633"}.get(row["Konfidenz"], "#8b949e")
                tag_c = TAG_COLOR.get(row["Quelle"], "#8b949e")
                html_rows += (
                    f'<tr>'
                    f'<td style="color:#c9d1d9;padding:5px 10px;font-size:0.82em;">{row["Datenpunkt"]}</td>'
                    f'<td style="text-align:center;padding:5px 8px;">{row["✓"]}</td>'
                    f'<td style="padding:5px 8px;">'
                    f'<span style="background:{tag_c}22;border:1px solid {tag_c};color:{tag_c};'
                    f'border-radius:3px;padding:1px 5px;font-size:0.72em;font-weight:700;">'
                    f'{row["Quelle"]}</span></td>'
                    f'<td style="color:{c};font-size:0.82em;font-weight:600;padding:5px 8px;">'
                    f'{row["Konfidenz"]}</td>'
                    f'</tr>'
                )
            st.markdown(
                f'<table style="width:100%;border-collapse:collapse;">'
                f'<thead><tr>'
                f'<th style="color:#8b949e;font-size:0.75em;padding:6px 10px;text-align:left;'
                f'border-bottom:1px solid #30363d;">Datenpunkt</th>'
                f'<th style="color:#8b949e;font-size:0.75em;padding:6px 8px;border-bottom:1px solid #30363d;">✓</th>'
                f'<th style="color:#8b949e;font-size:0.75em;padding:6px 8px;border-bottom:1px solid #30363d;">Quelle</th>'
                f'<th style="color:#8b949e;font-size:0.75em;padding:6px 8px;border-bottom:1px solid #30363d;">Konfidenz</th>'
                f'</tr></thead><tbody style="background:#161b22;">{html_rows}</tbody></table>',
                unsafe_allow_html=True)

        with col2:
            # Overall quality badge
            st.markdown(
                f'<div style="background:{color}22;border:1px solid {color};border-radius:10px;'
                f'padding:16px;text-align:center;margin-bottom:12px;">'
                f'<div style="color:#8b949e;font-size:0.72em;letter-spacing:1.5px;margin-bottom:4px;">'
                f'GESAMT-DATENQUALITÄT</div>'
                f'<div style="color:{color};font-weight:800;font-size:1.6em;">{quality}</div>'
                f'<div style="color:#8b949e;font-size:0.82em;margin-top:4px;">'
                f'{avail}/{total} Punkte ({pct_a:.0%})</div>'
                f'</div>',
                unsafe_allow_html=True)

            # Progress bar
            bar_color = color
            st.markdown(
                f'<div style="height:6px;background:#21262d;border-radius:3px;margin-bottom:12px;">'
                f'<div style="width:{pct_a*100:.0f}%;background:{bar_color};height:6px;border-radius:3px;"></div>'
                f'</div>',
                unsafe_allow_html=True)

            # Rules — JACK Daten-Hierarchie
            st.markdown(
                '<div style="background:#161b22;border-radius:6px;padding:10px 14px;">'
                '<span style="color:#8b949e;font-size:0.72em;font-weight:700;letter-spacing:1px;">'
                'JACK DATEN-HIERARCHIE</span><br>'
                '<span style="color:#c9d1d9;font-size:0.78em;line-height:1.8;">'
                '• <b style="color:#3fb950;">S1</b> = SEC-Filings / Investor Relations<br>'
                '• <b style="color:#79c0ff;">S2</b> = Koyfin / TIKR / StockAnalysis<br>'
                '• <b style="color:#e3b341;">S3</b> = marketscreener / Traderfox<br>'
                '• <b style="color:#d29922;">S4</b> = [ESTIMATE] nur E-Krit. &amp; WACC<br>'
                '• <b style="color:#388bfd;">LIVE</b> = Echtzeitkurs (yfinance)<br>'
                '• N/V → Konfidenz-Malus aktiv<br>'
                '• Datenqualität &lt; 65% → ANALYSE STOPPEN'
                '</span></div>',
                unsafe_allow_html=True)

            if pct_a < 0.65:
                st.error("⛔ Datenqualität < 65% — Analyse-Ergebnisse unzuverlässig!")
            elif pct_a < 0.85:
                st.warning("⚠️ Datenlücken vorhanden — Konfidenz max 🟡 MITTEL empfohlen")


# ── PRIORITÄTEN-LOGIK + REAPER ANKER ─────────────────────────────────────────
def _render_prioritaeten_reaper(j: dict, m: dict):
    """
    Zeigt PRIORITÄTEN-LOGIK (① DNA ② VALUATION ③ REST) und
    REAPER SCORE ANKER-SKALA (9-10 / 6-8 / 3-5 / 1-2) als expandierbares Panel.
    """
    rs        = j.get("reaper_score", 1)
    tiefe_d   = j.get("analyse_tiefe_data", {})
    val_reason = tiefe_d.get("val_reason", "Datenlage bestimmt Bewertungsmethode")
    k_icon, k_label, k_color = j.get("konfidenz", ("🔴", "NIEDRIG", "#da3633"))
    red_konfidenz = k_icon == "🔴"

    # Aktiver Valuation-Pfad
    fcf = m.get("fcf") or 0
    fcf_m = m.get("fcf_margin") or 0
    if fcf <= 0:
        val_path = "Negativer FCF → Multiples-Only + Reverse-DCF [B]"
        val_col  = "#da3633"
    elif fcf_m < 0.05:
        val_path = "Lückenhaft / Talsohle → Reverse-DCF Primär [B] + Multiples"
        val_col  = "#d29922"
    else:
        val_path = "[S1] stabil → Full DCF [B] + Reverse-DCF Sanity [C]"
        val_col  = "#3fb950"

    with st.expander("⚡ PRIORITÄTEN-LOGIK & REAPER ANKER-SKALA", expanded=False):
        col_p, col_r = st.columns([1, 1.2])

        with col_p:
            st.markdown("**⚡ PRIORITÄTEN-LOGIK**")
            for i, (step, desc, active) in enumerate([
                ("① DNA-CHECK",       "Immer vollständig — kein Skip",              True),
                ("② VALUATION",       val_path,                                      True),
                ("③ REST (B/C)",      "Best Effort · kein Analyse-Stopper",         True),
            ], 1):
                col_s = val_col if i == 2 else "#388bfd"
                st.markdown(
                    f'<div style="background:{col_s}11;border-left:3px solid {col_s};'
                    f'border-radius:0 5px 5px 0;padding:6px 10px;margin:4px 0;">'
                    f'<span style="color:{col_s};font-weight:700;font-size:0.85em;">{step}</span><br>'
                    f'<span style="color:#c9d1d9;font-size:0.78em;">{desc}</span></div>',
                    unsafe_allow_html=True)

            if red_konfidenz:
                st.markdown(
                    '<div style="background:#da363322;border:1px solid #da3633;border-radius:5px;'
                    'padding:6px 10px;margin-top:8px;">'
                    '<span style="color:#da3633;font-weight:700;font-size:0.82em;">'
                    '🔴 Konfidenz-Deckel aktiv → Score max 6/10</span></div>',
                    unsafe_allow_html=True)

        with col_r:
            st.markdown("**🎯 REAPER ANKER-SKALA**")
            for lo, hi, label, desc, treiber in [
                (9, 10, "AUSNAHME-COMPOUNDER", "#3fb950",
                 "ROIC >30% · Moat 4/4 · Reinvestment-Runway · Bewertung fair · Tier 1"),
                (6,  8, "QUALITÄTS-KERN",      "#79c0ff",
                 "K-BASIS erfüllt · Moat 2–3/4 · Bewertung akzeptabel · kein krit. Risiko"),
                (3,  5, "GRENZFALL/SPEKULATION","#d29922",
                 "K-Lücken ODER Moat schwach ODER überbewertet · min. 1 Stop-These aktiv"),
                (1,  2, "FINGER WEG",           "#da3633",
                 "Mehrere K verfehlt · Moat N/N · Bewertung absurd · Beneish/Mgmt-Risiko"),
            ]:
                active = lo <= rs <= hi
                bg = f"background:{desc}11;" if active else ""
                border = f"border:1px solid {desc};" if active else "border:1px solid #30363d;"
                st.markdown(
                    f'<div style="{bg}{border}border-radius:5px;padding:5px 10px;margin:3px 0;">'
                    f'<span style="color:{desc};font-weight:700;font-size:0.82em;">'
                    f'{"▶ " if active else ""}{lo}–{hi} │ {label}</span><br>'
                    f'<span style="color:#8b949e;font-size:0.73em;">{treiber}</span></div>',
                    unsafe_allow_html=True)

            st.markdown(
                f'<div style="background:#0d1117;border:1px solid #30363d;border-radius:5px;'
                f'padding:5px 10px;margin-top:6px;font-family:monospace;font-size:0.78em;">'
                f'<span style="color:#8b949e;">Aktiver Anker: </span>'
                f'<span style="color:#e6edf3;font-weight:700;">'
                f'{"9–10 AUSNAHME-COMPOUNDER" if rs >= 9 else "6–8 QUALITÄTS-KERN" if rs >= 6 else "3–5 GRENZFALL" if rs >= 3 else "1–2 FINGER WEG"}'
                f'</span>'
                f'<span style="color:#8b949e;"> · Score: </span>'
                f'<span style="color:{k_color};font-weight:700;">{rs}/10'
                f'{" (🔴 Deckel)" if red_konfidenz else ""}</span>'
                f'</div>',
                unsafe_allow_html=True)


# ── GLOBALE REGELN ────────────────────────────────────────────────────────────
def _render_globale_regeln(j: dict, m: dict):
    """Vollständige Globale Regeln — alle JACK-Constraints auf einen Blick."""
    rating    = j.get("rating", "SCHROTT")
    rs        = j.get("reaper_score", 1)
    mode      = m.get("_k_basis_mode", "5S Standard")
    k_icon, k_label, k_color = j.get("konfidenz", ("🔴", "NIEDRIG", "#da3633"))
    flags     = j.get("flags", [])
    k_met     = j.get("k_met", 0)
    k_basis   = j.get("k_basis", 5)

    r_color   = {"KAUFEN": "#3fb950", "BEOBACHTEN": "#d29922", "SCHROTT": "#da3633"}.get(rating, "#8b949e")
    k_cls     = {"KAUFEN": "🟢 Klasse A", "BEOBACHTEN": "🟡 Klasse B", "SCHROTT": "🔴 Klasse C"}.get(rating, "—")

    with st.expander(f"📜 GLOBALE REGELN — {k_cls} | K-BASIS: {mode}", expanded=False):
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**🟢 Drei-Klassen-System**")
            for cls, col, crit in [
                ("KLASSE A – KAUFEN",    "#3fb950", "Alle K ✅ · Score ≥ 7 · Keine roten Flags → Tier 1–2"),
                ("KLASSE B – BEOBACHTEN","#d29922", "1–2 K fehlen · Score 4–6 · Watchlist → Tier 3 (1–2%)"),
                ("KLASSE C – SCHROTT",   "#da3633", "≥3 K fehlen · Score 1–3 · Rote Flags → Tier 4 (0%)"),
            ]:
                is_cur = (cls.split("–")[1].strip() == rating)
                bg = f"background:{col}22;border:1px solid {col};" if is_cur else "border:1px solid #30363d;"
                st.markdown(
                    f'<div style="{bg}border-radius:5px;padding:6px 10px;margin:3px 0;">'
                    f'<span style="color:{col};font-weight:700;font-size:0.85em;">{cls}</span><br>'
                    f'<span style="color:#8b949e;font-size:0.78em;">{crit}</span></div>',
                    unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("**⚖️ Pflicht-Regeln (non-negotiable)**")
            rules = [
                ("KAUFEN ≠ SOFORT KAUFEN",          "Immer auf Abstauber-Preis warten (−15–25% MoS)"),
                ("K-Kriterien sind GATES",           "Alle K müssen erfüllt sein für KAUFEN-Rating"),
                ("Edge darf kein allein. Kaufgrund sein", "Edge-Engine nur ergänzend, nicht primär"),
                ("Konfidenz 🔴 → max BEOBACHTEN",   "Kein KAUFEN bei NIEDRIG-Konfidenz"),
                ("SBC > 15% → Deckel 🟡",           "Management verwässert → Sizing max Tier 3"),
                ("Makro-Radar vor jedem Trade",      "Kein Kauf gegen Trend (NQ100 / DXY / VIX)"),
                ("DCF ≠ Reverse-DCF Divergenz",      "Große Abweichung → min. BEOBACHTEN"),
                ("Keine Emotion, kein FOMO",         "Disziplin: Warten auf Einstiegssignal"),
            ]
            for rule, detail in rules:
                st.markdown(
                    f'<div style="border-left:2px solid #30363d;padding:3px 8px;margin:3px 0;">'
                    f'<span style="color:#e6edf3;font-size:0.82em;font-weight:600;">🔒 {rule}</span><br>'
                    f'<span style="color:#8b949e;font-size:0.76em;">{detail}</span></div>',
                    unsafe_allow_html=True)

        with c2:
            st.markdown("**🎯 K-BASIS Sonderregeln**")
            mode_rules = {
                "5S Standard":        ["ROIC > 20% Pflicht", "FCF-Marge ≥ 20% Pflicht",
                                        "Piotroski ≥ 7/9 Gate", "EPS-CAGR ≥ 12%", "SBC < 10%"],
                "5F Finanz":          ["ROE > 12% (kein ROIC)", "FCF-Marge ≥ 15% (niedrigere Hürde)",
                                        "Piotroski ≥ 7/9", "EPS-CAGR ≥ 10%", "Kein Capex-Check"],
                "5SaaS":              ["Bruttomarge ≥ 65% Gate", "Rev-CAGR ≥ 15%",
                                        "ROIC > 15% (niedrigere Hürde)", "SBC < 15% (höhere Toleranz)",
                                        "NRR / ARR dominant wenn verfügbar"],
                "5I Infrastruktur":   ["Op. Marge ≥ 40% (EBITDA-Proxy)", "ND/EBITDA < 6x (höhere Toleranz)",
                                        "FCF > 0 Gate", "Capex ≤ 30%", "Piotroski ≥ 5"],
                "5V Versorger":       ["ROE ≥ 10%", "Div.-Rendite ≥ 4% Gate",
                                        "Payout ≤ 80%", "ND/EBITDA < 5x", "Op. Marge ≥ 30%"],
                "5K Sachwerte":       ["EV/EBITDA ≤ 8x Gate", "ND/EBITDA < 3x",
                                        "FCF-Marge ≥ 5%", "ROA > 5%", "Piotroski ≥ 5"],
                "4P Piotroski":       ["Piotroski ≥ 7 = primäres Gate (hard)", "ROIC ≥ 10%",
                                        "FCF > 0", "ND/EBITDA < 4x", "NUR 4 K-Kriterien"],
                "5T (Transformation)":["FCF-Marge temporär als E-Kriterium",
                                        "ROIC-Trend wichtiger als Niveau", "Piotroski ≥ 4",
                                        "Umsatz ≥ 0%", "Management-Glaubwürdigkeit entscheidend"],
            }
            active_rules = mode_rules.get(mode, mode_rules["5S Standard"])
            mc = _K_MODE_COLORS.get(mode, "#8b949e")
            st.markdown(
                f'<div style="background:{mc}22;border:1px solid {mc};border-radius:8px;'
                f'padding:10px 14px;margin-bottom:10px;">'
                f'<span style="color:{mc};font-weight:700;font-size:0.9em;">{mode}</span><br>'
                + "".join(f'<span style="color:#c9d1d9;font-size:0.8em;">• {r}</span><br>'
                          for r in active_rules)
                + '</div>', unsafe_allow_html=True)

            # Active flags
            if flags:
                st.markdown("**⚑ Aktive Flags**")
                for f in flags:
                    st.markdown(
                        f'<div style="background:{f["color"]}22;border-left:3px solid {f["color"]};'
                        f'padding:3px 8px;margin:2px 0;border-radius:0 4px 4px 0;">'
                        f'<b style="color:{f["color"]};font-size:0.85em;">{f["name"]}</b>'
                        f' <span style="color:#8b949e;font-size:0.78em;">— {f["reason"]}</span></div>',
                        unsafe_allow_html=True)
            else:
                st.markdown('<span style="color:#3fb950;font-size:0.85em;">✅ Keine roten Flags aktiv</span>',
                            unsafe_allow_html=True)

            st.markdown("---")
            st.caption(
                f"Aktuell: **{rating}** · Score: {rs}/10 · K: {k_met}/{k_basis} · "
                f"Konfidenz: {k_icon} {k_label}")

        # ── KLASSE A / B / C Regelwerk (vollständig nach JACK-Spec) ──────────
        st.markdown("---")
        ca, cb, cc = st.columns(3)

        # ── Alle 30 KLASSE A Regeln (vollständig nach JACK-Spec) ─────────────
        # Format: (nr, name, detail, status) — status: ✅ impl / ⚠️ partial / 🚧 display-only
        _rules_a = [
            ( 1, "TAG-PFLICHT",           "S1/S2/S3/S4/LIVE/N/V bei jeder Kennzahl",                    "✅"),
            ( 2, "LIVE-INTEGRITÄT",       "Nur mit Web-Search + URL — Fake-LIVE = Regelverstoß",         "✅"),
            ( 3, "VERIFIED-SCHWELLE",     "≥2 Quellen · ≤10% · 10–20% = DISKREPANZ · >20% = N/V",       "✅"),
            ( 4, "SCHÄTZ-DOKTRIN",        "K: ESTIMATE verboten · E: erlaubt mit −20% Malus + 🟡",       "⚠️"),
            ( 5, "ABBRUCH-LOGIK",         "Einzige Quelle = DNA-CHECK Abbruch-Block",                    "✅"),
            ( 6, "K-BASIS-PFLICHT",       "Vor DNA-Check festlegen + im Header ausweisen",               "✅"),
            ( 7, "KONFIDENZ-PFLICHT",     "🟢/🟡/🔴 Pflicht-Output jeder Analyse",                       "✅"),
            ( 8, "🔴-REGELUNG",           "Tier 1/2 verboten · Score max 6 · EDGE-Deckel aktiv",         "✅"),
            ( 9, "WACC-PFLICHT",          "Dynamisch + WACC-BREAKDOWN Pflicht-Output",                   "✅"),
            (10, "PRIORITÄTEN-LOGIK",     "① DNA ② Valuation (Datenlage) ③ Rest Best Effort",           "✅"),
            (11, "REVERSE-DCF-ROLLE",     "Primär bei lückenhaft/Talsohle/neg.FCF · Sanity bei stabil",  "✅"),
            (12, "EXIT-PFLICHT",          "Kein KAUFEN ohne Exit-Strategie",                             "✅"),
            (13, "BEOBACHTEN-PFLICHT",    "Kein BEOBACHTEN ohne Abstauber-Limit + Trigger",              "✅"),
            (14, "BATTLE-VALUATION",      "Standard = QUICK CHECK · DCF-Kurz wenn beide S1",             "✅"),
            (15, "BATTLE-BASIS-WARNUNG",  "Unterschiedl. K-BASIS → Normalisierung als % Pflicht",        "⚠️"),
            (16, "FX-PFLICHT",            "Nicht-EUR → EUR-FV + FX-Impact ausweisen",                    "✅"),
            (17, "PREISE",                "Immer live abrufen — kein Trainingspreis als Basis",           "✅"),
            (18, "DATENALTER",            ">1 Quartal → ⚠️ VERALTET-Warnung aktiv",                      "✅"),
            (19, "THESE-DISZIPLIN",       "Kurs fällt ≠ These kaputt — strukturell prüfen",              "✅"),
            (20, "RECHEN-DOKTRIN",        "Python: Variablen → Zwischenschritte → Ergebnis",             "✅"),
            (21, "REAPER SCORE",          "Qualitätsurteil + Anker + 1-Satz-Treiber · Max 6 bei 🔴",     "✅"),
            (22, "BATTLE-VORFILTER",      "K-Check inkl. K-BASIS vor Battle-Vergleich",                  "✅"),
            (23, "KURSPFLICHT C/D",       "Live abrufen — Fehlschlag → max ⚠️ WACKELT",                  "✅"),
            (24, "TIEFE-PFLICHT",         "Jede Analyse mit Tiefe-Auswahl starten",                      "✅"),
            (25, "TV-WARNUNG",            "Terminal Value > 70% EV → Pflicht-Hinweis",                   "✅"),
            (26, "BENEISH-INTEGRITÄT",    "Nur [LIVE] · Sonst SKIP · Kein Abzug",                        "✅"),
            (27, "DCF g-BASIS-PFLICHT",   "g = FCF-CAGR(5J) × 0.8 · Fallback: Rev-CAGR",               "⚠️"),
            (28, "SAAS-OVERRIDE",         "NRR als K-Kriterium bei ARR-Modellen · N/V = Abbruch",        "⚠️"),
            (29, "DEBT-MATURITY-PFLICHT", "Schritt 4 immer vollständig · 🔴 → −10% FV-Malus",           "✅"),
            (30, "TRANSFORMATION",        "FCF-Override nur nach 3-Punkte-Qualifikation · max Tier 3",   "✅"),
        ]

        # Split into two columns for compact display
        half = len(_rules_a) // 2 + len(_rules_a) % 2
        left_rules  = _rules_a[:half]
        right_rules = _rules_a[half:]

        with ca:
            st.markdown(
                '<div style="background:#3fb95022;border:1px solid #3fb950;border-radius:6px;'
                'padding:8px 12px;margin-bottom:8px;">'
                '<span style="color:#3fb950;font-weight:700;font-size:0.85em;">'
                '🔒 KLASSE A — EISERN (nie brechen)</span><br>'
                '<span style="color:#8b949e;font-size:0.72em;">✅ implementiert · ⚠️ partial · 🚧 nur Anzeige</span>'
                '</div>',
                unsafe_allow_html=True)
            rows = ""
            for nr, name, detail, status in left_rules:
                sc = "#3fb950" if status == "✅" else "#d29922" if status == "⚠️" else "#8b949e"
                rows += (
                    f'<tr>'
                    f'<td style="color:#8b949e;font-size:0.7em;padding:3px 4px;text-align:right;">{nr}</td>'
                    f'<td style="padding:3px 6px;">'
                    f'<span style="color:{sc};font-size:0.7em;font-weight:700;">{status}</span></td>'
                    f'<td style="color:#e6edf3;font-size:0.73em;font-weight:600;padding:3px 4px;">{name}</td>'
                    f'<td style="color:#8b949e;font-size:0.7em;padding:3px 4px;">{detail}</td>'
                    f'</tr>'
                )
            st.markdown(
                f'<table style="width:100%;border-collapse:collapse;">'
                f'<tbody>{rows}</tbody></table>',
                unsafe_allow_html=True)

        with cb:
            st.markdown(
                '<div style="background:#3fb95022;border:1px solid #3fb950;border-radius:6px;'
                'padding:8px 12px;margin-bottom:8px;">'
                '<span style="color:#3fb950;font-weight:700;font-size:0.85em;">'
                '🔒 KLASSE A — Fortsetzung (16–30)</span>'
                '</div>',
                unsafe_allow_html=True)
            rows = ""
            for nr, name, detail, status in right_rules:
                sc = "#3fb950" if status == "✅" else "#d29922" if status == "⚠️" else "#8b949e"
                rows += (
                    f'<tr>'
                    f'<td style="color:#8b949e;font-size:0.7em;padding:3px 4px;text-align:right;">{nr}</td>'
                    f'<td style="padding:3px 6px;">'
                    f'<span style="color:{sc};font-size:0.7em;font-weight:700;">{status}</span></td>'
                    f'<td style="color:#e6edf3;font-size:0.73em;font-weight:600;padding:3px 4px;">{name}</td>'
                    f'<td style="color:#8b949e;font-size:0.7em;padding:3px 4px;">{detail}</td>'
                    f'</tr>'
                )
            st.markdown(
                f'<table style="width:100%;border-collapse:collapse;">'
                f'<tbody>{rows}</tbody></table>',
                unsafe_allow_html=True)

        with cc:
            st.markdown(
                '<div style="background:#d2992222;border:1px solid #d29922;border-radius:6px;'
                'padding:8px 12px;margin-bottom:6px;">'
                '<span style="color:#d29922;font-weight:700;font-size:0.85em;">'
                '⚙️ KLASSE B — KONTEXTABHÄNGIG</span></div>',
                unsafe_allow_html=True)
            for rule in [
                "Beneish: nur wenn alle 8 [S1/LIVE] → sonst SKIP",
                "Zyklus-Overlay: nur bei zyklischen Sektoren",
                "Piotroski-Override: Finanzsektor / Deep Value",
                "Python DCF: FULL DEEP DIVE + stabile Datenlage",
                "Reverse-DCF primär: lückenhaft / Talsohle / neg. FCF",
                "Moat-Verifikation Vollformat: nur FULL DEEP DIVE",
                "Management-Score Vollformat: nur FULL DEEP DIVE",
            ]:
                st.markdown(
                    f'<div style="border-left:2px solid #d29922;padding:2px 7px;margin:2px 0;">'
                    f'<span style="color:#c9d1d9;font-size:0.75em;">• {rule}</span></div>',
                    unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(
                '<div style="background:#8b949e22;border:1px solid #8b949e;border-radius:6px;'
                'padding:8px 12px;margin:6px 0;">'
                '<span style="color:#8b949e;font-weight:700;font-size:0.85em;">'
                '📋 KLASSE C — BEST EFFORT</span></div>',
                unsafe_allow_html=True)
            for rule in [
                "Analyst-Konsens-Check",
                "Insider-Käufe/-Verkäufe (6M)",
                "Technical Alignment",
                "Reverse-DCF Sanity Check (zusätzl. bei stabilem DCF)",
            ]:
                st.markdown(
                    f'<div style="border-left:2px solid #8b949e;padding:2px 7px;margin:2px 0;">'
                    f'<span style="color:#8b949e;font-size:0.75em;">• {rule}</span></div>',
                    unsafe_allow_html=True)


# ── FLAG-CHECK PANEL ──────────────────────────────────────────────────────────
def _render_flag_check(j: dict, m: dict):
    """Vollständiger FLAG-CHECK mit allen aktiven Flags und Konfidenz-Deckeln."""
    flags      = j.get("flags", [])
    konfidenz  = j.get("konfidenz", ("🔴", "NIEDRIG", "#da3633"))
    transf     = j.get("transformation", {})
    abbruch    = j.get("abbruch", {})
    debt_mat   = j.get("debt_maturity", {})
    capex_ch   = j.get("capex_check", {})
    k_icon, k_label, k_color = konfidenz

    with st.expander("⚑ FLAG-CHECK & KONFIDENZ-DECKEL", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Aktive Flags**")
            if not flags and not transf.get("active") and debt_mat.get("status") != "KRITISCH":
                st.markdown('<span style="color:#3fb950;">✅ Keine kritischen Flags aktiv</span>',
                            unsafe_allow_html=True)
            for f in flags:
                st.markdown(
                    f'<div style="background:{f["color"]}22;border-left:3px solid {f["color"]};'
                    f'padding:4px 8px;margin:3px 0;border-radius:0 4px 4px 0;">'
                    f'<b style="color:{f["color"]};">{f["name"]}</b><br>'
                    f'<span style="font-size:0.8em;color:#c9d1d9;">{f["reason"]}</span></div>',
                    unsafe_allow_html=True)
            if transf.get("active"):
                st.markdown(
                    '<div style="background:#388bfd22;border-left:3px solid #388bfd;'
                    'padding:4px 8px;margin:3px 0;border-radius:0 4px 4px 0;">'
                    '<b style="color:#388bfd;">TRANSFORMATION-FLAG</b><br>'
                    '<span style="font-size:0.8em;color:#c9d1d9;">FCF < 20% – K-BASIS auf 5T angepasst</span></div>',
                    unsafe_allow_html=True)
            if debt_mat.get("status") == "KRITISCH":
                for r in debt_mat.get("red", []):
                    st.markdown(
                        f'<div style="background:#da363322;border-left:3px solid #da3633;'
                        f'padding:4px 8px;margin:3px 0;border-radius:0 4px 4px 0;">'
                        f'<b style="color:#da3633;">DEBT-MATURITY KRITISCH</b><br>'
                        f'<span style="font-size:0.8em;color:#c9d1d9;">{r}</span></div>',
                        unsafe_allow_html=True)
            if capex_ch.get("triggered") and capex_ch.get("intensity") == "KRITISCH":
                st.markdown(
                    f'<div style="background:#da363322;border-left:3px solid #da3633;'
                    f'padding:4px 8px;margin:3px 0;border-radius:0 4px 4px 0;">'
                    f'<b style="color:#da3633;">CAPEX-KRITISCH</b><br>'
                    f'<span style="font-size:0.8em;color:#c9d1d9;">{capex_ch.get("note","")}</span></div>',
                    unsafe_allow_html=True)

        with col2:
            st.markdown("**KONFIDENZ-DECKEL Hierarchie**")
            # SBC-INFECTION-CHECK (Pflicht jede Analyse)
            sbc_intensity = m.get("sbc_intensity") or 0
            sbc_infection = sbc_intensity > 0.15
            sbc_warn      = sbc_intensity > 0.10

            deckel_items = [
                (k_icon, f"Gesamt-Konfidenz: {k_label}", k_color),
                ("🔴" if abbruch.get("abort") else "🟢", "Abbruch-Logik: " + ("AKTIV" if abbruch.get("abort") else "OK"), "#da3633" if abbruch.get("abort") else "#3fb950"),
                (debt_mat.get("icon","🟢"), f"Debt Maturity: {debt_mat.get('status','—')}", debt_mat.get("color","#3fb950")),
                ("🟢" if not transf.get("active") else "🔵", f"Transformation: {'AKTIV (5T)' if transf.get('active') else 'Inaktiv'}", "#388bfd" if transf.get("active") else "#3fb950"),
                ("☢️" if sbc_infection else ("⚠️" if sbc_warn else "🟢"),
                 f"SBC-Infection: {'AKTIV ☢️ —20% Malus' if sbc_infection else ('WARNUNG ⚠️' if sbc_warn else 'OK')} ({pct(sbc_intensity)})",
                 "#da3633" if sbc_infection else ("#d29922" if sbc_warn else "#3fb950")),
            ]
            for icon, label, col in deckel_items:
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;margin:4px 0;">'
                    f'<span style="font-size:1.1em;">{icon}</span>'
                    f'<span style="color:{col};font-size:0.85em;">{label}</span></div>',
                    unsafe_allow_html=True)

            if sbc_infection:
                st.markdown(
                    '<div style="background:#da363322;border:1px solid #da3633;border-radius:6px;'
                    'padding:8px 12px;margin:6px 0;">'
                    '<b style="color:#da3633;">☢️ SBC-INFECTION AKTIV</b><br>'
                    '<span style="color:#c9d1d9;font-size:0.82em;">'
                    'SBC > 15% Umsatz → Aktionärs-Verwässerung exzessiv.<br>'
                    '→ Konfidenz-Deckel: max 🟡 MITTEL<br>'
                    '→ Reaper Score: −2 Malus<br>'
                    '→ Sizing: max Tier 3 (1–2%)<br>'
                    '"Management bedient sich zuerst."</span></div>',
                    unsafe_allow_html=True)

            if abbruch.get("abort"):
                st.error(f"⛔ ANALYSE ABGEBROCHEN: {abbruch['reason']}")
            elif abbruch.get("grenzfall"):
                st.warning(f"⚠️ GRENZFALL: K={abbruch['k_met']}/{abbruch['k_basis']} — Begründungspflicht aktiv")

            st.markdown("---")
            st.caption("Regel: Niedrigster aktiver Deckel gewinnt · 🔴 < 🟡 < 🟢")


# ── TRANSFORMATION PANEL ──────────────────────────────────────────────────────
def _render_transformation(m: dict, j: dict):
    """Zeigt TRANSFORMATION-PROTOKOLL wenn aktiv oder grenzwertig."""
    t = j.get("transformation", {})
    if m.get("fcf_margin", 1) >= 0.20:
        return  # Nicht nötig

    with st.expander("🔄 TRANSFORMATION-PROTOKOLL", expanded=t.get("active", False)):
        col1, col2, col3 = st.columns(3)
        checks = [
            (t.get("q1_fcf_path"), "① FCF-Pfad-Nachweis", "Bruttomarge ≥ 50% + Op. Leverage vorhanden", col1),
            (t.get("q2_horizon"),  "② Zeithorizont",       f"Net Debt/EBITDA < 3x (aktuell: {xfmt(t.get('nd'))})", col2),
            (t.get("q3_balance"),  "③ Bilanz-Schutz",      f"Current Ratio ≥ 1x (aktuell: {nfmt(t.get('cr'))})", col3),
        ]
        for ok, title, desc, col in checks:
            icon  = "✅" if ok else "❌"
            color = "#3fb950" if ok else "#da3633"
            col.markdown(f'<div style="text-align:center;">'
                         f'<div style="font-size:1.5em;">{icon}</div>'
                         f'<div style="color:{color};font-weight:700;font-size:0.85em;">{title}</div>'
                         f'<div style="color:#8b949e;font-size:0.75em;">{desc}</div></div>',
                         unsafe_allow_html=True)

        if t.get("active"):
            st.success("✅ TRANSFORMATION qualifiziert · K-BASIS: **5T** · FCF-Marge temporär als E-Kriterium")
        else:
            st.error(f"❌ TRANSFORMATION nicht qualifiziert → K-BASIS: Standard\n\n" +
                     "\n".join(f"• {r}" for r in t.get("reasons_fail", [])))


# ── MOAT-VERIFIKATION PANEL ───────────────────────────────────────────────────
def _render_moat(j: dict):
    """Rendert Moat-Verifikations-Panel."""
    moat = j.get("moat", {})
    if not moat:
        return

    st.markdown(f"### 🏰 Moat-Verifikation &nbsp; "
                f'<span style="color:{moat["color"]};font-weight:700;">{moat["label"]}</span> '
                f'<span style="color:#8b949e;font-size:0.85em;">({moat["score"]}/{moat["max"]})</span>',
                unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (crit, v) in enumerate(moat["details"].items()):
        icon  = "✅" if v["pass"] else "❌"
        color = "#3fb950" if v["pass"] else "#da3633"
        cols[i].markdown(
            f'<div class="mtile"><div class="mlabel">{icon} {crit}</div>'
            f'<div class="mvalue" style="color:{color};">{v["val"]}</div>'
            f'<div style="color:#8b949e;font-size:0.68em;">{v["note"]}</div></div>',
            unsafe_allow_html=True)

    # REINVESTMENT MOAT + BASE RATE CHECK
    st.markdown("")
    moat_score = moat.get("score",0)
    reinvest = "✅ Ja" if moat_score >= 3 else ("⚠️ Begrenzt" if moat_score == 2 else "❌ Nein")
    # BASE RATE CHECK — historische Erfolgsrate
    moat_label_str = moat.get("label","")
    if moat_score >= 4:
        case_type, case_rate, case_reason = "Asset-Light Compounder", "Hoch", "ROIC-Reinvestment-Kombination historisch superior"
    elif moat_score >= 3:
        case_type, case_rate, case_reason = "Quality Growth", "Gemischt", "Abhängig von Reinvestment-Runway und Makro-Zyklus"
    elif moat_score >= 2:
        case_type, case_rate, case_reason = "Turnaround / Moderate Moat", "Selten erfolgreich", "Statistisch ~30% Hit Rate; Timing-Abhängigkeit hoch"
    else:
        case_type, case_rate, case_reason = "Commodity / kein Moat", "Selten erfolgreich", "Strukturell schwaches Geschäftsmodell – Base Rate <20%"
    rate_col = "#3fb950" if case_rate == "Hoch" else "#d29922" if case_rate == "Gemischt" else "#da3633"
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(
            f'<div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:8px 12px;">'
            f'<span style="color:#8b949e;font-size:0.75em;">REINVESTMENT MOAT</span><br>'
            f'<span style="color:#e6edf3;font-weight:700;">Kapital zu >20% ROIC reinvestierbar?</span>'
            f'<span style="color:{"#3fb950" if reinvest.startswith("✅") else "#d29922" if "Begrenzt" in reinvest else "#da3633"};font-size:1.1em;margin-left:8px;">{reinvest}</span>'
            f'</div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown(
            f'<div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:8px 12px;">'
            f'<span style="color:#8b949e;font-size:0.75em;">📊 BASE RATE CHECK (Case-Statistik)</span><br>'
            f'<span style="color:#8b949e;font-size:0.8em;">Case-Typ: </span><b style="color:#e6edf3;font-size:0.9em;">{case_type}</b><br>'
            f'<span style="color:#8b949e;font-size:0.8em;">Hist. Erfolgsrate: </span>'
            f'<span style="color:{rate_col};font-weight:700;">{case_rate}</span><br>'
            f'<span style="color:#6e7681;font-size:0.75em;">{case_reason}</span>'
            f'</div>', unsafe_allow_html=True)
    st.markdown("")


# ── MANAGEMENT-SCORE PANEL ────────────────────────────────────────────────────
def _render_management(j: dict):
    """Rendert Management-Score Panel (FULL DEEP DIVE)."""
    mgmt = j.get("management", {})
    if not mgmt:
        return

    st.markdown(f"### 👤 Management-Score &nbsp; "
                f'<span style="color:{mgmt["color"]};font-weight:700;">{mgmt["label"]}</span> '
                f'<span style="color:#8b949e;font-size:0.85em;">({mgmt["score"]}/{mgmt["max"]})</span>',
                unsafe_allow_html=True)

    cols = st.columns(len(mgmt["details"]))
    for i, (crit, v) in enumerate(mgmt["details"].items()):
        icon  = "✅" if v["pass"] else "❌"
        color = "#3fb950" if v["pass"] else "#da3633"
        cols[i].markdown(
            f'<div class="mtile"><div class="mlabel">{icon} {crit}</div>'
            f'<div class="mvalue" style="color:{color};">{v["val"]}</div>'
            f'<div style="color:#8b949e;font-size:0.68em;">{v["note"]}</div></div>',
            unsafe_allow_html=True)


# ── QUICK FILTER: MOAT STICHPUNKTE ──────────────────────────────────────────
def _render_moat_quick(j: dict):
    """QUICK FILTER: Moat als 2–3 Stichpunkte (kein 4-Panel)."""
    moat = j.get("moat", {})
    if not moat:
        return
    score = moat.get("score", 0)
    label = moat.get("label", "—")
    color = moat.get("color", "#8b949e")
    details = moat.get("details", {})

    st.markdown(
        f'<div style="background:#161b22;border:1px solid #30363d;border-radius:8px;'
        f'padding:10px 16px;margin:6px 0;">'
        f'<span style="color:#8b949e;font-size:0.75em;letter-spacing:1px;">🏰 MOAT</span> &nbsp;'
        f'<span style="color:{color};font-weight:700;">{label}</span>'
        f'<span style="color:#8b949e;font-size:0.8em;"> ({score}/4)</span>'
        + "".join(
            f'<span style="margin-left:10px;color:{"#3fb950" if v["pass"] else "#da3633"};'
            f'font-size:0.82em;">{"✅" if v["pass"] else "❌"} {crit}: {v["val"]}</span>'
            for crit, v in list(details.items())[:3]
        )
        + '</div>',
        unsafe_allow_html=True)


# ── QUICK FILTER: MANAGEMENT STICHPUNKTE ─────────────────────────────────────
def _render_management_quick(j: dict):
    """QUICK FILTER: Management-Score als kompakte Zeile."""
    mgmt = j.get("management", {})
    if not mgmt:
        return
    score = mgmt.get("score", 0)
    label = mgmt.get("label", "—")
    color = mgmt.get("color", "#8b949e")
    details = mgmt.get("details", {})

    bullets = []
    for crit, v in details.items():
        if v.get("pass"):
            bullets.append(f'✅ {crit}')
    failed  = [crit for crit, v in details.items() if not v.get("pass")]

    st.markdown(
        f'<div style="background:#161b22;border:1px solid #30363d;border-radius:8px;'
        f'padding:10px 16px;margin:6px 0;">'
        f'<span style="color:#8b949e;font-size:0.75em;letter-spacing:1px;">👤 MANAGEMENT</span> &nbsp;'
        f'<span style="color:{color};font-weight:700;">{score}/5 — {label}</span><br>'
        f'<span style="color:#3fb950;font-size:0.82em;">{" · ".join(bullets) if bullets else "—"}</span>'
        + (f'<br><span style="color:#da3633;font-size:0.78em;">Fehlt: {", ".join(failed)}</span>'
           if failed else "")
        + '</div>',
        unsafe_allow_html=True)


# ── QUICK FILTER: VALUATION SCHNELLCHECK ────────────────────────────────────
def _render_quick_valuation(j: dict, m: dict):
    """
    QUICK FILTER Valuation:
    KGV / PEG / EV-FCF Schnellcheck + Reverse-DCF Primär.
    Kein Python-DCF.
    """
    tiefe_d  = j.get("analyse_tiefe_data", {})
    val_mode = tiefe_d.get("val_mode", "FULL DCF")
    val_reason = tiefe_d.get("val_reason", "")
    rdcf     = j.get("reverse_dcf", {})
    konv     = j.get("konvergenz", {})
    stress_d = j.get("stress_test", {})
    sym      = "€" if m.get("currency") == "EUR" else "$"
    price    = m.get("price") or 0
    pe       = m.get("pe") or 0
    fwd_pe   = m.get("fwd_pe") or 0
    ev_fcf   = m.get("ev_fcf") or 0
    ev_ebitda = m.get("ev_ebitda") or 0
    kgv_s    = m.get("price_to_sales") or 0
    rev_cagr = m.get("rev_cagr") or 0
    eps_cagr = m.get("eps_cagr") or 0
    target   = m.get("target_price") or 0
    sector   = m.get("sector", "")
    bm       = _sector_benchmarks(sector)

    st.markdown("### 5️⃣ Valuation (QUICK FILTER)")

    # Val-Mode Banner
    vm_col = "#388bfd" if val_mode == "FULL DCF" else "#d29922" if "REVERSE" in val_mode else "#da3633"
    st.markdown(
        f'<div style="background:{vm_col}22;border:1px solid {vm_col};border-radius:6px;'
        f'padding:6px 14px;margin-bottom:10px;font-size:0.85em;">'
        f'<span style="color:{vm_col};font-weight:700;">VALUATION-MODUS: {val_mode}</span>'
        f' — <span style="color:#8b949e;">{val_reason}</span></div>',
        unsafe_allow_html=True)

    # KONVERGENZ
    if konv:
        sigs = konv.get("signals", [])
        sig_html = " &nbsp;·&nbsp; ".join(
            f'<span style="color:{c};">{n}: {v}</span>' for n, v, c in sigs)
        st.markdown(
            f'<div style="background:#161b22;border:1px solid #30363d;border-radius:8px;'
            f'padding:8px 14px;margin-bottom:10px;">'
            f'<span style="color:#8b949e;font-size:0.8em;">KONVERGENZ: </span>'
            f'<span style="color:{konv.get("color","#8b949e")};font-weight:700;">{konv.get("label","—")}</span>'
            f'<span style="font-size:0.8em;margin-left:14px;">{sig_html}</span></div>',
            unsafe_allow_html=True)

    # KGV-SPRUNG-CHECK
    if pe > 0 and fwd_pe > 0:
        kgv_delta = abs(fwd_pe - pe) / pe
        if kgv_delta > 0.50:
            kgv_dir = "gesunken" if fwd_pe < pe else "gestiegen"
            st.warning(f"⚠️ KGV-SPRUNG: {pe:.0f}x → {fwd_pe:.0f}x ({kgv_delta:.0%} {kgv_dir}) — Einmaleffekt / EPS-Einbruch prüfen!")

    # KGV / PEG / EV-FCF Schnellcheck
    col1, col2, col3 = st.columns(3)

    # KGV (fwd)
    kgv_bench  = bm.get("kgv", (15, 25))
    kgv_delta_bm = ((fwd_pe - kgv_bench[0]) / kgv_bench[0] * 100) if fwd_pe > 0 else None
    kgv_col    = "#3fb950" if fwd_pe > 0 and fwd_pe < kgv_bench[0] else (
                 "#d29922" if fwd_pe > 0 and fwd_pe <= kgv_bench[1] else "#da3633")
    with col1:
        st.markdown(
            f'<div class="mtile">'
            f'<div class="mlabel">KGV (fwd)</div>'
            f'<div class="mvalue" style="color:{kgv_col};">{fwd_pe:.0f}x</div>'
            f'<div style="color:#8b949e;font-size:0.72em;">Sektor: {kgv_bench[0]}–{kgv_bench[1]}x</div>'
            f'<div style="color:{kgv_col};font-size:0.78em;">'
            f'{"✅ günstig" if kgv_col=="#3fb950" else "⚖️ fair" if kgv_col=="#d29922" else "❌ teuer"}</div>'
            f'</div>' if fwd_pe > 0 else
            f'<div class="mtile"><div class="mlabel">KGV (fwd)</div>'
            f'<div class="mvalue" style="color:#8b949e;">N/V</div></div>',
            unsafe_allow_html=True)

    # PEG
    peg = (fwd_pe / (eps_cagr * 100)) if (fwd_pe > 0 and eps_cagr and eps_cagr > 0) else None
    peg_col = "#3fb950" if peg and peg < 1.5 else ("#d29922" if peg and peg < 2.5 else "#da3633")
    peg_lbl = "✅ fair" if peg and peg < 1.5 else ("⚠️ ambitioniert" if peg and peg < 2.5 else "❌ >2.5 teuer")
    with col2:
        st.markdown(
            f'<div class="mtile">'
            f'<div class="mlabel">PEG</div>'
            f'<div class="mvalue" style="color:{peg_col if peg else "#8b949e"};">'
            f'{"N/V" if not peg else f"{peg:.2f}"}</div>'
            f'<div style="color:#8b949e;font-size:0.72em;"><1.5 fair · 1.5-2.5 ambitioniert</div>'
            f'<div style="color:{peg_col};font-size:0.78em;">{peg_lbl if peg else "—"}</div>'
            f'</div>',
            unsafe_allow_html=True)

    # EV/FCF
    evfcf_col = "#3fb950" if 0 < ev_fcf < 25 else ("#d29922" if 0 < ev_fcf < 35 else "#da3633")
    with col3:
        st.markdown(
            f'<div class="mtile">'
            f'<div class="mlabel">EV/FCF</div>'
            f'<div class="mvalue" style="color:{evfcf_col if ev_fcf > 0 else "#8b949e"};">'
            f'{"N/V" if ev_fcf <= 0 else f"{ev_fcf:.0f}x"}</div>'
            f'<div style="color:#8b949e;font-size:0.72em;"><25x günstig · >35x teuer</div>'
            f'<div style="color:{evfcf_col};font-size:0.78em;">'
            f'{"✅ günstig" if evfcf_col=="#3fb950" else "⚖️ fair" if evfcf_col=="#d29922" else ("❌ teuer" if ev_fcf > 0 else "—")}</div>'
            f'</div>',
            unsafe_allow_html=True)

    st.markdown("")

    # Analyst-Ziel
    if target > 0 and price > 0:
        up = target / price - 1
        up_col = "#3fb950" if up > 0.10 else "#d29922" if up > -0.05 else "#da3633"
        st.markdown(
            f'<div style="background:#161b22;border:1px solid #30363d;border-radius:6px;'
            f'padding:8px 14px;font-size:0.88em;">'
            f'Analysten-Konsens: <b style="color:{up_col};">{sym}{target:.2f} ({up:+.1%})</b>'
            f' — {m.get("analyst_count",0):.0f} Analysten · Empfehlung: {(m.get("recommendation") or "—").upper()}'
            f'</div>', unsafe_allow_html=True)

    st.markdown("")

    # Reverse-DCF (bei QUICK FILTER immer als Primär)
    if rdcf.get("available"):
        st.markdown("**🔄 Reverse-DCF (Primär bei QUICK FILTER)**")
        r = rdcf
        r_col = r.get("color","#8b949e")
        c1, c2 = st.columns(2)
        c1.metric("Impliziertes Wachstum (Reverse-DCF)", pct(r.get("implied_g")))
        c2.metric("Tatsächliches Rev-CAGR (Hist.)", pct(r.get("actual_g")))
        st.markdown(f'<div style="color:{r_col};font-weight:700;font-size:1.0em;margin:6px 0;">'
                    f'{r.get("verdict","—")}</div>', unsafe_allow_html=True)
        st.caption("[ESTIMATE] Reverse-DCF zeigt: Welches Wachstum preist der Markt beim aktuellen Kurs ein?")
    else:
        st.caption(f"⚠️ Reverse-DCF: {rdcf.get('reason','N/V')}")

    # Stress-Test (vereinfacht)
    if stress_d:
        st.markdown("**⚡ Stress-Test (vereinfacht)**")
        s = stress_d
        rows = []
        for name, sv in s.get("scenarios",{}).items():
            sym2 = sv.get("sym","$")
            rows.append({
                "Szenario": name,
                "IV/Aktie": f"{sym2}{sv['iv']:.2f}" if sv.get("iv",0) > 0 else "n/b",
                "Upside":   f"{sv['upside']:+.1%}" if sv.get("upside") is not None else "n/b",
            })
        if rows:
            st.markdown(_html_table(pd.DataFrame(rows)), unsafe_allow_html=True)
        st.markdown(
            f'<span style="color:{s.get("rr_color","#8b949e")};font-weight:700;">'
            f'{s.get("rr_verdict","—")}</span>', unsafe_allow_html=True)

    st.caption("QUICK FILTER: Kein Python-DCF · KGV/PEG/EV-FCF + Reverse-DCF Primär [B] · "
               "Für Full DCF → Large/Mid Cap (>$2B) analysieren")


# ── CAPEX-CHECK PANEL ─────────────────────────────────────────────────────────
def _render_capex_check(j: dict):
    """Rendert CAPEX-CHECK wenn Capex/Umsatz > 5%."""
    cc = j.get("capex_check", {})
    if not cc.get("triggered"):
        return

    with st.expander(f"⚙️ CAPEX-CHECK · {cc['intensity']} ({pct(cc['ratio'])})", expanded=(cc["intensity"] == "KRITISCH")):
        col1, col2, col3 = st.columns(3)
        col1.metric("Capex/Umsatz", pct(cc["ratio"]), delta="Schwelle: 5%")
        col2.metric("FCF-Qualität", cc["fcf_quality"])
        if cc.get("maintenance_est"):
            col3.metric("Maintenance Capex (est.)", cap_fmt(cc["maintenance_est"]))
        if cc.get("growth_capex_est") and cc["growth_capex_est"] > 0:
            st.info(f"📈 Growth Capex (geschätzt): {cap_fmt(cc['growth_capex_est'])} — prüfen ob Wachstumsinvestment oder Erhaltungsausgabe")
        st.caption(cc["note"])


# ── DEBT MATURITY PANEL ───────────────────────────────────────────────────────
def _render_debt_maturity(j: dict):
    """Rendert Debt Maturity Check Panel."""
    dm = j.get("debt_maturity", {})
    if not dm:
        return

    st.markdown(f"### 💰 Debt Maturity Check &nbsp; "
                f'<span style="color:{dm["color"]};font-weight:700;">{dm["icon"]} {dm["status"]}</span>',
                unsafe_allow_html=True)

    cols = st.columns(4)
    cols[0].metric("Net Debt/EBITDA", xfmt(dm.get("nd")),  delta_color="inverse")
    cols[1].metric("Current Ratio",   nfmt(dm.get("cr")))
    cols[2].metric("EK-Quote",        pct(dm.get("eq")))
    cols[3].metric("D/E Ratio",       nfmt(dm.get("de"))   if dm.get("de") else "N/V")

    if dm["red"]:
        for r in dm["red"]:
            st.error(f"🔴 {r}")
    if dm["yellow"]:
        for y in dm["yellow"]:
            st.warning(f"🟡 {y}")

    st.caption(f"FV-Einfluss: {dm['fv_adj']}")


# ── EXIT-STRATEGIE PANEL ──────────────────────────────────────────────────────
def _render_exit_strategy(j: dict):
    """Rendert Exit-Strategie (KAUFEN-Pflicht per Regel #11)."""
    es = j.get("exit_strategy", {})
    if not es:
        return

    with st.expander("🚪 Exit-Strategie & Trigger", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**⬆️ Upgrade-Trigger**")
            for t in es.get("upgrade", []):
                st.markdown(f"✅ {t}")
            if not es.get("upgrade"):
                st.caption("Alle K erfüllt — kein Upgrade-Trigger aktiv")

        with col2:
            st.markdown("**⬇️ Downgrade-Trigger**")
            for t in es.get("downgrade", []):
                st.markdown(f"⚠️ {t}")

        with col3:
            st.markdown("**🚫 Exit-Bedingungen**")
            for t in es.get("exit", []):
                st.markdown(f"❌ {t}")


# ── EARNINGS-PREP PANEL ───────────────────────────────────────────────────────
def _render_earnings_prep(m: dict, j: dict, eps_hist: pd.DataFrame):
    """EARNINGS-PREP: TERMIN · KONSENS · Beat/Miss · Szenarien · AMPEL · Exit."""
    st.markdown("## 📊 EARNINGS-PREP")
    st.caption("Vorbereitung für den nächsten Earnings-Termin — JACK-Analyse")

    sym    = "€" if m.get("currency") == "EUR" else "$"
    price  = m.get("price") or 0
    sector = m.get("sector", "—")
    name   = m.get("name", "—")
    ticker = m.get("symbol", "—")
    target = m.get("target_price") or 0
    rc     = m.get("revenue_growth") or 0
    fcf_m  = m.get("fcf_margin") or 0
    roic   = m.get("roic") or 0
    nd     = m.get("nd_ebitda") or 0
    sbc    = m.get("sbc_intensity") or 0
    k_met  = j.get("k_met", 0)
    k_basis= j.get("k_basis", 5)
    flags  = j.get("flags", [])
    rating = j.get("rating", "SCHROTT")
    rs     = j.get("reaper_score", 1)

    # ── TERMIN & KONSENS HEADER ───────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Rating",         rating)
    c2.metric("Reaper Score",   f"{rs}/10")
    c3.metric("K-Kriterien",    f"{k_met}/{k_basis}")
    c4.metric("Konfidenz",      j.get("konfidenz", ("—","—","—"))[1])
    c5.metric("Flags aktiv",    str(len(flags)))

    # ── TERMIN & NEXT EARNINGS (from yfinance calendar if available) ──────────
    ex_div = m.get("ex_dividend")
    st.markdown("---")
    st.markdown("**📅 TERMIN & KONSENS**")
    t_col1, t_col2 = st.columns(2)

    with t_col1:
        next_eps = None
        if eps_hist is not None and not eps_hist.empty:
            if "epsEstimate" in eps_hist.columns:
                latest_est = eps_hist["epsEstimate"].dropna()
                if not latest_est.empty:
                    next_eps = latest_est.iloc[0]

        termin_items = [
            ("Ex-Dividende",            str(ex_div)[:10] if ex_div else "N/V"),
            ("Nächster EPS-Konsens",    f"{sym}{next_eps:.2f}" if next_eps else "[MANUAL] prüfen"),
            ("Analysten-Ziel",          f"{sym}{target:.2f} ({(target/price-1):+.1%})" if (target and price) else "N/V"),
            ("# Analysten",             str(int(m.get("analyst_count") or 0)) or "N/V"),
            ("Empfehlung",              (m.get("recommendation") or "N/V").upper()),
            ("Rev-Wachstum YoY",        pct(rc)),
        ]
        for k_n, v_n in termin_items:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;'
                f'border-bottom:1px solid #21262d;padding:4px 0;">'
                f'<span style="color:#8b949e;font-size:0.82em;">{k_n}</span>'
                f'<span style="color:#e6edf3;font-size:0.82em;font-weight:500;">{v_n}</span>'
                f'</div>',
                unsafe_allow_html=True)

    with t_col2:
        # ── EARNINGS AMPEL ────────────────────────────────────────────────────
        # Logic: check beat rate + quality signals
        beat_count = 0
        total_eps  = 0
        if eps_hist is not None and not eps_hist.empty:
            if "epsActual" in eps_hist.columns and "epsEstimate" in eps_hist.columns:
                ep_clean = eps_hist.dropna(subset=["epsActual", "epsEstimate"])
                total_eps = len(ep_clean)
                beat_count = int((ep_clean["epsActual"] >= ep_clean["epsEstimate"]).sum())

        beat_rate = beat_count / total_eps if total_eps > 0 else 0.5
        amp_checks = {
            "Beat-Rate ≥ 70%":       beat_rate >= 0.70,
            "FCF-Marge ≥ 15%":       fcf_m >= 0.15,
            "ROIC > 15%":            roic > 0.15,
            "Keine roten Flags":      not any(f["color"] == "#da3633" for f in flags),
            "K ≥ k_basis − 1":       k_met >= k_basis - 1,
        }
        amp_pass = sum(1 for v in amp_checks.values() if v)
        amp_total = len(amp_checks)

        if amp_pass >= 4:
            amp_c, amp_t, amp_icon = "#3fb950", "GRÜN — Starke Ausgangslage", "🟢"
        elif amp_pass >= 3:
            amp_c, amp_t, amp_icon = "#d29922", "GELB — Solide, Schwächen beachten", "🟡"
        else:
            amp_c, amp_t, amp_icon = "#da3633", "ROT — Risikoreiche Ausgangslage", "🔴"

        st.markdown(
            f'<div style="background:{amp_c}22;border:1px solid {amp_c};border-radius:8px;'
            f'padding:12px 16px;text-align:center;">'
            f'<div style="font-size:1.8em;">{amp_icon}</div>'
            f'<div style="color:{amp_c};font-weight:700;font-size:0.95em;">EARNINGS-AMPEL</div>'
            f'<div style="color:{amp_c};font-size:0.85em;">{amp_t}</div>'
            f'<div style="color:#8b949e;font-size:0.75em;margin-top:4px;">'
            f'{amp_pass}/{amp_total} Kriterien erfüllt</div>'
            f'</div>',
            unsafe_allow_html=True)

        # Check details
        st.markdown("<br>", unsafe_allow_html=True)
        for check, passed in amp_checks.items():
            c = "#3fb950" if passed else "#da3633"
            ic = "✅" if passed else "❌"
            st.markdown(
                f'<div style="display:flex;gap:6px;padding:2px 0;">'
                f'<span>{ic}</span><span style="color:{c};font-size:0.8em;">{check}</span>'
                f'</div>',
                unsafe_allow_html=True)

    st.markdown("---")

    # ── SZENARIEN (Bull / Base / Bear) ────────────────────────────────────────
    st.markdown("**📊 Earnings-Szenarien (nächstes Quartal)**")
    bm = _sector_benchmarks(sector)

    if price > 0:
        # Base: current trend
        base_rev_g  = max(0, rc)
        # Bull: 20% better than base
        bull_rev_g  = base_rev_g * 1.20
        # Bear: 20% worse, min 0
        bear_rev_g  = max(0, base_rev_g * 0.80 - 0.05)

        # Implied price reaction (rough: 1% earnings surprise ≈ 1.5% stock move)
        bull_upside = min(0.25,  bull_rev_g * 1.5)
        bear_down   = max(-0.25, -(abs(base_rev_g - bear_rev_g) * 2 + 0.05))

        szenarien = [
            ("🐂 BULL",  "#3fb950", f"Rev-Wachstum {bull_rev_g:.1%}+",
             f"Guidance erhöht · Marge expansion → Kursreaktion ca. +{bull_upside:.0%}",
             f"{sym}{price * (1+bull_upside):.2f}"),
            ("⚖️ BASE",  "#8b949e", f"Rev-Wachstum {base_rev_g:.1%}",
             "In-line mit Konsens · Keine Guidance-Änderung",
             f"{sym}{price:.2f}"),
            ("🐻 BEAR",  "#da3633", f"Rev-Wachstum {bear_rev_g:.1%}",
             f"Verfehlt Konsens · Guidance gesenkt → Kursreaktion ca. {bear_down:.0%}",
             f"{sym}{price * (1+bear_down):.2f}"),
        ]

        sz_cols = st.columns(3)
        for i, (label, color, growth, note, kurs) in enumerate(szenarien):
            sz_cols[i].markdown(
                f'<div style="background:{color}22;border:1px solid {color};border-radius:8px;'
                f'padding:10px 12px;text-align:center;">'
                f'<div style="color:{color};font-weight:700;">{label}</div>'
                f'<div style="color:#e6edf3;font-weight:600;font-size:0.9em;">{growth}</div>'
                f'<div style="color:#8b949e;font-size:0.76em;margin:4px 0;">{note}</div>'
                f'<div style="color:{color};font-size:0.85em;">Kurs: {kurs}</div>'
                f'</div>',
                unsafe_allow_html=True)

    st.markdown("---")

    # ── BEAT/MISS HISTORY ─────────────────────────────────────────────────────
    if eps_hist is not None and not eps_hist.empty:
        st.markdown(f"**📅 EPS Beat/Miss-Historie  ({beat_count}/{total_eps} Beats = {beat_rate:.0%})**")
        ep = eps_hist.copy()
        if "epsActual" in ep.columns and "epsEstimate" in ep.columns:
            ep = ep.dropna(subset=["epsActual", "epsEstimate"])
            ep["Beat/Miss"] = ep.apply(
                lambda r: "✅ Beat" if r["epsActual"] >= r["epsEstimate"] else "❌ Miss", axis=1)
            ep["Differenz"] = (ep["epsActual"] - ep["epsEstimate"]).apply(lambda x: f"{x:+.2f}")
            ep["Surprise %"] = ep.apply(
                lambda r: f"{(r['epsActual']-r['epsEstimate'])/abs(r['epsEstimate']):.1%}"
                if r['epsEstimate'] != 0 else "—", axis=1)
            ep_disp = ep[["period","epsEstimate","epsActual","Beat/Miss","Differenz","Surprise %"]].rename(
                columns={"period":"Quartal","epsEstimate":"Konsens","epsActual":"Ist"})
            for col_n in ["Konsens","Ist"]:
                ep_disp[col_n] = ep_disp[col_n].apply(
                    lambda v: f"{v:.2f}" if isinstance(v, float) else v)
            st.markdown(_html_table(ep_disp), unsafe_allow_html=True)
    else:
        st.warning("⚠️ Kein EPS-Konsens verfügbar — Beat/Miss-Analyse nicht möglich.")

    st.markdown("---")

    # ── SEKTOR-METRIKEN & EXIT-TRIGGER ───────────────────────────────────────
    col_s, col_t = st.columns(2)
    with col_s:
        st.markdown(f"**🏭 Sektor-Benchmarks ({sector})**")
        bm = _sector_benchmarks(sector)
        sector_data = [
            ("KUV",        nfmt(m.get("price_to_sales")),  f"{bm['kuv'][0]}–{bm['kuv'][1]}x"),
            ("KGV (fwd)",  nfmt(m.get("fwd_pe")),          f"{bm['kgv'][0]}–{bm['kgv'][1]}x"),
            ("EV/EBITDA",  xfmt(m.get("ev_ebitda")),       f"{bm['ev_ebitda'][0]}–{bm['ev_ebitda'][1]}x"),
            ("P/FCF",      xfmt(m.get("p_fcf")),           f"{bm['p_fcf'][0]}–{bm['p_fcf'][1]}x"),
        ]
        st.markdown(_html_table(pd.DataFrame(sector_data,
                    columns=["Metrik","Ist","Peer-Range"])), unsafe_allow_html=True)

    with col_t:
        st.markdown("**📌 Exit-Trigger & These-Status**")
        moat  = j.get("moat", {})
        es    = j.get("exit_strategy", {})
        st.markdown(
            f'<div style="background:#161b22;border-radius:6px;padding:8px 12px;">'
            f'<span style="color:#8b949e;font-size:0.8em;">Moat: '
            f'<b style="color:{moat.get("color","#8b949e")}">{moat.get("label","N/V")} '
            f'({moat.get("score","?")}/4)</b></span><br>'
            + "".join(
                f'<div style="color:#da3633;font-size:0.8em;">⚠️ {t}</div>'
                for t in es.get("downgrade", [])[:3]
            )
            + ("" if es.get("downgrade") else
               '<div style="color:#3fb950;font-size:0.8em;">✅ Keine Downgrade-Trigger aktiv</div>')
            + '</div>',
            unsafe_allow_html=True)


# ── ULTRA-QUICK-SCAN ──────────────────────────────────────────────────────────
def _render_ultra_quick_scan(m: dict, j: dict):
    """MODUS E: BIG FIVE + Reaper-Urteil (Kurzcheck)."""
    st.markdown("## ⚡ ULTRA-QUICK-SCAN")
    st.caption("BIG FIVE: ROIC · Real FCF-Marge · Net Debt/EBITDA · Rev-CAGR · EV/FCF")

    big5 = [
        ("ROIC",           pct(m.get("roic")),       (m.get("roic") or 0) > 0.20),
        ("FCF-Marge",      pct(m.get("fcf_margin")), (m.get("fcf_margin") or 0) >= 0.20),
        ("Net Debt/EBITDA",xfmt(m.get("nd_ebitda")), (m.get("nd_ebitda") or 99) < 2.0),
        ("Rev-CAGR",       pct(m.get("rev_cagr")),   (m.get("rev_cagr") or 0) >= 0.08),
        ("EV/FCF",         xfmt(m.get("ev_fcf")),    0 < (m.get("ev_fcf") or 999) < 25),
    ]
    cols = st.columns(5)
    for i, (name, val, ok) in enumerate(big5):
        c = "#3fb950" if ok else "#da3633"
        cols[i].markdown(
            f'<div class="mtile"><div class="mlabel">{"✅" if ok else "❌"} {name}</div>'
            f'<div class="mvalue" style="color:{c};">{val}</div></div>',
            unsafe_allow_html=True)

    rs     = j.get("reaper_score", 1)
    rating = j.get("rating", "SCHROTT")
    passed = sum(1 for _,_,ok in big5 if ok)

    if rating == "KAUFEN" and passed >= 4:
        verdict, color = "🟢 DEEP DIVE WERT", "#3fb950"
    elif passed >= 3:
        verdict, color = "🟡 WATCHLIST",       "#d29922"
    else:
        verdict, color = "🔴 TONNE",           "#da3633"

    st.markdown(f'<div style="margin-top:16px;font-size:1.2em;font-weight:800;color:{color};">'
                f'REAPER-URTEIL: {verdict} · Score {rs}/10 · {passed}/5 BIG-FIVE ✅</div>',
                unsafe_allow_html=True)


# ── THESE-CHECK ───────────────────────────────────────────────────────────────
def _render_these_check(m: dict, j: dict):
    """MODUS C: THESE-CHECK – Thesis Status."""
    st.markdown("## 🔍 THESE-CHECK")
    st.caption("Trigger: 'Noch intakt?' / 'Halten oder raus?' — Prüft ob die Investment-These noch gilt")

    rating = j.get("rating","SCHROTT")
    flags  = j.get("flags", [])
    moat   = j.get("moat", {})
    abbruch = j.get("abbruch", {})
    k_met   = j.get("k_met", 0)
    k_basis = j.get("k_basis", 5)

    red_flags = [f for f in flags if f["color"] == "#da3633"]
    status_score = 0
    if k_met >= k_basis:        status_score += 3
    elif k_met >= k_basis - 1:  status_score += 1
    if not red_flags:           status_score += 2
    if moat.get("score", 0) >= 3: status_score += 2
    if rating == "KAUFEN":      status_score += 2
    elif rating == "BEOBACHTEN": status_score += 1

    if status_score >= 7:    status, s_color = "✅ INTAKT",   "#3fb950"
    elif status_score >= 4:  status, s_color = "⚠️ WACKELT",  "#d29922"
    else:                    status, s_color = "❌ GEBROCHEN", "#da3633"

    st.markdown(f'<div style="font-size:1.6em;font-weight:900;color:{s_color};margin:12px 0;">'
                f'THESE-STATUS: {status}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📋 Aktuelle Lage**")
        st.markdown(f"K-Kriterien: **{k_met}/{k_basis}**")
        st.markdown(f"Moat: **{moat.get('label','N/V')}**")
        st.markdown(f"Rating: **{rating}** · Score: **{j.get('reaper_score','?')}/10**")
        if red_flags:
            for f in red_flags:
                st.error(f"🔴 {f['name']}: {f['reason']}")

    with col2:
        st.markdown("**🎯 Exit-Trigger Status**")
        es = j.get("exit_strategy", {})
        for t in es.get("downgrade", []):
            st.markdown(f"⚠️ {t}")
        for t in es.get("exit", []):
            st.markdown(f"🚫 {t}")
        if not es.get("downgrade") and not es.get("exit"):
            st.success("Keine Exit-Trigger ausgelöst")

    if abbruch.get("abort"):
        st.error(f"⛔ {abbruch['reason']}")


# ── DECISION MODE ─────────────────────────────────────────────────────────────
def _render_decision_mode(m: dict, j: dict):
    """MODUS F: DECISION MODE – Ultra-Short Entscheidung."""
    st.markdown("## ⚡ DECISION MODE")
    st.caption("Ultra-Short: These · Edge · Devil's Advocate · Rating · 12M-Prediction")

    name   = m.get("name", "Dieses Unternehmen")
    rating = j.get("rating","SCHROTT")
    rs     = j.get("reaper_score", 1)
    moat   = j.get("moat", {})
    ec     = j.get("edge_catalyst", {})
    flags  = j.get("flags",[])
    price  = m.get("price") or 0
    sym    = "€" if m.get("currency") == "EUR" else "$"
    target = m.get("target_price") or 0
    upside = f"{(target/price-1):+.1%}" if price and target else "N/V"

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**① These**")
        st.markdown(j.get("verdict","—"))
        st.markdown(f"**② Edge**")
        st.markdown(f"Edge: **{ec.get('edge','—')}** · Catalyst: **{ec.get('catalyst','—')}**")
        st.markdown(f"Moat: **{moat.get('label','N/V')}**")

    with col2:
        st.markdown(f"**③ Devil's Advocate**")
        if flags:
            for f in flags[:3]:
                st.markdown(f"⚠️ {f['name']}: {f['reason']}")
        else:
            st.markdown("Keine kritischen Gegenargumente identifiziert")

        st.markdown(f"**④ Rating & Size**")
        r_color = "#3fb950" if rating == "KAUFEN" else "#d29922" if rating == "BEOBACHTEN" else "#da3633"
        st.markdown(f'<span style="color:{r_color};font-size:1.3em;font-weight:800;">'
                    f'{rating} · {j.get("sizing","—")} · Score {rs}/10</span>',
                    unsafe_allow_html=True)

        st.markdown(f"**⑤ 12M-Prediction (Konsens)**")
        if target and price:
            pred_color = "#3fb950" if target > price else "#da3633"
            st.markdown(f'<span style="color:{pred_color};">'
                        f'Ziel: {sym}{target:.2f} ({upside}) · Aktuell: {sym}{price:.2f}</span>',
                        unsafe_allow_html=True)
        else:
            st.caption("Kein Analysten-Ziel verfügbar")


# ── MAKRO-RADAR ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=900)    # 15-Min Cache
def _fetch_macro_live() -> dict:
    """Fetch live Makro-Daten via yfinance (15min cache)."""
    _tickers = {
        "^NDX":       ("NQ100 (Nasdaq-100)", "index"),
        "^GSPC":      ("S&P 500",            "index"),
        "^VIX":       ("VIX",                "index"),
        "JPY=X":      ("USD/JPY",            "fx"),
        "EURUSD=X":   ("EUR/USD",            "fx"),
        "^TNX":       ("US 10Y Yield %",     "yield"),
        "^IRX":       ("US 3M Yield %",      "yield"),
        "BTC-USD":    ("Bitcoin (BTC)",      "crypto"),
        "GC=F":       ("Gold ($/oz)",        "commodity"),
        "DX-Y.NYB":   ("DXY (USD-Index)",    "fx"),
    }
    out = {}
    for _tk, (_name, _cat) in _tickers.items():
        try:
            _info = yf.Ticker(_tk).info
            _p  = _info.get("regularMarketPrice") or _info.get("currentPrice")
            _pc = _info.get("previousClose") or _info.get("regularMarketPreviousClose")
            _chg = ((_p - _pc) / _pc) if (_p and _pc and _pc != 0) else None
            out[_name] = {"price": _p, "change": _chg, "cat": _cat}
        except Exception:
            out[_name] = {"price": None, "change": None, "cat": _cat}
    return out


def _render_makro_radar():
    """MAKRO-RADAR — Live-Daten via yfinance (15min Cache) + Zinskurve + Crypto-Ampel."""
    with st.expander("🌍 MAKRO-RADAR [LIVE]", expanded=False):
        with st.spinner("Lade Makro-Daten…"):
            try:
                data = _fetch_macro_live()
                live_ok = True
            except Exception:
                data = {}
                live_ok = False

        if not live_ok or not data:
            st.warning("⚠️ Makro-Live-Daten nicht verfügbar. Prüfe Netzwerk.")
            return

        # ── Zinskurve (2Y–10Y Spread Proxy: 3M vs 10Y) ─────────────────────
        y10 = (data.get("US 10Y Yield %", {}).get("price") or 0)
        y3m = (data.get("US 3M Yield %", {}).get("price") or 0)
        spread = y10 - y3m if (y10 and y3m) else None
        if spread is not None:
            inv = spread < 0
            zk_icon  = "⚠️ INVERS" if inv else "🟢 NORMAL"
            zk_color = "#da3633" if inv else "#3fb950"
            st.markdown(
                f'<div style="background:{zk_color}22;border:1px solid {zk_color};'
                f'border-radius:6px;padding:6px 14px;margin-bottom:8px;">'
                f'<span style="color:{zk_color};font-weight:700;font-size:0.85em;">'
                f'📈 ZINSKURVE: {zk_icon} · Spread (10Y−3M) = {spread:+.2f}%'
                f'</span>'
                f'<span style="color:#8b949e;font-size:0.78em;margin-left:10px;">'
                f'{"Inversion: Rezessionsrisiko erhöht" if inv else "Normale Kurve"}'
                f'</span></div>',
                unsafe_allow_html=True)

        # ── Tile-Grid ────────────────────────────────────────────────────────
        cols = st.columns(5)
        _order = [
            "NQ100 (Nasdaq-100)", "S&P 500", "VIX",
            "USD/JPY", "EUR/USD", "DXY (USD-Index)",
            "US 10Y Yield %", "US 3M Yield %",
            "Bitcoin (BTC)", "Gold ($/oz)"
        ]
        _icons = {
            "index": "📊", "yield": "📉", "fx": "💱",
            "crypto": "₿", "commodity": "🪙"
        }
        for i, _name in enumerate(_order):
            _d = data.get(_name, {})
            _p = _d.get("price")
            _c = _d.get("change")
            _cat = _d.get("cat", "index")
            _icon = _icons.get(_cat, "📊")

            _chg_str = f"{_c:+.2%}" if _c is not None else "—"
            _chg_col = "#3fb950" if (_c or 0) >= 0 else "#da3633"
            _p_str   = (f"{_p:,.2f}" if (_p and _p < 10_000)
                        else (f"{_p:,.0f}" if _p else "—"))

            # Special: yields shown as %
            if _cat == "yield" and _p:
                _p_str = f"{_p:.2f}%"

            cols[i % 5].markdown(
                f'<div style="background:#161b22;border:1px solid #30363d;border-radius:7px;'
                f'padding:8px 10px;margin:3px 0;text-align:center;">'
                f'<div style="color:#8b949e;font-size:0.68em;">{_icon} {_name}</div>'
                f'<div style="color:#e6edf3;font-weight:700;font-size:0.95em;">{_p_str}</div>'
                f'<div style="color:{_chg_col};font-size:0.78em;">{_chg_str}</div>'
                f'</div>',
                unsafe_allow_html=True)

        # ── Crypto Fear & Greed (manuell — kein öffentlicher kostenfreier API) ─
        st.markdown("---")
        st.markdown(
            '<div style="display:flex;gap:12px;align-items:center;">'
            '<span style="color:#8b949e;font-size:0.8em;">🎰 Crypto Fear & Greed:</span>'
            '<a href="https://alternative.me/crypto/fear-and-greed-index/" target="_blank" '
            'style="color:#388bfd;font-size:0.82em;">alternative.me → live prüfen</a>'
            '<span style="color:#8b949e;font-size:0.78em;"> | '
            'BTC dominance, Social sentiment → JACK-Signal: VIX > 30 + F&G < 25 = Einstiegsfenster</span>'
            '</div>',
            unsafe_allow_html=True)

        # ── JACK Makro-Ampel ─────────────────────────────────────────────────
        vix = data.get("VIX", {}).get("price") or 0
        nq  = data.get("NQ100 (Nasdaq-100)", {}).get("change") or 0
        dxy = data.get("DXY (USD-Index)", {}).get("change") or 0

        if vix > 30 or nq < -0.05:
            amp_c, amp_t = "#da3633", "🔴 RISIKO-OFF — Kein neuer KAUFEN-Einstieg. Abstauber abwarten."
        elif vix > 20 or (inv if spread is not None else False):
            amp_c, amp_t = "#d29922", "🟡 ERHÖHTE VORSICHT — Größe reduzieren. Watchlist pflegen."
        else:
            amp_c, amp_t = "#3fb950", "🟢 RISIKO-ON — Qualitäts-KAUFEN möglich. JACK-Kriterien prüfen."

        st.markdown(
            f'<div style="background:{amp_c}22;border:1px solid {amp_c};border-radius:6px;'
            f'padding:8px 14px;margin-top:8px;">'
            f'<span style="color:{amp_c};font-weight:700;font-size:0.85em;">JACK MAKRO-AMPEL: {amp_t}</span>'
            f'</div>',
            unsafe_allow_html=True)
        st.caption("[LIVE] yfinance · 15min Cache · Crypto F&G: manual · Zinskurve: 10Y − 3M")


# ══════════════════════════════════════════════════════════════════════════════
# VALUATION ENGINE: WACC · DCF · REVERSE-DCF · STRESS-TEST · KONVERGENZ
# ══════════════════════════════════════════════════════════════════════════════

def _calc_wacc(m: dict) -> dict:
    beta    = max(0.3, m.get("beta") or 1.0)
    rf      = 0.042          # US 10Y [TRAINING] May 2026
    mrp     = 0.055          # Market Risk Premium [TRAINING] Damodaran
    ke      = rf + beta * mrp

    total_debt = m.get("total_debt") or 0
    interest   = abs(m.get("interest_expense") or 0)
    kd_raw     = interest / total_debt if total_debt > 0 else 0.04
    kd         = max(0.02, min(0.12, kd_raw))

    tax_rate   = m.get("tax_rate") or 0.21
    mktcap     = m.get("mktcap") or 0
    ev         = m.get("ev") or max(mktcap + total_debt, 1)
    w_e        = min(0.97, max(0.03, mktcap / ev)) if ev > 0 else 0.7
    w_d        = 1 - w_e

    wacc = w_e * ke + w_d * kd * (1 - tax_rate)
    wacc = max(0.04, min(0.25, wacc))

    flag, color = ("🔴", "#da3633") if wacc > 0.12 else (("🟡", "#d29922") if wacc > 0.09 else ("🟢", "#3fb950"))
    return {
        "wacc": wacc, "ke": ke, "kd": kd, "kd_raw": kd_raw,
        "rf": rf, "beta": beta, "mrp": mrp,
        "tax_rate": tax_rate, "w_e": w_e, "w_d": w_d,
        "flag": flag, "color": color,
        "note": "[TRAINING] Rf=4.2% (US 10Y) · MRP=5.5% (Damodaran) · Beta [VERIFIED] yfinance",
    }


def _calc_dcf(m: dict, wacc_d: dict) -> dict:
    fcf_base  = m.get("fcf") or 0
    revenue   = m.get("revenue") or 0
    shares    = m.get("shares") or 1
    wacc      = wacc_d.get("wacc", 0.09)
    rev_cagr  = m.get("rev_cagr") or 0.05
    price     = m.get("price") or 0
    nc        = m.get("net_cash") or 0
    sym       = "€" if m.get("currency") == "EUR" else "$"

    if fcf_base <= 0 or revenue <= 0:
        return {"available": False, "reason": "FCF negativ / Revenue fehlt → Reverse-DCF Primär [ESTIMATE]"}

    g_phase = max(0.0, rev_cagr * 0.80)    # −20% Schätz-Malus (JACK-Doktrin)
    g_term  = 0.025

    fcf_proj, fcf_t = [], fcf_base
    for _ in range(5):
        fcf_t *= (1 + g_phase)
        fcf_proj.append(fcf_t)

    pv_fcf = sum(f / (1 + wacc) ** (i + 1) for i, f in enumerate(fcf_proj))
    tv     = fcf_proj[-1] * (1 + g_term) / (wacc - g_term) if wacc > g_term else 0
    pv_tv  = tv / (1 + wacc) ** 5
    tv_pct = pv_tv / (pv_fcf + pv_tv) if (pv_fcf + pv_tv) > 0 else 0

    iv  = (pv_fcf + pv_tv + nc) / shares if shares > 0 else 0
    up  = (iv / price - 1) if (price > 0 and iv > 0) else None
    mos = iv * 0.85 if iv > 0 else None

    return {
        "available": True, "iv": iv, "pv_fcf": pv_fcf, "pv_tv": pv_tv,
        "tv": tv, "tv_pct": tv_pct, "tv_warning": tv_pct > 0.70,
        "upside": up, "mos": mos, "g_phase": g_phase, "g_term": g_term,
        "fcf_proj": fcf_proj, "wacc": wacc, "sym": sym, "price": price,
    }


def _calc_reverse_dcf(m: dict, wacc_d: dict) -> dict:
    mktcap   = m.get("mktcap") or 0
    fcf_base = m.get("fcf") or 0
    nc       = m.get("net_cash") or 0
    wacc     = wacc_d.get("wacc", 0.09)
    g_term   = 0.025

    if fcf_base <= 0 or mktcap <= 0:
        return {"available": False, "reason": "FCF negativ oder Market Cap fehlt"}

    ev_impl = mktcap - nc

    def dcf_at_g(g):
        if g >= wacc: return float("inf")
        f, pv = fcf_base, 0
        for i in range(5):
            f *= (1 + g); pv += f / (1 + wacc) ** (i + 1)
        pv += f * (1 + g_term) / (wacc - g_term) / (1 + wacc) ** 5
        return pv

    lo, hi = -0.30, wacc - 0.001
    for _ in range(60):
        mid = (lo + hi) / 2
        (lo if dcf_at_g(mid) < ev_impl else hi).__class__  # dummy
        if dcf_at_g(mid) < ev_impl: lo = mid
        else: hi = mid
    ig = (lo + hi) / 2

    ag = m.get("rev_cagr") or 0
    if ig > ag + 0.05:   verd, vc = "📈 Markt preist MEHR Wachstum ein — Downside-Risiko",    "#d29922"
    elif ig < ag - 0.05: verd, vc = "💎 Markt preist WENIGER Wachstum ein — Upside möglich",   "#3fb950"
    else:                verd, vc = "⚖️ Markt preist aktuelles Wachstum korrekt ein",           "#8b949e"

    return {"available": True, "implied_g": ig, "actual_g": ag,
            "verdict": verd, "color": vc, "ev_impl": ev_impl}


def _calc_stress_test(m: dict, wacc_d: dict) -> dict:
    rev   = m.get("revenue") or 0
    fcf_m = m.get("fcf_margin") or 0
    rc    = m.get("rev_cagr") or 0.05
    sh    = m.get("shares") or 1
    price = m.get("price") or 0
    nc    = m.get("net_cash") or 0
    wacc  = wacc_d.get("wacc", 0.09)
    sym   = "€" if m.get("currency") == "EUR" else "$"
    g_t   = 0.025

    def _iv(g, fm, w):
        if rev <= 0: return 0
        f = rev * fm; pv = 0
        for i in range(5):
            f *= (1 + g); pv += f / (1 + w) ** (i + 1)
        if w > g_t: pv += f * (1 + g_t) / (w - g_t) / (1 + w) ** 5
        return (pv + nc) / sh if sh > 0 else 0

    scenarios = {
        "🐂 Bull": {"g": rc + 0.05, "fm": fcf_m + 0.03, "wd": -0.005},
        "📊 Base": {"g": rc * 0.80, "fm": fcf_m,        "wd":  0.000},
        "🐻 Bear": {"g": max(0, rc - 0.08), "fm": max(0, fcf_m - 0.05), "wd": 0.015},
    }
    res = {}
    for name, s in scenarios.items():
        iv  = _iv(s["g"], max(0, s["fm"]), max(0.04, wacc + s["wd"]))
        res[name] = {
            "g": s["g"], "fm": s["fm"], "wacc": wacc + s["wd"],
            "iv": iv, "upside": (iv / price - 1) if price and iv > 0 else None, "sym": sym,
        }

    bu = res["🐂 Bull"].get("upside") or 0
    be = res["🐻 Bear"].get("upside") or 0
    if be < -0.30 and bu < 0.15:  rv, rc2 = "❌ Schlechtes Risiko/Rendite-Profil — JACK: Geld direkt verbrennen?", "#da3633"
    elif bu > 0.30 and be > -0.25: rv, rc2 = "✅ Attraktives Risiko/Rendite-Profil", "#3fb950"
    else:                          rv, rc2 = "⚖️ Moderates Risiko/Rendite-Profil",   "#d29922"

    return {"scenarios": res, "rr_verdict": rv, "rr_color": rc2}


def _calc_konvergenz(m: dict, dcf: dict, rdcf: dict) -> dict:
    price  = m.get("price") or 0
    target = m.get("target_price") or 0
    ev_fcf = m.get("ev_fcf") or 0
    sigs   = []

    if dcf.get("available") and dcf.get("iv") and price:
        up = dcf["iv"] / price - 1
        sigs.append(("DCF", "🟢 Unterbewertet" if up > 0.15 else ("🟡 Fair" if up > -0.10 else "🔴 Überbewertet"),
                     "#3fb950" if up > 0.15 else ("#d29922" if up > -0.10 else "#da3633")))

    if ev_fcf > 0:
        sigs.append(("EV/FCF", "🟢 Günstig" if ev_fcf < 25 else ("🟡 Fair" if ev_fcf < 35 else "🔴 Teuer"),
                     "#3fb950" if ev_fcf < 25 else ("#d29922" if ev_fcf < 35 else "#da3633")))

    if target and price:
        up2 = target / price - 1
        sigs.append(("Analysten", "🟢 Aufwärts" if up2 > 0.10 else ("🟡 Neutral" if up2 > -0.05 else "🔴 Abwärts"),
                     "#3fb950" if up2 > 0.10 else ("#d29922" if up2 > -0.05 else "#da3633")))

    if not sigs: return {"label": "⚪ KEINE DATEN", "color": "#8b949e", "signals": []}

    greens = sum(1 for _, v, _ in sigs if "🟢" in v)
    reds   = sum(1 for _, v, _ in sigs if "🔴" in v)
    if greens >= 2 and reds == 0: label, col = "✅ STARK",        "#3fb950"
    elif greens > reds:            label, col = "🟡 MODERAT",      "#d29922"
    else:                          label, col = "⚠️ WIDERSPRUCH",  "#d29922"

    return {"label": label, "color": col, "signals": sigs}


def _calc_shareholder_yield(m: dict) -> dict:
    div     = m.get("dividend") or 0
    sbc_i   = m.get("sbc_intensity") or 0
    buyback = m.get("buyback_yield_est") or 0
    total   = div + buyback - sbc_i
    label, color = ("🟢 POSITIV", "#3fb950") if total > 0.03 else (("🟡 NEUTRAL", "#d29922") if total > 0 else ("🔴 NEGATIV", "#da3633"))
    return {"div": div, "buyback": buyback, "sbc": sbc_i, "total": total,
            "label": label, "color": color,
            "note": "Buyback: geschätzt via Cashflow [VERIFIED] · Dividende [VERIFIED] · SBC [VERIFIED]"}


def _calc_analyse_tiefe(m: dict) -> dict:
    """
    Auto-Detection Analyse-Tiefe:
      Large Cap (>$10B) → FULL DEEP DIVE
      Small/Mid Cap (≤$10B) → QUICK FILTER
    Valuation-Mode:
      FCF positiv & stabil  → FULL DCF + Reverse Sanity
      Lückenhaft / Talsohle → Reverse-DCF Primär + Multiples
      Negativer FCF         → Multiples-Only + Reverse-DCF
    """
    mktcap   = m.get("mktcap") or 0
    fcf      = m.get("fcf") or 0
    fcf_m    = m.get("fcf_margin") or 0
    revenue  = m.get("revenue") or 0
    roic     = m.get("roic") or 0
    rev_cagr = m.get("rev_cagr") or 0
    nd_ebitda = m.get("nd_ebitda")

    # ── TIEFE ────────────────────────────────────────────────────────────────
    if mktcap > 10e9:
        tiefe = "FULL DEEP DIVE"
        tiefe_reason = f"Large Cap ({cap_fmt(mktcap)}) → alle Module aktiv"
    elif mktcap > 2e9:
        tiefe = "FULL DEEP DIVE"
        tiefe_reason = f"Mid Cap ({cap_fmt(mktcap)}) → FULL DEEP DIVE"
    else:
        tiefe = "QUICK FILTER"
        tiefe_reason = f"Small Cap ({cap_fmt(mktcap)}) → DNA-Check + Konfidenz + Verdict"

    # ── VALUATION-MODE ────────────────────────────────────────────────────────
    # Negativer FCF
    if fcf < 0:
        val_mode = "MULTIPLES ONLY"
        val_reason = f"Negativer FCF ({cap_fmt(fcf)}) → Multiples + Reverse-DCF Primär [B]"
    # Lückenhaft: FCF positiv aber sehr niedrig Marge (Talsohle-Indiz)
    elif fcf_m < 0.05 and roic < 0.10:
        val_mode = "REVERSE DCF PRIMARY"
        val_reason = f"FCF-Marge {fcf_m:.1%} + ROIC {roic:.1%} → Talsohle-Indiz → Reverse-DCF Primär [B]"
    # Stabil & verifiziert
    elif fcf > 0 and fcf_m >= 0.10:
        val_mode = "FULL DCF"
        val_reason = f"FCF positiv & stabil ({fcf_m:.1%} Marge) → Full DCF [B] + Reverse Sanity [C]"
    else:
        val_mode = "REVERSE DCF PRIMARY"
        val_reason = f"Lückenhaft / geringe FCF-Marge → Reverse-DCF Primär [B] + Multiples"

    return {
        "tiefe":       tiefe,
        "val_mode":    val_mode,
        "tiefe_reason": tiefe_reason,
        "val_reason":  val_reason,
        "is_full":     tiefe == "FULL DEEP DIVE",
        "is_quick":    tiefe == "QUICK FILTER",
    }


def _calc_technical(m: dict) -> dict:
    price = m.get("price") or 0
    hi52  = m.get("hi52") or 0
    lo52  = m.get("lo52") or 0
    if not (price and hi52 and lo52 and hi52 > lo52):
        return {"available": False}
    pos      = (price - lo52) / (hi52 - lo52)
    from_hi  = (price - hi52) / hi52
    if pos > 0.70:   trend, tc, sig = "📈 Oberes Drittel",   "#3fb950", "Momentum positiv"
    elif pos > 0.40: trend, tc, sig = "↔️ Mittleres Drittel", "#d29922", "Neutral"
    else:            trend, tc, sig = "📉 Unteres Drittel",   "#da3633", "Mögliche Bodenbildung"
    return {"available": True, "pos": pos, "trend": trend, "color": tc,
            "signal": sig, "from_hi": from_hi,
            "note": "[VERIFIED] 52W Hoch/Tief via yfinance · Kein Live-Chart"}


def _calc_devils_advocate(m: dict, j: dict) -> dict:
    """
    Devil's Advocate mit 3 strukturellen Fragen + BIAS-KILL-SWITCH.
    Returns dict mit 'questions', 'bias_strikes', 'bias_kill'.
    """
    rating  = j.get("rating", "SCHROTT")
    pe      = m.get("pe") or 0
    fwd_pe  = m.get("fwd_pe") or 0
    ev_fcf  = m.get("ev_fcf") or 0
    ev_ebi  = m.get("ev_ebitda") or 0
    beta    = m.get("beta") or 1.0
    nd      = m.get("nd_ebitda") or 0
    sbc     = m.get("sbc_intensity") or 0
    rc      = m.get("rev_cagr") or 0
    fcf_m   = m.get("fcf_margin") or 0
    roic    = m.get("roic") or 0
    sector  = (m.get("sector") or "").lower()
    flags   = j.get("flags", [])
    k_met   = j.get("k_met", 0)
    k_basis = j.get("k_basis", 5)
    rs      = j.get("reaper_score", 1)
    moat    = j.get("moat", {}).get("score", 0)
    dcf_fv  = j.get("dcf", {}).get("fair_value") or 0
    price   = m.get("price") or 0

    questions = []

    # ── FRAGE 1: PREIS-FRAGE (Bewertungsrisiko) ────────────────────────────────
    q1_risk  = "HOCH" if pe > 40 or ev_fcf > 40 else ("MITTEL" if pe > 25 or ev_fcf > 25 else "NIEDRIG")
    q1_color = "#da3633" if q1_risk == "HOCH" else ("#d29922" if q1_risk == "MITTEL" else "#3fb950")

    if pe > 0 and fwd_pe > 0 and price > 0:
        # Simulate 30% growth miss → what's implied downside?
        miss_pe = fwd_pe * 1.30   # expand P/E if growth slows
        implied_down = (pe / miss_pe) - 1 if miss_pe > 0 else 0
        q1_detail = (f"KGV {pe:.0f}x / Forward {fwd_pe:.0f}x. Bei 30%-Wachstums-Enttäuschung: "
                     f"KGV-Expansion auf ~{miss_pe:.0f}x → Kurskorrektur ca. {implied_down:.0%}.")
    elif ev_fcf > 0:
        q1_detail = (f"EV/FCF {ev_fcf:.0f}x — Markt preist dauerhaft hohes Wachstum ein. "
                     f"Bei Wachstumsverlangsamung: multiple contraction 30–50% möglich.")
    else:
        q1_detail = "Bewertungsdaten unvollständig — manuelle KGV/EV-FCF-Prüfung erforderlich."

    questions.append({
        "nr":     "①",
        "titel":  "PREIS-FRAGE (Bewertungsrisiko)",
        "frage":  "Was passiert mit dem Kurs, wenn das Wachstum enttäuscht?",
        "detail": q1_detail,
        "risiko": q1_risk,
        "color":  q1_color,
    })

    # ── FRAGE 2: THESE-FRAGE (Strukturrisiko) ──────────────────────────────────
    q2_risks = []
    if moat < 2:
        q2_risks.append(f"Moat schwach ({moat}/4) — Wettbewerb kann Margen komprimieren")
    if nd > 2.5:
        q2_risks.append(f"Net Debt/EBITDA {nd:.1f}x — Zinsrisiko bei Refinanzierung oder Zinsanstieg")
    if sbc > 0.12:
        q2_risks.append(f"SBC {pct(sbc)} — Management-Kompensation geht auf Kosten der Aktionäre")
    if rc < 0.05 and roic < 0.15:
        q2_risks.append(f"Wachstum {pct(rc)} + ROIC {pct(roic)} — kein Compounding-Katalysator sichtbar")
    if k_met < k_basis - 1:
        q2_risks.append(f"K-Kriterien: nur {k_met}/{k_basis} — strukturelle Qualitätslücke")
    if not q2_risks:
        q2_risks.append("Keine dominanten Strukturrisiken identifiziert — eigene Due Diligence empfohlen")

    q2_risk  = "HOCH" if len(q2_risks) >= 3 else ("MITTEL" if len(q2_risks) >= 2 else "NIEDRIG")
    q2_color = "#da3633" if q2_risk == "HOCH" else ("#d29922" if q2_risk == "MITTEL" else "#3fb950")
    questions.append({
        "nr":     "②",
        "titel":  "THESE-FRAGE (Strukturrisiko)",
        "frage":  "Was ist das stärkste Gegenargument für diese Investitionsthese?",
        "detail": " | ".join(q2_risks),
        "risiko": q2_risk,
        "color":  q2_color,
    })

    # ── FRAGE 3: MAKRO-FRAGE (Kontextrisiko) ───────────────────────────────────
    _macro_risks = {
        "technology":        "Regulierung (KI/Datenschutz) + Zinsanstieg komprimiert Tech-Multiples drastisch",
        "financial":         "Kreditrisiko-Schock oder Bankenregulierung → Bilanzqualität in Rezession",
        "energy":            "Commodity-Zyklus-Umkehr + Energie-Transition beschleunigt → Stranded Assets",
        "basic materials":   "China-Nachfragerückgang + Überkapazität → Rohstoffpreise kollabieren",
        "consumer cyclical": "Rezession + Konsumrückgang — Zykliker verlieren 50–70% in Abschwüngen",
        "real estate":       "Zinsanstieg → Cap-Rate-Expansion → Immobilienbewertungen fallen 20–40%",
        "utilities":         "Regulierungsänderungen + Zinsen hoch → Dividend-Yield-Konkurrenz",
        "healthcare":        "Preisregulierung (Inflation Reduction Act) + IP-Klippe",
    }
    q3_risk_text = "Kein dominantes Makro-Risiko identifiziert. Beta prüfen."
    for _k, _v in _macro_risks.items():
        if _k in sector:
            q3_risk_text = _v
            break

    _beta_lvl    = "hohe" if beta > 1.3 else "moderate"
    _beta_corr   = f"-{round(beta * 20)}% erwartet"
    q3_beta_note = (f"Beta {beta:.1f} → {_beta_lvl} Marktkorrelation. "
                    f"Bei 20%-Korrektur: {_beta_corr}.")
    q3_detail    = f"{q3_risk_text} | {q3_beta_note}"
    q3_risk      = "HOCH" if beta > 1.5 or any(f["color"] == "#da3633" for f in flags) else \
                   ("MITTEL" if beta > 1.2 else "NIEDRIG")
    q3_color     = "#da3633" if q3_risk == "HOCH" else ("#d29922" if q3_risk == "MITTEL" else "#3fb950")
    questions.append({
        "nr":     "③",
        "titel":  "MAKRO-FRAGE (Kontextrisiko)",
        "frage":  "Welches externe Makro-Risiko könnte diese Analyse zunichte machen?",
        "detail": q3_detail,
        "risiko": q3_risk,
        "color":  q3_color,
    })

    # ── BIAS-KILL-SWITCH ───────────────────────────────────────────────────────
    bias_checks = {
        "Recency Bias":       rs >= 7 and rc < 0.05,      # High score despite low growth
        "Narrative Bias":     moat >= 3 and k_met < k_basis,  # Nice story, missing gates
        "Anchoring Bias":     dcf_fv > 0 and price > 0 and dcf_fv / price > 1.5,  # DCF >>  price
        "Confirmation Bias":  rating == "KAUFEN" and len([f for f in flags if f["color"] == "#da3633"]) > 0,
    }
    strikes     = [name for name, hit in bias_checks.items() if hit]
    bias_kill   = len(strikes) >= 2   # 2+ strikes → BIAS-STRIKE warning

    return {
        "questions":   questions,
        "bias_checks": bias_checks,
        "strikes":     strikes,
        "bias_kill":   bias_kill,
    }


# ── RENDER: VALUATION ENGINE ──────────────────────────────────────────────────
def _render_wacc_dcf(j: dict, m: dict):
    wacc_d   = j.get("wacc_data", {})
    dcf_d    = j.get("dcf", {})
    rdcf_d   = j.get("reverse_dcf", {})
    stress_d = j.get("stress_test", {})
    konv     = j.get("konvergenz", {})

    st.markdown("### 5️⃣ Valuation Engine")

    if konv:
        sigs = konv.get("signals", [])
        sig_html = " &nbsp;·&nbsp; ".join(
            f'<span style="color:{c};">{n}: {v}</span>' for n, v, c in sigs)
        st.markdown(
            f'<div style="background:#161b22;border:1px solid #30363d;border-radius:8px;'
            f'padding:10px 16px;margin-bottom:10px;">'
            f'<span style="color:#8b949e;font-size:0.8em;">KONVERGENZ: </span>'
            f'<span style="color:{konv.get("color","#8b949e")};font-weight:700;">{konv.get("label","—")}</span>'
            f'<span style="font-size:0.8em;margin-left:14px;">{sig_html}</span></div>',
            unsafe_allow_html=True)

    # ── KGV-SPRUNG-CHECK (Pflicht QUICK FILTER) ───────────────────────────────
    pe_val     = m.get("pe") or 0
    fwd_pe_val = m.get("fwd_pe") or 0
    if pe_val > 0 and fwd_pe_val > 0:
        kgv_delta = abs(fwd_pe_val - pe_val) / pe_val
        if kgv_delta > 0.50:
            kgv_dir = "gesunken" if fwd_pe_val < pe_val else "gestiegen"
            kgv_reason = "EPS-Wachstum prognostiziert" if fwd_pe_val < pe_val else "EPS-Rückgang / Einmaleffekte"
            st.warning(
                f"⚠️ KGV-SPRUNG-FLAG: Trailing KGV {pe_val:.0f}x → Forward KGV {fwd_pe_val:.0f}x "
                f"({kgv_delta:.0%} {kgv_dir}) — Pflicht-Erklärung: **{kgv_reason}**\n\n"
                f"Ohne Erklärung → [TRAINING] statt [VERIFIED]. Prüfe: Einmaleffekt / EPS-Einbruch / Verwässerung?")

    t1, t2, t3, t4 = st.tabs(["📐 WACC", "📊 Full DCF", "🔄 Reverse-DCF", "⚡ Stress-Test"])

    with t1:
        if not wacc_d:
            st.caption("N/V")
        else:
            w = wacc_d
            c1, c2, c3 = st.columns(3)
            c1.metric("WACC", pct(w["wacc"]))
            c2.metric("Cost of Equity (Ke)", pct(w["ke"]))
            c3.metric("Cost of Debt (Kd, after-tax)", pct(w["kd"] * (1 - w["tax_rate"])))
            st.markdown(f"""
| Komponente | Wert | Daten-Tag |
|---|---|---|
| Risk-free Rate (Rf) | {pct(w["rf"])} | [TRAINING] US 10Y |
| Beta (β) | {nfmt(w["beta"])} | [VERIFIED] yfinance |
| Market Risk Premium | {pct(w["mrp"])} | [TRAINING] Damodaran |
| Cost of Equity (Ke) | {pct(w["ke"])} | CAPM |
| Cost of Debt (Kd) | {pct(w["kd"])} | [VERIFIED] Finanzdaten |
| Steuersatz | {pct(w["tax_rate"])} | [VERIFIED] yfinance |
| EK-Gewicht | {pct(w["w_e"])} | [VERIFIED] |
| FK-Gewicht | {pct(w["w_d"])} | [VERIFIED] |
| **WACC** | **{pct(w["wacc"])}** | Dynamisch |
""")
            st.caption(w["note"])

    with t2:
        d = dcf_d
        if not d.get("available"):
            st.warning(f"⚠️ {d.get('reason','DCF nicht verfügbar')} → Reverse-DCF Primär")
        else:
            sym = d["sym"]
            c1, c2, c3 = st.columns(3)
            c1.metric("Intrinsic Value / Aktie", f"{sym}{d['iv']:.2f}")
            c2.metric("Upside/Downside", f"{d['upside']:+.1%}" if d.get("upside") is not None else "N/V")
            c3.metric("MoS-Preis (−15%)", f"{sym}{d['mos']:.2f}" if d.get("mos") else "N/V")

            if d["tv_warning"]:
                st.error(f"⚠️ TV-WARNUNG (Klasse A #15): Terminal Value = {d['tv_pct']:.0%} des EV (>70%). "
                         "Intrinsic Value stark von weit-entfernten Cash Flows abhängig.")
            else:
                st.success(f"✅ Terminal Value = {d['tv_pct']:.0%} des EV — akzeptabel")

            st.markdown(f"""
| DCF-Komponente | Wert |
|---|---|
| FCF-Wachstum Phase (−20% Doktrin) | {pct(d["g_phase"])} |
| Terminal Growth Rate | {pct(d["g_term"])} |
| WACC | {pct(d["wacc"])} |
| PV FCF (5J) | {cap_fmt(d["pv_fcf"])} |
| PV Terminal Value | {cap_fmt(d["pv_tv"])} |
| TV-Anteil | {d["tv_pct"]:.0%} |
""")
            st.caption("[ESTIMATE] Projektion auf historischen Daten + Rev-CAGR")

    with t3:
        r = rdcf_d
        if not r.get("available"):
            st.warning(f"⚠️ {r.get('reason','N/V')}")
        else:
            c1, c2 = st.columns(2)
            c1.metric("Impliziertes Wachstum (Reverse-DCF)", pct(r["implied_g"]))
            c2.metric("Tatsächliches Rev-CAGR", pct(r["actual_g"]))
            st.markdown(f'<div style="color:{r["color"]};font-weight:700;font-size:1.05em;margin:8px 0;">'
                        f'{r["verdict"]}</div>', unsafe_allow_html=True)
            st.caption("Reverse-DCF: Welche Wachstumsrate preist der Markt beim aktuellen Kurs ein?")

    with t4:
        if not stress_d:
            st.caption("N/V")
        else:
            s = stress_d
            st.markdown(f'<span style="color:{s["rr_color"]};font-weight:700;">{s["rr_verdict"]}</span>',
                        unsafe_allow_html=True)
            rows = []
            for name, sv in s["scenarios"].items():
                sym2 = sv.get("sym", "$")
                rows.append({
                    "Szenario": name,
                    "Rev-Wachstum": pct(sv["g"]),
                    "FCF-Marge": pct(sv["fm"]),
                    "WACC": pct(sv["wacc"]),
                    "IV/Aktie": f"{sym2}{sv['iv']:.2f}" if sv.get("iv", 0) > 0 else "n/b",
                    "Upside": f"{sv['upside']:+.1%}" if sv.get("upside") is not None else "n/b",
                })
            st.markdown(_html_table(pd.DataFrame(rows)), unsafe_allow_html=True)
            st.caption("[ESTIMATE] Bear = −8pp Wachstum · −5pp FCF-Marge · +1.5pp WACC")


def _render_beneish():
    with st.expander("🔍 Beneish M-Score", expanded=False):
        st.warning("⏭️ SKIP (Klasse B Regel): Beneish M-Score erfordert alle 8 Komponenten als [LIVE] "
                   "(SEC-Echtzeitdaten). yfinance liefert [VERIFIED] Jahresabschlüsse — keine Live-SEC-Pull.\n\n"
                   "→ Für manuelle Analyse: SEC EDGAR / TIKR aufrufen.")
        st.markdown("""
| Beneish-Komponente | Status |
|---|---|
| Days Sales in Receivables Index (DSRI) | ⏭️ SKIP |
| Gross Margin Index (GMI) | ⏭️ SKIP |
| Asset Quality Index (AQI) | ⏭️ SKIP |
| Sales Growth Index (SGI) | ⏭️ SKIP |
| Depreciation Index (DEPI) | ⏭️ SKIP |
| SGA Expenses Index (SGAI) | ⏭️ SKIP |
| Leverage Index (LVGI) | ⏭️ SKIP |
| Total Accruals to Total Assets (TATA) | ⏭️ SKIP |
""")


def _render_sbc_check(j: dict, m: dict):
    """Schritt 4 — SBC-CHECK: FCF − SBC = Real FCF · Verwässerungs-Transparenz."""
    sbc_abs    = m.get("sbc_abs") or 0
    fcf        = m.get("fcf") or 0
    revenue    = m.get("revenue") or 0
    sbc_i      = m.get("sbc_intensity") or 0
    fcf_margin = m.get("fcf_margin") or 0
    sym        = "€" if m.get("currency") == "EUR" else "$"

    real_fcf   = fcf - sbc_abs
    real_fcf_m = real_fcf / revenue if revenue > 0 else 0
    sbc_drag   = sbc_abs / revenue if revenue > 0 else sbc_i

    infected = sbc_i > 0.15
    warn     = sbc_i > 0.10
    icon     = "☢️" if infected else ("⚠️" if warn else "✅")
    color    = "#da3633" if infected else ("#d29922" if warn else "#3fb950")
    label    = "KRITISCH ☢️" if infected else ("WARNUNG ⚠️" if warn else "OK ✅")

    with st.expander(f"{icon} SBC-CHECK — Real FCF: {sym}{real_fcf/1e9:.2f}B  ({real_fcf_m:.1%} Marge)", expanded=True):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("**🧮 FCF − SBC Rechnung**")
            rows = [
                ("Reported FCF",   f"{sym}{fcf/1e9:.2f}B",         f"{fcf_margin:+.1%}"),
                ("− SBC (Awards)", f"−{sym}{sbc_abs/1e9:.2f}B",    f"−{sbc_drag:.1%}"),
                ("= Real FCF",     f"{sym}{real_fcf/1e9:.2f}B",    f"{real_fcf_m:+.1%}"),
            ]
            for label_r, val, pct_v in rows:
                fc = "#3fb950" if label_r.startswith("=") else ("#da3633" if label_r.startswith("−") else "#e6edf3")
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;'
                    f'border-bottom:1px solid #21262d;padding:5px 0;">'
                    f'<span style="color:#8b949e;font-size:0.85em;">{label_r}</span>'
                    f'<span style="color:{fc};font-weight:{"700" if label_r.startswith("=") else "400"};'
                    f'font-size:0.85em;">{val} <span style="color:#6e7681;font-size:0.85em;">({pct_v})</span>'
                    f'</span></div>',
                    unsafe_allow_html=True)

        with c2:
            # SBC-INFECTION verdict
            st.markdown("**⚑ SBC-INFECTION-CHECK**")
            st.markdown(
                f'<div style="background:{color}22;border:1px solid {color};border-radius:8px;'
                f'padding:10px 14px;text-align:center;">'
                f'<div style="color:{color};font-weight:800;font-size:1.1em;">{label}</div>'
                f'<div style="color:#8b949e;font-size:0.78em;margin-top:4px;">'
                f'SBC/Revenue = {sbc_i:.1%}</div>'
                f'</div>',
                unsafe_allow_html=True)
            if infected:
                st.markdown(
                    '<div style="margin-top:8px;color:#da3633;font-size:0.8em;">'
                    '→ Konfidenz-Deckel: max 🟡 MITTEL<br>'
                    '→ Reaper Score: −2 Malus<br>'
                    '→ Sizing: max Tier 3<br>'
                    '"Management bedient sich zuerst."</div>',
                    unsafe_allow_html=True)
            elif warn:
                st.markdown(
                    '<div style="margin-top:8px;color:#d29922;font-size:0.8em;">'
                    '→ SBC 10–15%: Beobachten.<br>'
                    '→ FCF-Qualität prüfen.</div>',
                    unsafe_allow_html=True)

        with c3:
            # FCF quality comparison
            st.markdown("**📊 FCF-Qualität**")
            for name, val, ref, ok in [
                ("Reported FCF-Marge", pct(fcf_margin),  "≥ 20%", fcf_margin >= 0.20),
                ("Real FCF-Marge",     pct(real_fcf_m),  "≥ 15%", real_fcf_m >= 0.15),
                ("SBC-Drag",           pct(sbc_drag),     "< 10%", sbc_drag < 0.10),
            ]:
                fc = "#3fb950" if ok else "#da3633"
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;padding:3px 0;">'
                    f'<span style="color:#8b949e;font-size:0.82em;">{name}</span>'
                    f'<span style="color:{fc};font-weight:600;font-size:0.82em;">'
                    f'{val} <span style="color:#6e7681;">({ref})</span></span></div>',
                    unsafe_allow_html=True)
        st.caption("[VERIFIED] SBC aus Cash-Flow-Statement (yfinance) · Real FCF = Reported FCF − SBC")


def _render_share_count_trend(m: dict):
    """Financial Health: Share Count Trend (3J) — Verwässerung vs. Buyback-Analyse."""
    hist = m.get("share_history", [])
    shares_cur = m.get("shares_out") or m.get("shares") or 0

    if not hist and not shares_cur:
        return

    with st.expander("📉 Share Count Trend (3J) — Verwässerungs-Analyse", expanded=False):
        c1, c2 = st.columns([1.5, 1])

        with c1:
            if len(hist) >= 2:
                # Calculate trend
                oldest = hist[-1]["shares"]
                newest = hist[0]["shares"]
                total_change = (newest - oldest) / oldest if oldest > 0 else 0
                yrs = min(len(hist), 3)
                cagr = (newest / oldest) ** (1 / yrs) - 1 if (oldest > 0 and yrs > 0) else 0

                trend_icon  = "🔻" if cagr < -0.02 else ("⚠️" if cagr > 0.02 else "✅")
                trend_color = "#3fb950" if cagr <= -0.02 else ("#da3633" if cagr > 0.03 else "#d29922")
                trend_label = "BUYBACK ✅" if cagr < -0.02 else ("VERWÄSSERUNG ⚠️" if cagr > 0.02 else "STABIL")

                st.markdown(
                    f'<div style="background:{trend_color}22;border:1px solid {trend_color};'
                    f'border-radius:8px;padding:10px 16px;margin-bottom:10px;">'
                    f'<span style="color:{trend_color};font-weight:700;">{trend_icon} {trend_label}</span>'
                    f'<span style="color:#8b949e;font-size:0.82em;margin-left:10px;">'
                    f'CAGR: {cagr:+.2%} p.a. · Gesamt {yrs}J: {total_change:+.1%}</span>'
                    f'</div>',
                    unsafe_allow_html=True)

                # Table
                rows = []
                for entry in hist[:4]:
                    rows.append({
                        "Jahr":    entry["date"][:4],
                        "Aktien": f"{entry['shares']/1e6:.1f}M",
                        "vs. Aktuell": f"{(entry['shares'] - shares_cur)/shares_cur:+.1%}" if shares_cur else "—",
                    })
                st.markdown(_html_table(pd.DataFrame(rows)), unsafe_allow_html=True)
            else:
                if shares_cur:
                    st.metric("Aktuelle Aktienzahl", f"{shares_cur/1e6:.1f}M")
                st.caption("Nicht genug historische Daten für Trend-Analyse.")

        with c2:
            st.markdown("**JACK-Bewertung**")
            if len(hist) >= 2:
                cagr_val = cagr  # already calculated above
                rules = [
                    (cagr_val < -0.02, "✅ Aktive Buybacks: Kapital kommt zu Aktionären zurück"),
                    (abs(cagr_val) <= 0.02, "🟡 Stabile Aktienzahl: Neutral"),
                    (0.02 < cagr_val <= 0.05, "⚠️ Leichte Verwässerung: SBC/Equity-Kap. prüfen"),
                    (cagr_val > 0.05, "🔴 VERWÄSSERUNG: > 5%/Jahr — Aktionärsschädlich"),
                ]
                for cond, msg in rules:
                    if cond:
                        st.markdown(f'<span style="font-size:0.85em;">{msg}</span>',
                                    unsafe_allow_html=True)
                        break
            st.markdown(
                '<div style="background:#161b22;border-radius:6px;padding:8px 12px;margin-top:8px;">'
                '<span style="color:#8b949e;font-size:0.75em;font-weight:700;">REGEL</span><br>'
                '<span style="color:#c9d1d9;font-size:0.78em;">'
                'Rückläufig = Buybacks > Dilution<br>'
                'Steigend > 3% p.a. → Warnsignal<br>'
                'Steigend > 5% p.a. → Rotes Flag</span>'
                '</div>',
                unsafe_allow_html=True)
        st.caption("[VERIFIED] Aktienzahl aus Bilanz (yfinance) · Trend über max. 4 Jahresabschlüsse")


def _render_sanity_check(j: dict, m: dict):
    """Schritt 5B — SANITY-CHECK: DCF vs. Analyst-Konsens vs. Marktpreis."""
    dcf_d   = j.get("dcf", {})
    rdcf_d  = j.get("reverse_dcf", {})
    konv    = j.get("konvergenz", {})
    price   = m.get("price") or 0
    target  = m.get("target_price") or 0
    sym     = "€" if m.get("currency") == "EUR" else "$"

    dcf_fv  = dcf_d.get("fair_value")   or 0
    impl_g  = rdcf_d.get("implied_growth") or 0
    wacc_v  = j.get("wacc_data", {}).get("wacc") or 0.09

    with st.expander("🔍 Schritt 5B — SANITY-CHECK: DCF · Konsens · Marktpreis", expanded=False):
        cols = st.columns(4)

        # Tile: Preis
        def _tile(col, label, value, sub="", color="#e6edf3"):
            col.markdown(
                f'<div style="background:#161b22;border:1px solid #30363d;border-radius:7px;'
                f'padding:10px 12px;text-align:center;">'
                f'<div style="color:#8b949e;font-size:0.72em;">{label}</div>'
                f'<div style="color:{color};font-weight:700;font-size:1.1em;">{value}</div>'
                f'<div style="color:#6e7681;font-size:0.73em;">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True)

        def _upside(val, base=price):
            if val and base and base > 0:
                u = (val / base) - 1
                c = "#3fb950" if u > 0.15 else ("#da3633" if u < -0.10 else "#d29922")
                return f"{u:+.1%}", c
            return "N/V", "#8b949e"

        dcf_up, dcf_c   = _upside(dcf_fv)
        tar_up, tar_c   = _upside(target)

        _tile(cols[0], "Marktpreis [LIVE]",        f"{sym}{price:.2f}", "Aktuell", "#388bfd")
        _tile(cols[1], "DCF-Fairer Wert [ESTIMATE]", f"{sym}{dcf_fv:.2f}" if dcf_fv else "N/V", f"Upside: {dcf_up}", dcf_c)
        _tile(cols[2], "Analyst-Ziel [ESTIMATE]",  f"{sym}{target:.2f}" if target else "N/V",   f"Upside: {tar_up}", tar_c)
        _tile(cols[3], "Impl. Wachstum (RDCF)",    f"{impl_g:.1%}" if impl_g else "N/V",
              f"WACC: {wacc_v:.1%}", "#d29922" if impl_g > 0.15 else "#8b949e")

        st.markdown("---")

        # Convergenz-Tabelle
        checks = []
        if dcf_fv and price:
            diff = dcf_fv / price - 1
            checks.append({
                "Vergleich": "DCF vs. Marktpreis",
                "DCF": f"{sym}{dcf_fv:.2f}",
                "Referenz": f"{sym}{price:.2f}",
                "Abweichung": f"{diff:+.1%}",
                "Signal": "✅ Unterbewertet" if diff > 0.15 else ("⚠️ Fair" if diff > -0.10 else "🔴 Überbewertet"),
            })
        if target and price:
            diff2 = target / price - 1
            checks.append({
                "Vergleich": "Konsens-Ziel vs. Marktpreis",
                "DCF": f"{sym}{target:.2f}",
                "Referenz": f"{sym}{price:.2f}",
                "Abweichung": f"{diff2:+.1%}",
                "Signal": "✅ Upside" if diff2 > 0.10 else ("⚠️ Neutral" if diff2 > -0.05 else "🔴 Abwärts"),
            })
        if dcf_fv and target:
            diff3 = dcf_fv / target - 1
            checks.append({
                "Vergleich": "DCF vs. Konsens-Ziel",
                "DCF": f"{sym}{dcf_fv:.2f}",
                "Referenz": f"{sym}{target:.2f}",
                "Abweichung": f"{diff3:+.1%}",
                "Signal": "✅ Konvergenz" if abs(diff3) < 0.15 else "⚠️ Divergenz → BEOBACHTEN",
            })

        if checks:
            st.markdown(_html_table(pd.DataFrame(checks)), unsafe_allow_html=True)

        # Konvergenz-Urteil
        kl = konv.get("label", "")
        kc = konv.get("color", "#8b949e")
        if kl:
            st.markdown(
                f'<div style="background:{kc}22;border:1px solid {kc};border-radius:6px;'
                f'padding:8px 14px;margin-top:8px;">'
                f'<span style="color:{kc};font-weight:700;font-size:0.85em;">'
                f'KONVERGENZ-URTEIL: {kl}</span>'
                f'<span style="color:#8b949e;font-size:0.78em;margin-left:10px;">'
                f'Regel: DCF und Konsens müssen grob in die selbe Richtung zeigen.</span>'
                f'</div>',
                unsafe_allow_html=True)

        impl_warn = impl_g > 0.25
        if impl_warn:
            st.warning(f"⚠️ SANITY-FLAG: Implizites Wachstum {impl_g:.1%} > 25% — Markt preist Perfektion ein. "
                       "Jede Enttäuschung → signifikante Kurskorrektur.")
        st.caption(f"[ESTIMATE] DCF: JACK-Modell ({wacc_v:.1%} WACC) · Konsens: {m.get('analyst_count',0) or '?'} Analysten · [LIVE] Preis: yfinance")


def _render_shareholder_yield(j: dict):
    sy = j.get("shareholder_yield", {})
    if not sy:
        return
    with st.expander(f"💵 Shareholder Yield — {sy['label']}", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Dividende", pct(sy["div"]))
        c2.metric("Buyback (est.)", pct(sy["buyback"]))
        c3.metric("SBC-Verwässerung", pct(sy["sbc"]), delta_color="inverse")
        c4.metric("Netto Shareholder Yield", pct(sy["total"]))
        st.caption(sy["note"])


def _render_technical_insider(j: dict, m: dict):
    tech = j.get("technical", {})
    with st.expander("📐 Klasse C: Technical Alignment & Insider", expanded=False):
        st.caption("Klasse C = Best Effort · Kein Analyse-Stopper")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📈 Technical Alignment (52W Proxy)**")
            if tech.get("available"):
                st.markdown(f"Position: **{tech['trend']}**")
                st.markdown(f'<span style="color:{tech["color"]};">Signal: {tech["signal"]}</span>',
                            unsafe_allow_html=True)
                st.markdown(f"Vom 52W-Hoch: **{tech['from_hi']:+.1%}**")
                st.progress(float(tech["pos"]))
                st.caption(tech["note"])
            else:
                st.caption("Kursdaten nicht verfügbar")
        with c2:
            st.markdown("**👥 Insider & Institutionen**")
            ip = m.get("insider_pct"); itp = m.get("inst_pct"); sp = m.get("short_pct")
            if ip is not None:
                c = "#3fb950" if ip > 0.05 else "#8b949e"
                st.markdown(f'<span style="color:{c};">Insider-Anteil: **{pct(ip)}**</span>',
                            unsafe_allow_html=True)
            if itp is not None:
                st.markdown(f"Institutionen: **{pct(itp)}**")
            if sp is not None:
                c = "#da3633" if sp > 0.10 else "#8b949e"
                st.markdown(f'<span style="color:{c};">Short Interest: **{pct(sp)}**</span>',
                            unsafe_allow_html=True)
            st.caption("[VERIFIED] Daten: yfinance · Stand: letzter Meldetermin")


def _render_devil(j: dict):
    da = j.get("devils_advocate", {})
    # Backward-compat: if old list format
    if isinstance(da, list):
        with st.expander("😈 Devil's Advocate (Schritt 7)", expanded=False):
            for a in da:
                st.markdown(f"⚠️ {a}")
        return

    questions  = da.get("questions",   [])
    bias_chk   = da.get("bias_checks", {})
    strikes    = da.get("strikes",     [])
    bias_kill  = da.get("bias_kill",   False)

    bias_color = "#da3633" if bias_kill else ("#d29922" if strikes else "#3fb950")
    bias_icon  = "☢️ BIAS-STRIKE AKTIV" if bias_kill else (f"⚠️ {len(strikes)} Bias-Signal(e)" if strikes else "✅ Kein Bias-Strike")

    with st.expander(f"😈 Devil's Advocate & Bias-Kill-Switch (Schritt 7) — {bias_icon}", expanded=False):

        if bias_kill:
            st.error(
                "☢️ **BIAS-KILL-SWITCH AKTIV** — 2+ Bias-Signale erkannt. "
                "Rating mit erhöhter Skepsis prüfen. Gegencheck: Was sagen die K-Kriterien nüchtern?")

        # ── 3 Strukturfragen ─────────────────────────────────────────────────
        st.markdown("**🎯 3 Strukturelle Gegenargumente**")
        for q in questions:
            risk_c = q["color"]
            st.markdown(
                f'<div style="background:{risk_c}11;border-left:3px solid {risk_c};'
                f'border-radius:0 8px 8px 0;padding:10px 14px;margin:6px 0;">'
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">'
                f'<span style="color:{risk_c};font-weight:800;font-size:1.1em;">{q["nr"]}</span>'
                f'<span style="color:#e6edf3;font-weight:700;font-size:0.9em;">{q["titel"]}</span>'
                f'<span style="background:{risk_c}33;color:{risk_c};border-radius:4px;'
                f'padding:1px 7px;font-size:0.72em;font-weight:700;margin-left:auto;">'
                f'RISIKO: {q["risiko"]}</span>'
                f'</div>'
                f'<div style="color:#8b949e;font-size:0.82em;font-style:italic;margin-bottom:4px;">'
                f'❓ {q["frage"]}</div>'
                f'<div style="color:#c9d1d9;font-size:0.82em;">{q["detail"]}</div>'
                f'</div>',
                unsafe_allow_html=True)

        st.markdown("---")

        # ── BIAS-KILL-SWITCH ─────────────────────────────────────────────────
        st.markdown(f'**🧠 BIAS-KILL-SWITCH** <span style="color:{bias_color};font-weight:700;">{bias_icon}</span>',
                    unsafe_allow_html=True)

        bias_col1, bias_col2 = st.columns(2)
        bias_defs = {
            "Recency Bias":       "Rating basiert auf kurzfristiger Performance statt LT-Trend?",
            "Narrative Bias":     "Folge ich einer Story statt den nüchternen K-Kriterien?",
            "Anchoring Bias":     "Bin ich an einen alten Kurs oder DCF-Wert fixiert?",
            "Confirmation Bias":  "Ignoriere ich rote Flags weil ich kaufen will?",
        }
        for i, (name, desc) in enumerate(bias_defs.items()):
            hit   = name in strikes
            b_c   = "#da3633" if hit else "#3fb950"
            b_ic  = "🔴" if hit else "🟢"
            (bias_col1 if i < 2 else bias_col2).markdown(
                f'<div style="padding:4px 0;">'
                f'<span style="color:{b_c};">{b_ic} <b>{name}</b></span><br>'
                f'<span style="color:#8b949e;font-size:0.78em;">{desc}</span>'
                f'</div>',
                unsafe_allow_html=True)

        st.caption("Gegencheck: K-Kriterien nüchtern lesen · Bei Bias-Strike: Analyst/Peer fragen bevor Kaufentscheidung")


def _render_zyklus(m: dict):
    sector = (m.get("sector") or "").lower()
    if not any(x in sector for x in ["energy", "basic materials", "consumer cyclical", "industrials"]):
        return
    with st.expander(f"🔄 Zyklus-Overlay — {m.get('sector','—')} erkannt als zyklisch", expanded=False):
        nd = m.get("nd_ebitda")
        st.markdown(f"""
**Zyklus-Sonderregeln (Klasse B):**
- K-Kriterien über vollständigen Zyklus messen (nicht nur Boom-Phase)
- ROIC / FCF können im Abschwung stark schwanken → Mid-Cycle Normalisierung
- Net Debt/EBITDA Schwelle für Zykliker: **< 1.5x** (strenger als Standard < 2x)
- JACK-Empfehlung: Bewertung auf Mid-Cycle EPS / EBITDA basieren
""")
        if nd is not None and nd > 1.5:
            st.warning(f"⚠️ Net Debt/EBITDA {nd:.1f}x > 1.5x — Zykliker-Warnschwelle überschritten")
        st.caption("[TRAINING] Zyklus-Position: Kein Live-Makro verfügbar. Manuell prüfen: Wo steht der Sektor?")


def _render_fx_pflicht(m: dict):
    currency = m.get("currency", "USD")
    if currency == "EUR":
        return
    price = m.get("price") or 0
    FX_RATES = {"USD": 0.92, "GBP": 1.17, "JPY": 0.0062, "CHF": 1.07, "CAD": 0.68, "SEK": 0.086}
    fx = FX_RATES.get(currency, 1.0)
    st.info(f"🌍 **FX-PFLICHT (Klasse A Regel #13):** Werte in **{currency}**. "
            f"Approx. EUR-Rate: 1 {currency} ≈ EUR {fx:.4f} [TRAINING]. "
            f"Aktueller Kurs {currency} {price:.2f} ≈ EUR {price * fx:.2f}. "
            f"→ Präzise FX: ECB / Yahoo Finance Devisen.")


def _render_daten_hierarchie(m: dict = None):
    """Vollständige DATEN-HIERARCHIE mit SEC-Live-Status und Links."""
    sec      = (m or {}).get("sec", {})
    ticker   = (m or {}).get("name", "")
    symbol   = ""
    stufe    = (m or {}).get("_stufe", "3")
    stufe_lbl= (m or {}).get("_stufe_label", "[STUFE 3] Yahoo Finance")
    sec_avail = sec.get("available", False)
    cik      = sec.get("cik", "")

    # Stufe-1 Status
    s1_icon  = "✅" if sec_avail else "❌"
    s1_color = "#3fb950" if sec_avail else "#da3633"
    s1_note  = f"CIK: {cik}" if sec_avail else sec.get("reason", "Nicht verfügbar")

    with st.expander("🗂️ DATEN-HIERARCHIE & QUELLEN-STATUS", expanded=False):

        # Aktive Daten-Stufe Banner
        s_color = "#3fb950" if stufe == "1+3" else "#d29922"
        st.markdown(
            f'<div style="background:{s_color}22;border:1px solid {s_color};border-radius:6px;'
            f'padding:8px 14px;margin-bottom:10px;">'
            f'<span style="color:{s_color};font-weight:700;">AKTIVE DATEN-STUFE: {stufe_lbl}</span>'
            f'</div>', unsafe_allow_html=True)

        # Stufen-Tabelle mit Live-Status
        rows_html = f"""
<table style="width:100%;border-collapse:collapse;font-size:0.85em;">
<tr>
  <th style="background:#21262d;color:#8b949e;padding:8px 12px;text-align:left;border:1px solid #30363d;">Stufe</th>
  <th style="background:#21262d;color:#8b949e;padding:8px 12px;text-align:left;border:1px solid #30363d;">Quelle</th>
  <th style="background:#21262d;color:#8b949e;padding:8px 12px;text-align:left;border:1px solid #30363d;">Verwendung</th>
  <th style="background:#21262d;color:#8b949e;padding:8px 12px;text-align:left;border:1px solid #30363d;">Status</th>
  <th style="background:#21262d;color:#8b949e;padding:8px 12px;text-align:left;border:1px solid #30363d;">Tag</th>
</tr>
<tr>
  <td style="background:#161b22;color:#e6edf3;padding:7px 12px;border:1px solid #21262d;font-weight:700;">Stufe 1</td>
  <td style="background:#161b22;color:#e6edf3;padding:7px 12px;border:1px solid #21262d;">SEC EDGAR / 10-K Filings</td>
  <td style="background:#161b22;color:#8b949e;padding:7px 12px;border:1px solid #21262d;">Primärquelle · K-Kriterien</td>
  <td style="background:#161b22;padding:7px 12px;border:1px solid #21262d;">
    <span style="color:{s1_color};font-weight:700;">{s1_icon} {'AKTIV' if sec_avail else 'N/V'}</span>
    <span style="color:#8b949e;font-size:0.8em;"> {s1_note}</span>
  </td>
  <td style="background:#161b22;padding:7px 12px;border:1px solid #21262d;">
    <span style="background:#3fb95022;border:1px solid #3fb950;color:#3fb950;border-radius:3px;padding:1px 6px;font-size:0.8em;">[VERIFIED]</span>
  </td>
</tr>
<tr>
  <td style="background:#161b22;color:#e6edf3;padding:7px 12px;border:1px solid #21262d;font-weight:700;">Stufe 2</td>
  <td style="background:#161b22;color:#e6edf3;padding:7px 12px;border:1px solid #21262d;">Koyfin · TIKR · StockAnalysis · Macrotrends</td>
  <td style="background:#161b22;color:#8b949e;padding:7px 12px;border:1px solid #21262d;">Sekundärquelle · Bestätigung</td>
  <td style="background:#161b22;padding:7px 12px;border:1px solid #21262d;">
    <span style="color:#d29922;font-weight:700;">🔗 Links unten</span>
  </td>
  <td style="background:#161b22;padding:7px 12px;border:1px solid #21262d;">
    <span style="background:#3fb95022;border:1px solid #3fb950;color:#3fb950;border-radius:3px;padding:1px 6px;font-size:0.8em;">[VERIFIED]</span>
  </td>
</tr>
<tr>
  <td style="background:#161b22;color:#e6edf3;padding:7px 12px;border:1px solid #21262d;font-weight:700;">Stufe 3</td>
  <td style="background:#161b22;color:#e6edf3;padding:7px 12px;border:1px solid #21262d;">Yahoo Finance (yfinance) ← Haupt-Feed</td>
  <td style="background:#161b22;color:#8b949e;padding:7px 12px;border:1px solid #21262d;">Alle Metriken · Kurs [LIVE]</td>
  <td style="background:#161b22;padding:7px 12px;border:1px solid #21262d;">
    <span style="color:#3fb950;font-weight:700;">✅ AKTIV</span>
  </td>
  <td style="background:#161b22;padding:7px 12px;border:1px solid #21262d;">
    <span style="background:#3fb95022;border:1px solid #3fb950;color:#3fb950;border-radius:3px;padding:1px 6px;font-size:0.8em;">[VERIFIED*]</span>
  </td>
</tr>
<tr>
  <td style="background:#161b22;color:#e6edf3;padding:7px 12px;border:1px solid #21262d;font-weight:700;">Stufe 4</td>
  <td style="background:#161b22;color:#e6edf3;padding:7px 12px;border:1px solid #21262d;">Schätzungen / WACC-Komponenten / TTM</td>
  <td style="background:#161b22;color:#8b949e;padding:7px 12px;border:1px solid #21262d;">Nur E-Kriterien & WACC</td>
  <td style="background:#161b22;padding:7px 12px;border:1px solid #21262d;">
    <span style="color:#d29922;font-weight:700;">⚠️ EINGESCHRÄNKT</span>
  </td>
  <td style="background:#161b22;padding:7px 12px;border:1px solid #21262d;">
    <span style="background:#d2992222;border:1px solid #d29922;color:#d29922;border-radius:3px;padding:1px 6px;font-size:0.8em;">[ESTIMATE]</span>
  </td>
</tr>
</table>
"""
        st.markdown(rows_html, unsafe_allow_html=True)

        st.markdown("---")

        # Direkt-Links zu allen Stufen
        st.markdown("**🔗 Schnell-Links für manuelle Verifikation:**")
        if m:
            name_q = (m.get("name") or "").replace(" ", "+")
            sym    = m.get("symbol", "") or ""

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Stufe 1 — Primär:**")
                if sec_avail and cik:
                    st.markdown(f"[📄 SEC EDGAR 10-K]({sec.get('sec_url','#')})")
                    st.markdown(f"[📊 SEC XBRL Facts](https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json)")
                else:
                    st.caption("SEC: nur US-Aktien")
                st.markdown(f"[🏢 Investor Relations (Google)](https://www.google.com/search?q={name_q}+investor+relations+annual+report)")

            with col2:
                st.markdown("**Stufe 2 — Sekundär:**")
                st.markdown(f"[📈 StockAnalysis](https://stockanalysis.com/stocks/{sym.lower()}/financials/)")
                st.markdown(f"[📊 Macrotrends](https://www.macrotrends.net/stocks/charts/{sym}/{name_q}/revenue)")
                st.markdown(f"[💹 Koyfin](https://app.koyfin.com/)")
                st.markdown(f"[📉 TIKR](https://app.tikr.com/)")

            with col3:
                st.markdown("**Stufe 3 — Bestätigung:**")
                st.markdown(f"[🦁 Yahoo Finance](https://finance.yahoo.com/quote/{sym}/financials/)")
                st.markdown(f"[📰 MarketScreener](https://www.marketscreener.com/)")
                st.markdown(f"[🦊 Traderfox](https://traderfox.de/)")
                st.markdown(f"[🔍 Seeking Alpha](https://seekingalpha.com/symbol/{sym})")

        st.markdown("---")
        st.markdown("**📋 Schätz-Doktrin:**")
        st.caption("K-Kriterien: [ESTIMATE] VERBOTEN · [N/V] = Sofort-Abbruch\n"
                   "E-Kriterien: [ESTIMATE] erlaubt mit −20% Upside-Malus + Konfidenz-Deckel 🟡\n"
                   "[VERIFIED*]: yfinance gilt als VERIFIED wenn ≤10% Abweichung zur SEC-Quelle")


def _render_sec_crossval(m: dict):
    """SEC EDGAR vs yfinance Kreuzvalidierungs-Panel."""
    sec = m.get("sec", {})
    if not sec.get("available"):
        return

    checks = [
        ("Umsatz (Revenue)",    m.get("revenue"),   sec.get("revenue"),   m.get("_cv_revenue",    {})),
        ("Nettogewinn",         m.get("_net_inc"),   sec.get("net_income"), m.get("_cv_net_income", {})),
        ("EBIT",                m.get("_op_inc"),    sec.get("op_income"),  m.get("_cv_op_income",  {})),
        ("Bruttogewinn",        m.get("_gp"),        sec.get("gross_profit"),m.get("_cv_gross",     {})),
        ("Total Assets",        m.get("_assets"),    sec.get("assets"),     m.get("_cv_assets",     {})),
    ]

    with st.expander("🔬 Stufe-1 Kreuzvalidierung: SEC EDGAR vs Yahoo Finance", expanded=False):
        st.markdown(f"**Unternehmen (SEC):** {sec.get('entity','—')} · CIK: `{sec.get('cik','—')}`")
        st.markdown(f"[Direkt zu SEC EDGAR 10-K]({sec.get('sec_url','#')})")
        st.markdown("---")

        rows_html = """
<table style="width:100%;border-collapse:collapse;font-size:0.84em;">
<tr>
  <th style="background:#21262d;color:#8b949e;padding:7px 12px;border:1px solid #30363d;text-align:left;">Kennzahl</th>
  <th style="background:#21262d;color:#8b949e;padding:7px 12px;border:1px solid #30363d;text-align:right;">Yahoo (Stufe 3)</th>
  <th style="background:#21262d;color:#8b949e;padding:7px 12px;border:1px solid #30363d;text-align:right;">SEC (Stufe 1)</th>
  <th style="background:#21262d;color:#8b949e;padding:7px 12px;border:1px solid #30363d;text-align:center;">Abweichung</th>
  <th style="background:#21262d;color:#8b949e;padding:7px 12px;border:1px solid #30363d;text-align:left;">JACK-Status</th>
</tr>"""
        for name_k, yf_v, sec_v, cv in checks:
            yf_str  = cap_fmt(yf_v)  if yf_v  else "N/V"
            sec_str = cap_fmt(sec_v) if sec_v else "N/V"
            tag     = cv.get("tag", "N/V")
            color   = cv.get("color", "#8b949e")
            delta   = cv.get("delta_pct")
            delta_s = f"{delta:.1%}" if delta is not None else "—"
            rows_html += f"""
<tr>
  <td style="background:#161b22;color:#e6edf3;padding:7px 12px;border:1px solid #21262d;">{name_k}</td>
  <td style="background:#161b22;color:#8b949e;padding:7px 12px;border:1px solid #21262d;text-align:right;">{yf_str}</td>
  <td style="background:#161b22;color:#e6edf3;padding:7px 12px;border:1px solid #21262d;text-align:right;font-weight:600;">{sec_str}</td>
  <td style="background:#161b22;padding:7px 12px;border:1px solid #21262d;text-align:center;">
    <span style="color:{color};">{delta_s}</span></td>
  <td style="background:#161b22;padding:7px 12px;border:1px solid #21262d;">
    <span style="background:{color}22;border:1px solid {color};color:{color};border-radius:3px;
      padding:1px 7px;font-size:0.8em;font-weight:700;">{tag}</span>
  </td>
</tr>"""
        rows_html += "</table>"
        st.markdown(rows_html, unsafe_allow_html=True)

        st.markdown("---")
        st.caption("SAUBER ≤10% · DISKREPANZ 10–20% (SEC dominiert) · ERKLÄRUNGSPFLICHT >20% (TTM vs FY? Adjustments?)")
        stufe_lbl = m.get("_stufe_label", "")
        sc = "#3fb950" if "1+3" in m.get("_stufe","") else "#d29922"
        st.markdown(f'<span style="color:{sc};font-weight:700;">Aktive Daten-Stufe: {stufe_lbl}</span>',
                    unsafe_allow_html=True)


def _render_quick_news_scan(m: dict, j: dict):
    """MODUS D: Quick News Scan (kein Live-Web — Training-Hinweis)."""
    st.markdown("## 📰 MODUS D: QUICK NEWS SCAN")
    st.warning("⚠️ [TRAINING] — Kein Live-Web-Search aktiv. "
               "JACK kann keine Echtzeit-News abrufen (kein Web-Search-Tool in dieser Umgebung).")
    st.info("**Für Live-News:** Yahoo Finance / Bloomberg / Reuters / Google Finance aufrufen.\n\n"
            "JACK prüft: Wichtigste Meldung · Kurs-Reaktion · Depot-Relevanz · Signal oder Rauschen · Exit-Trigger berührt?")

    name = m.get("name", "Unternehmen")
    st.markdown(f"**Zuletzt bekannte Fundamentaldaten für {name}:**")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rating",       j.get("rating","—"))
    c2.metric("Score",        f"{j.get('reaper_score','—')}/10")
    c3.metric("Flags aktiv",  str(len(j.get("flags",[]))))
    c4.metric("Konfidenz",    j.get("konfidenz",("—","—","—"))[1])

    es = j.get("exit_strategy",{})
    if es.get("downgrade"):
        st.markdown("**⚠️ Exit-Trigger — prüfe ob News diese berührt:**")
        for t in es["downgrade"]:
            st.markdown(f"• {t}")

    rec = (m.get("recommendation") or "").upper()
    target = m.get("target_price")
    price  = m.get("price") or 0
    sym    = "€" if m.get("currency") == "EUR" else "$"
    if target and price:
        up = target / price - 1
        st.markdown(f"**Analysten-Konsens:** {rec} · Ziel: {sym}{target:.2f} ({up:+.1%}) · "
                    f"[VERIFIED] {m.get('analyst_count',0):.0f} Analysten")


# ══════════════════════════════════════════════════════════════════════════════
# MODUS B: BATTLE — K-BASIS Vorfilter · Vergleichstabelle · FINAL SCORE
# ══════════════════════════════════════════════════════════════════════════════
def _render_battle(ta: str, ma: dict, ja: dict, tb: str, mb: dict, jb: dict):
    """MODUS B BATTLE: Vollständiger K-BASIS Vorfilter + Vergleichstabelle + FINAL SCORE."""

    sym_a = "€" if ma.get("currency") == "EUR" else "$"
    sym_b = "€" if mb.get("currency") == "EUR" else "$"

    r_color = {"KAUFEN": "#3fb950", "BEOBACHTEN": "#d29922", "SCHROTT": "#da3633"}

    # ── HEADER: Side-by-side Rating ───────────────────────────────────────────
    st.markdown("## ⚔️ MODUS B — BATTLE ANALYSE")
    h1, h2 = st.columns(2)
    for _col, _sym, _m, _j, _t in [(h1, sym_a, ma, ja, ta), (h2, sym_b, mb, jb, tb)]:
        _r     = _j.get("rating", "SCHROTT")
        _rs    = _j.get("reaper_score", 1)
        _rc    = r_color.get(_r, "#8b949e")
        _k_ic, _k_lb, _k_c = _j.get("konfidenz", ("🔴","NIEDRIG","#da3633"))
        _mode  = _m.get("_k_basis_mode", "5S")
        _price = _m.get("price") or 0
        _col.markdown(
            f'<div style="background:{_rc}22;border:2px solid {_rc};border-radius:10px;'
            f'padding:14px;text-align:center;">'
            f'<div style="color:#8b949e;font-size:0.75em;">{_m.get("name","—")} ({_t})</div>'
            f'<div style="color:{_rc};font-weight:800;font-size:1.4em;">{_r}</div>'
            f'<div style="color:#e6edf3;font-weight:700;font-size:1.1em;">{_rs}/10</div>'
            f'<div style="color:#8b949e;font-size:0.8em;">{_k_ic} {_k_lb} · {_mode}</div>'
            f'<div style="color:#8b949e;font-size:0.8em;">{_sym}{_price:.2f}</div>'
            f'</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── K-BASIS VORFILTER ─────────────────────────────────────────────────────
    st.markdown("**🔬 K-BASIS Vorfilter (Gatekeeper)**")
    ka_rows, kb_rows = ja.get("K", {}), jb.get("K", {})
    all_k_names = list(dict.fromkeys(list(ka_rows.keys()) + list(kb_rows.keys())))

    battle_k = []
    for name in all_k_names:
        va = ka_rows.get(name, {})
        vb = kb_rows.get(name, {})
        pa = va.get("pass", False)
        pb = vb.get("pass", False)
        winner = "→ A ✅" if (pa and not pb) else ("→ B ✅" if (pb and not pa) else ("beide ✅" if (pa and pb) else "beide ❌"))
        battle_k.append({
            "Kriterium":    name,
            f"{ta} Wert":   va.get("val", "N/V"),
            f"{ta} ✓":      "✅" if pa else "❌",
            f"{tb} Wert":   vb.get("val", "N/V"),
            f"{tb} ✓":      "✅" if pb else "❌",
            "Vorteil":      winner,
        })
    st.markdown(_html_table(pd.DataFrame(battle_k)), unsafe_allow_html=True)

    st.markdown("---")

    # ── HAUPTKENNZAHLEN VERGLEICH ──────────────────────────────────────────────
    st.markdown("**📊 Hauptkennzahlen Vergleich**")
    metrics_compare = [
        ("Reaper Score",     f"{ja['reaper_score']}/10",             f"{jb['reaper_score']}/10"),
        ("K-Kriterien",      f"{ja['k_met']}/{ja['k_basis']}",       f"{jb['k_met']}/{jb['k_basis']}"),
        ("E-Kriterien",      f"{ja['e_met']}/{len(ja['E'])}",        f"{jb['e_met']}/{len(jb['E'])}"),
        ("Rating",           ja.get("rating","—"),                   jb.get("rating","—")),
        ("Konfidenz",        ja.get("konfidenz",("","NIEDRIG",""))[1], jb.get("konfidenz",("","NIEDRIG",""))[1]),
        ("K-BASIS Modus",    ma.get("_k_basis_mode","5S"),           mb.get("_k_basis_mode","5S")),
        ("Marktkapitalisierung", cap_fmt(ma.get("mktcap")),          cap_fmt(mb.get("mktcap"))),
        ("KGV (trailing)",   nfmt(ma.get("pe")) or "N/V",           nfmt(mb.get("pe")) or "N/V"),
        ("EV/EBITDA",        xfmt(ma.get("ev_ebitda")),             xfmt(mb.get("ev_ebitda"))),
        ("ROIC",             pct(ma.get("roic")),                    pct(mb.get("roic"))),
        ("FCF-Marge",        pct(ma.get("fcf_margin")),              pct(mb.get("fcf_margin"))),
        ("Rev-CAGR",         pct(ma.get("rev_cagr")),               pct(mb.get("rev_cagr"))),
        ("Net Debt/EBITDA",  xfmt(ma.get("nd_ebitda")),             xfmt(mb.get("nd_ebitda"))),
        ("Bruttomarge",      pct(ma.get("gross_margin")),            pct(mb.get("gross_margin"))),
        ("Moat Score",       f"{ja.get('moat',{}).get('score','?')}/4", f"{jb.get('moat',{}).get('score','?')}/4"),
        ("Sizing",           ja.get("sizing","—"),                   jb.get("sizing","—")),
        ("Abstauber-Preis",  ja.get("abstauber","—"),               jb.get("abstauber","—")),
        ("Flags aktiv",      str(len(ja.get("flags",[]))),           str(len(jb.get("flags",[])))),
    ]

    df_cmp = pd.DataFrame(metrics_compare, columns=["Kennzahl", ta, tb])
    st.markdown(_html_table(df_cmp), unsafe_allow_html=True)

    st.markdown("---")

    # ── FINAL SCORE ───────────────────────────────────────────────────────────
    st.markdown("**🏆 FINAL SCORE — BATTLE-URTEIL**")

    # Score: Reaper Score (40%) + K-met/k_basis (30%) + Moat (20%) + Flags (-10% each)
    def _battle_score(j, m):
        rs     = j.get("reaper_score", 1)
        k_met  = j.get("k_met", 0)
        k_bas  = j.get("k_basis", 5)
        moat_s = j.get("moat", {}).get("score", 0)
        flags  = len([f for f in j.get("flags", []) if f["color"] == "#da3633"])
        score  = (rs / 10 * 40) + (k_met / k_bas * 30) + (moat_s / 4 * 20) - (flags * 5)
        return round(max(0, score), 1)

    score_a = _battle_score(ja, ma)
    score_b = _battle_score(jb, mb)
    winner  = ta if score_a >= score_b else tb
    w_score = max(score_a, score_b)
    l_score = min(score_a, score_b)

    f1, f2, f3 = st.columns([1, 0.3, 1])

    for _col, _t, _score, _j, _m in [(f1, ta, score_a, ja, ma), (f3, tb, score_b, jb, mb)]:
        _r  = _j.get("rating", "SCHROTT")
        _rc = r_color.get(_r, "#8b949e")
        _is_w = (_t == winner)
        _col.markdown(
            f'<div style="background:{"#1f6feb22" if _is_w else "#161b22"};'
            f'border:{"2px solid #1f6feb" if _is_w else "1px solid #30363d"};'
            f'border-radius:10px;padding:16px;text-align:center;">'
            + (f'<div style="color:#1f6feb;font-size:0.75em;font-weight:700;">🏆 SIEGER</div>' if _is_w else "")
            + f'<div style="color:#e6edf3;font-weight:700;font-size:1.1em;">{_t}</div>'
            f'<div style="color:#1f6feb;font-weight:800;font-size:2em;">{_score:.0f}</div>'
            f'<div style="color:#8b949e;font-size:0.8em;">/ 100 JACK-Punkte</div>'
            f'<div style="color:{_rc};font-size:0.85em;margin-top:4px;">{_r}</div>'
            f'</div>',
            unsafe_allow_html=True)

    f2.markdown(
        f'<div style="text-align:center;padding-top:30px;'
        f'color:#8b949e;font-size:1.5em;">⚔️</div>',
        unsafe_allow_html=True)

    margin = abs(score_a - score_b)
    verdict_text = (
        f"**{winner}** gewinnt mit {w_score:.0f} vs {l_score:.0f} Punkten "
        f"(Vorsprung: {margin:.0f} Punkte). "
    )
    if margin < 5:
        verdict_text += "⚠️ Sehr knappes Rennen — beide sorgfältig abwägen."
    elif margin < 15:
        verdict_text += "Klarer Vorsprung in K-Kriterien und/oder Moat."
    else:
        verdict_text += "🔴 Deutlicher Qualitätsunterschied — Wahl ist klar."

    st.markdown(
        f'<div style="background:#1f6feb22;border:1px solid #1f6feb;border-radius:8px;'
        f'padding:12px 16px;margin-top:12px;">'
        f'<span style="color:#1f6feb;font-weight:700;">JACK BATTLE-URTEIL: </span>'
        f'<span style="color:#e6edf3;font-size:0.9em;">{verdict_text}</span>'
        f'</div>',
        unsafe_allow_html=True)
    st.caption("BATTLE-SCORE: Reaper (40%) + K-met/basis (30%) + Moat (20%) − Rote Flags (5%/Flag)")


# ── App Layout ────────────────────────────────────────────────────────────────
hc1, hc2 = st.columns([3, 1])
with hc1:
    st.markdown('<p class="jack-title">🛡️ JACK – THE MOAT REAPER</p>', unsafe_allow_html=True)
    st.markdown('<p class="jack-sub">Equity Exorcist · Daten via Yahoo Finance · Kein API Key nötig</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Analyse-Modus")
    modus = st.radio("Modus wählen", [
        "🔬 A: Einzelanalyse",
        "⚔️ B: Battle (A vs B)",
        "🔍 C: These-Check",
        "📰 D: Quick News Scan",
        "⚡ E: Ultra-Quick-Scan",
        "🎯 F: Decision Mode",
        "📊 Earnings-Prep",
        "🌍 Makro-Radar",
    ], label_visibility="collapsed")
    st.divider()
    st.markdown("**Legende Modi:**")
    st.caption("A: Vollanalyse (7 Schritte)\nB: Vergleich 2 Aktien\nC: These noch intakt?\nE: BIG FIVE Kurzcheck\nF: Ultra-Short Entscheid")
    st.divider()
    st.caption(f"Daten: Yahoo Finance\nKein API Key nötig\nCache: 1h\nStand: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

st.markdown("---")

# ── Makro-Radar (kein Ticker nötig) ──────────────────────────────────────────
if "Makro" in modus:
    _render_makro_radar()

# ── Battle Mode (B) ───────────────────────────────────────────────────────────
elif "Battle" in modus:
    ca, cb = st.columns(2)
    ta = ca.text_input("Ticker A", placeholder="AAPL", key="ta").strip().upper()
    tb = cb.text_input("Ticker B", placeholder="MSFT", key="tb").strip().upper()
    if st.button("⚔️ Battle starten", type="primary", use_container_width=True) and ta and tb:
        with st.spinner(f"Analysiere {ta} vs {tb}..."):
            raw_a = fetch(ta); raw_b = fetch(tb)
        if "error" in raw_a:
            st.error(f"{ta}: {raw_a['error']}")
        elif "error" in raw_b:
            st.error(f"{tb}: {raw_b['error']}")
        else:
            ma = calc_metrics(raw_a); ja = calc_jack(ma)
            mb = calc_metrics(raw_b); jb = calc_jack(mb)
            _render_battle(ta, ma, ja, tb, mb, jb)
            st.markdown("---")
            st.markdown("### Einzelanalysen")
            tab_a, tab_b = st.tabs([f"🔬 {ta} — Vollanalyse", f"🔬 {tb} — Vollanalyse"])
            with tab_a:
                render(ta, ma, ja, raw_a.get("hist", pd.DataFrame()), raw_a.get("eps_hist", pd.DataFrame()))
            with tab_b:
                render(tb, mb, jb, raw_b.get("hist", pd.DataFrame()), raw_b.get("eps_hist", pd.DataFrame()))

# ── Modi C / E / F / Earnings-Prep — Ticker-basiert ──────────────────────────
else:
    _ticker_placeholder = {
        "These": "Ticker für These-Check (z.B. NVDA)",
        "Quick": "Ticker für Quick-Scan (z.B. AAPL)",
        "Decision": "Ticker für Decision Mode (z.B. META)",
        "Earnings": "Ticker für Earnings-Prep (z.B. MSFT)",
    }
    placeholder = next((v for k, v in _ticker_placeholder.items() if k in modus),
                       "z.B.  AAPL  ·  NVDA  ·  SAP.DE  ·  ASML.AS")

    ticker_input = st.text_input(
        "Ticker eingeben",
        placeholder="AAPL · SAP.DE · US0378331005 · 865985 · Apple Inc.",
        label_visibility="collapsed",
    ).strip()

    if ticker_input:
        # ── Smart Resolver: Ticker / ISIN / WKN / Firmenname ─────────────────
        with st.spinner("Suche Ticker..."):
            resolved, resolve_label, resolve_err = resolve_input(ticker_input)

        if resolve_err:
            st.error(f"❌ {resolve_err}")
            st.info("Eingabe-Formate: Ticker (AAPL), ISIN (US0378331005), WKN (865985), Firmenname (Apple)")
            resolved = None

        if resolved:
            if resolve_label:
                st.caption(f"🔍 Aufgelöst: {resolve_label}")
            with st.spinner(f"Lade Daten für {resolved} von Yahoo Finance..."):
                raw = fetch(resolved)
            ticker_input = resolved  # verwende aufgelösten Ticker weiterhin

        if resolved and "error" in raw:
            st.error(f"❌ {raw['error']}")
            st.info("Tipp: US-Aktien ohne Kürzel (AAPL), deutsche Aktien mit .DE (SAP.DE), Schweizer mit .SW (NESN.SW)")
            resolved = None

        if resolved and "error" not in raw:
            m = calc_metrics(raw)
            j = calc_jack(m)
            hist     = raw.get("hist", pd.DataFrame())
            eps_hist = raw.get("eps_hist", pd.DataFrame())

            if "Diese" in modus:            # C: These-Check
                _render_these_check(m, j)
            elif "News" in modus:           # D: Quick News Scan
                _render_quick_news_scan(m, j)
            elif "Quick" in modus:          # E: Ultra-Quick-Scan
                _render_ultra_quick_scan(m, j)
            elif "Decision" in modus:       # F: Decision Mode
                _render_decision_mode(m, j)
            elif "Earnings" in modus:       # Earnings-Prep
                _render_earnings_prep(m, j, eps_hist)
            else:                           # A: Einzelanalyse (Standard)
                render(ticker_input, m, j, hist, eps_hist)
    else:
        st.markdown("""
<div class="welcome">
  <div style="font-size:3em;margin-bottom:12px;">🛡️</div>
  <h3 style="color:#e94560;margin:0 0 8px 0;">JACK ist bereit</h3>
  <p>Ticker eingeben und Enter drücken — kein API Key, kein Login nötig.</p>
  <p style="font-size:.83em;color:#6e7681;">
    <code>NVDA</code> &nbsp;·&nbsp; <code>AAPL</code> &nbsp;·&nbsp;
    <code>SAP.DE</code> &nbsp;·&nbsp; <code>ASML.AS</code> &nbsp;·&nbsp;
    <code>META</code> &nbsp;·&nbsp; <code>BRK-B</code>
  </p>
</div>""", unsafe_allow_html=True)
