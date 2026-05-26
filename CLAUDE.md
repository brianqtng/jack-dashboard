# JACK – The Moat Reaper Dashboard

## Projekt-Übersicht
Streamlit-basiertes Finanzanalyse-Dashboard nach dem JACK-Framework.
Analysiert Aktien auf Basis von K-Kriterien, Reaper Score, Moat-Analyse und DCF-Bewertung.

## Stack
- **Framework:** Streamlit >= 1.40.0
- **Dataquelle:** yfinance (live)
- **Charts:** Plotly
- **Sprache:** Python 3.9+
- **Hauptdatei:** `app.py` (~5500+ Zeilen)

## Deployment
- **Lokal:** `streamlit run app.py` → http://localhost:8501
- **Live-URL:** https://jack-dashboard.streamlit.app
- **GitHub:** https://github.com/brianqtng/jack-dashboard
- **Branch:** main

## Lokaler Pfad
```
/Users/brianqtng/jack_dashboard/app.py
```

## Update-Workflow (nach Änderungen)
```bash
cd /Users/brianqtng/jack_dashboard
git add app.py && git commit -m "Update" && git push
```
→ Streamlit Cloud aktualisiert automatisch in ~1-2 Minuten.

## JACK K-BASIS Modi
| Modus | Kriterien | Trigger |
|-------|-----------|---------|
| 5S Standard | ROIC/FCF/Leverage/Piotroski/EPS/SBC | Default |
| 5F Finanz | ROE/FCF/OpLev/Piotroski/EPS/SBC | Finanzsektor |
| 5SaaS | ROIC/FCF(real)/GM/RevCAGR/EPS/SBC | Tech + GM≥65% |
| 5I Infrastruktur | OpMarge/ND-EBITDA/FCF/Capex/Piotroski/SBC | Infra-Sektor |
| 5V Versorger | ROE/Div/Payout/OpMarge/ND-EBITDA/SBC | Utilities |
| 5K Sachwerte | FCF/EV-EBITDA/ND-EBITDA/ROA/Piotroski/SBC | Mining/Energy/REIT |
| 4P Piotroski | Piotroski/ROIC/FCF/ND-EBITDA/SBC | Deep Value |

## Wichtige Technische Details
- Python 3.9: keine `str | None` Syntax, keine verschachtelten f-string Quotes
- Streamlit: `width="stretch"` statt `use_container_width=True`
- FCF-Marge in K-Kriterien = **Real FCF (nach SBC)**, nicht reported FCF
- `@st.cache_data(ttl=900)` für Makro-Daten (15 Min Cache)
- `_auto_detect_k_basis()` gibt 3-Tuple zurück: (k_basis, mode_label, mode_reason)
