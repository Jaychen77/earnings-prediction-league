import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import yfinance as yf

# Page Configuration - Clean single-page layout without sidebar
st.set_page_config(
    page_title="EarningsBeat — Stock Prediction League",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling (Dark FinTech Aesthetics, Mobile Responsive & Touch Optimized)
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0b0f19 !important;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 85% 85%, rgba(99, 102, 241, 0.08) 0%, transparent 45%) !important;
        color: #f8fafc !important;
    }
    
    /* Hide Streamlit Sidebar completely */
    [data-testid="stSidebar"], section[data-testid="stSidebar"], div[data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* App Container Padding for Mobile */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 1100px;
    }
    
    /* Touch-Friendly Buttons */
    .stButton > button {
        border-radius: 8px !important;
        padding: 6px 10px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        min-height: 38px !important;
        transition: all 0.15s ease-in-out;
    }
    
    .stButton > button:active {
        transform: scale(0.96);
    }
    
    /* Modern FinTech Typography & Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 13px !important;
        color: #94a3b8 !important;
    }
    
    /* Selectboxes and Inputs */
    .stSelectbox div[data-baseweb="select"], .stTextInput > div > div {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border-radius: 8px;
    }
    
    /* Mobile-Specific Breakpoints */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.4rem !important;
            padding-right: 0.4rem !important;
        }
        
        /* Adjust Column Spacing on phones */
        div[data-testid="column"] {
            padding: 2px 4px !important;
        }
        
        /* Compact typography on small screens */
        h2 {
            font-size: 1.5rem !important;
        }
        
        p, span, label {
            font-size: 0.88rem !important;
        }
        
        .stButton > button {
            padding: 4px 6px !important;
            font-size: 0.85rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = os.path.join(os.path.dirname(__file__), "league_data.json")

# Default Data: Starting with Week 34
DEFAULT_DATA = {
    "users": [
        {"id": "user-1", "name": "Jay", "avatar": "🦁"},
        {"id": "user-2", "name": "Stan", "avatar": "🚀"},
        {"id": "user-3", "name": "Edwin", "avatar": "🐺"}
    ],
    "weeks": [
        {
            "id": "week-2026-34",
            "name": "Week 34 (Aug 24 - Aug 28, 2026)",
            "date_range": "Aug 24 - Aug 28, 2026",
            "stocks": [
                {
                    "id": "s-1",
                    "ticker": "INTU",
                    "company": "Intuit Inc.",
                    "date": "Aug 22 / Aug 25",
                    "timing": "AMC (After Close)",
                    "price": 665.00,
                    "eps_est": 1.85,
                    "market_cap_b": 182.4,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-2",
                    "ticker": "SNPS",
                    "company": "Synopsys, Inc.",
                    "date": "Aug 26 (Wed)",
                    "timing": "AMC (After Close)",
                    "price": 575.00,
                    "eps_est": 3.28,
                    "market_cap_b": 87.2,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-3",
                    "ticker": "NVDA",
                    "company": "NVIDIA Corporation",
                    "date": "Aug 26 (Wed)",
                    "timing": "AMC (After Close)",
                    "price": 128.50,
                    "eps_est": 0.68,
                    "market_cap_b": 3150.0,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-4",
                    "ticker": "CRWD",
                    "company": "CrowdStrike Holdings",
                    "date": "Aug 27 (Thu)",
                    "timing": "AMC (After Close)",
                    "price": 265.40,
                    "eps_est": 0.98,
                    "market_cap_b": 64.8,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-5",
                    "ticker": "SNOW",
                    "company": "Snowflake Inc",
                    "date": "Aug 27 (Thu)",
                    "timing": "AMC (After Close)",
                    "price": 132.80,
                    "eps_est": 0.16,
                    "market_cap_b": 44.5,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-6",
                    "ticker": "CRM",
                    "company": "Salesforce, Inc.",
                    "date": "Aug 28 (Wed/Thu)",
                    "timing": "AMC (After Close)",
                    "price": 260.00,
                    "eps_est": 2.35,
                    "market_cap_b": 252.1,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-7",
                    "ticker": "DELL",
                    "company": "Dell Technologies",
                    "date": "Aug 28 (Thu/Fri)",
                    "timing": "AMC (After Close)",
                    "price": 139.10,
                    "eps_est": 1.73,
                    "market_cap_b": 98.6,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-8",
                    "ticker": "PDD",
                    "company": "PDD Holdings (Temu)",
                    "date": "Aug 28 (Fri)",
                    "timing": "BMO (Before Open)",
                    "price": 142.10,
                    "eps_est": 2.73,
                    "market_cap_b": 195.4,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                }
            ]
        },
        {
            "id": "week-2026-35",
            "name": "Week 35 (Aug 31 - Sep 04, 2026)",
            "date_range": "Aug 31 - Sep 04, 2026",
            "stocks": [
                {
                    "id": "s-w35-1",
                    "ticker": "AVGO",
                    "company": "Broadcom Inc.",
                    "date": "Sep 03 (Thu)",
                    "timing": "AMC (After Close)",
                    "price": 160.50,
                    "eps_est": 1.20,
                    "market_cap_b": 750.2,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w35-2",
                    "ticker": "LULU",
                    "company": "Lululemon Athletica",
                    "date": "Sep 03 (Thu)",
                    "timing": "AMC (After Close)",
                    "price": 270.00,
                    "eps_est": 2.95,
                    "market_cap_b": 34.2,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w35-3",
                    "ticker": "NIO",
                    "company": "NIO Inc.",
                    "date": "Sep 04 (Fri)",
                    "timing": "BMO (Before Open)",
                    "price": 4.10,
                    "eps_est": -0.31,
                    "market_cap_b": 8.5,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                }
            ]
        },
        {
            "id": "week-2026-36",
            "name": "Week 36 (Sep 07 - Sep 11, 2026)",
            "date_range": "Sep 07 - Sep 11, 2026",
            "stocks": [
                {
                    "id": "s-w36-1",
                    "ticker": "ORCL",
                    "company": "Oracle Corporation",
                    "date": "Sep 09 (Wed)",
                    "timing": "AMC (After Close)",
                    "price": 140.00,
                    "eps_est": 1.33,
                    "market_cap_b": 385.0,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w36-2",
                    "ticker": "ADBE",
                    "company": "Adobe Inc.",
                    "date": "Sep 11 (Fri)",
                    "timing": "AMC (After Close)",
                    "price": 550.00,
                    "eps_est": 4.53,
                    "market_cap_b": 245.0,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w36-3",
                    "ticker": "KR",
                    "company": "Kroger Co.",
                    "date": "Sep 11 (Fri)",
                    "timing": "BMO (Before Open)",
                    "price": 52.00,
                    "eps_est": 0.91,
                    "market_cap_b": 37.5,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                }
            ]
        }
    ]
}

SCHEMA_VERSION = "v3"
DATA_FILE = os.path.join(os.path.dirname(__file__), f"league_data_{SCHEMA_VERSION}.json")
GITHUB_REPO = "Jaychen77/earnings-prediction-league"
GITHUB_PATH = f"league_data_{SCHEMA_VERSION}.json"

# --- GitHub API Persistence ---
def _merge_defaults(saved):
    """Merge any missing default stocks/weeks into saved data."""
    for def_week in DEFAULT_DATA["weeks"]:
        saved_week = next((w for w in saved.get("weeks", []) if w["id"] == def_week["id"]), None)
        if saved_week:
            existing_tickers = {s["ticker"] for s in saved_week.get("stocks", [])}
            for s in def_week.get("stocks", []):
                if s["ticker"] not in existing_tickers:
                    saved_week["stocks"].append(s)
        else:
            saved.setdefault("weeks", []).append(def_week)
    return saved

def load_data():
    # 1. Try loading from GitHub
    try:
        token = st.secrets.get("github", {}).get("token", "")
        headers = {"Accept": "application/vnd.github.v3.raw"}
        if token:
            headers["Authorization"] = f"token {token}"
        resp = __import__("requests").get(
            f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{GITHUB_PATH}",
            headers=headers, timeout=5
        )
        if resp.status_code == 200:
            saved = resp.json()
            return _merge_defaults(saved)
    except Exception:
        pass

    # 2. Fallback: local file
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return _merge_defaults(json.load(f))
        except Exception:
            pass

    return DEFAULT_DATA

def save_data(data):
    # Always write local file
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

    # Push to GitHub via API
    try:
        token = st.secrets.get("github", {}).get("token", "")
        if not token:
            return
        import requests, base64
        api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_PATH}"
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        # Get current SHA (needed for update)
        get_resp = requests.get(api_url, headers=headers, timeout=5)
        sha = get_resp.json().get("sha", "") if get_resp.status_code == 200 else ""
        content = base64.b64encode(json.dumps(data, indent=2).encode()).decode()
        payload = {
            "message": f"Auto-save: league data {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "content": content,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha
        requests.put(api_url, headers=headers, json=payload, timeout=10)
    except Exception:
        pass

@st.cache_data(ttl=86400) # Auto-refresh daily (every 24 hours)
def fetch_live_stock_data(ticker_list):
    results = {}
    for ticker in ticker_list:
        try:
            t_obj = yf.Ticker(ticker)
            info = t_obj.info or {}
            p = info.get("currentPrice") or info.get("previousClose") or info.get("regularMarketPrice")
            eps = info.get("forwardEps") or info.get("trailingEps")
            mkt_cap = info.get("marketCap", 0) or 0
            results[ticker] = {
                "name": info.get("shortName") or info.get("longName") or ticker,
                "price": float(p) if p else None,
                "eps_est": float(eps) if eps else None,
                "market_cap": float(mkt_cap),
                "market_cap_b": round(mkt_cap / 1e9, 1) if mkt_cap else 0
            }
        except Exception:
            results[ticker] = {"name": ticker, "price": None, "eps_est": None, "market_cap": 0, "market_cap_b": 0}
    return results

def sync_daily_stock_data(data):
    # Collect all tickers across weeks
    all_tickers = list({s["ticker"] for w in data.get("weeks", []) for s in w.get("stocks", [])})
    if all_tickers:
        live_info = fetch_live_stock_data(tuple(all_tickers))
        updated = False
        for w in data.get("weeks", []):
            for s in w.get("stocks", []):
                t_data = live_info.get(s["ticker"], {})
                if t_data.get("price") and s.get("price") != t_data["price"]:
                    s["price"] = t_data["price"]
                    updated = True
                if t_data.get("eps_est") and s.get("eps_est") != t_data["eps_est"]:
                    s["eps_est"] = t_data["eps_est"]
                    updated = True
                if t_data.get("market_cap_b"):
                    s["market_cap_b"] = t_data["market_cap_b"]
        if updated:
            save_data(data)

# Vote Authentication Password
VOTE_PASSWORD = "stock2026"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "data" not in st.session_state:
    st.session_state.data = load_data()
    sync_daily_stock_data(st.session_state.data)
    # Immediately populate Google Sheet with initial tables on startup
    save_data(st.session_state.data)

data = st.session_state.data

# Top Bar Header: Voter Selector, Add User for Jay, & League Branding
h_col1, h_col2, h_col3 = st.columns([2.5, 1.8, 1.7])
with h_col1:
    st.markdown("## 📈 Earnings**Beat**")
    st.caption("Weekly Stock Up/Down Prediction League (>$50B Cap)")

with h_col2:
    user_options = {f"{u['avatar']} {u['name']}": u['id'] for u in data["users"]}
    selected_user_label = st.selectbox("🎯 Voting As:", list(user_options.keys()), index=0)
    active_user_id = user_options[selected_user_label]

with h_col3:
    if not st.session_state.authenticated:
        pass_val = st.text_input("🔑 Passcode to Unlock", key="global_pass_key", placeholder="e.g. stock****")
        if pass_val:
            if pass_val.strip() == VOTE_PASSWORD:
                st.session_state.authenticated = True
                st.success("Unlocked!")
                st.rerun()
            else:
                st.caption("❌ Invalid passcode")
    else:
        st.write("")
        st.caption("🔓 **League Unlocked**")

# Protected Controls: Add User & Add Stock (> $50B Market Cap) - ONLY visible if passcode unlocked
if st.session_state.authenticated:
    c_bar1, c_bar2 = st.columns(2)
    with c_bar1:
        with st.expander("👤 Add Member to League", expanded=False):
            with st.form("add_user_form", clear_on_submit=True):
                u_col1, u_col2 = st.columns([2, 1])
                with u_col1:
                    new_friend_name = st.text_input("Friend's Display Name")
                with u_col2:
                    new_friend_avatar = st.selectbox("Avatar Icon", ["🦁", "🚀", "🐺", "🦉", "⚡", "🎯", "💎", "🔥", "👑", "🦊", "🐻", "🦄", "🦅", "🦈"])
                
                if st.form_submit_button("➕ Add to League"):
                    if new_friend_name.strip():
                        new_user = {
                            "id": f"user-{int(datetime.now().timestamp()*1000)}",
                            "name": new_friend_name.strip(),
                            "avatar": new_friend_avatar
                        }
                        data["users"].append(new_user)
                        save_data(data)
                        st.success(f"Added {new_friend_name} to the league!")
                        st.rerun()

    with c_bar2:
        with st.expander("🔍 Add Stock Matchup (> $50B Cap)", expanded=False):
            with st.form("add_stock_cap_form", clear_on_submit=True):
                t_input = st.text_input("Ticker Symbol (e.g. AMD, BABA, AVGO, COST)").upper().strip()
                timing_input = st.selectbox("Earnings Timing", ["AMC (After Close)", "BMO (Before Open)"])
                
                if st.form_submit_button("➕ Check & Add (> $50B)"):
                    if t_input:
                        try:
                            ticker_info = yf.Ticker(t_input).info or {}
                            mkt_cap = ticker_info.get("marketCap", 0) or 0
                            mkt_cap_b = round(mkt_cap / 1e9, 1)
                            
                            if mkt_cap_b >= 50.0:
                                comp_name = ticker_info.get("shortName") or ticker_info.get("longName") or t_input
                                cur_price = ticker_info.get("currentPrice") or ticker_info.get("previousClose") or ticker_info.get("regularMarketPrice") or 0.0
                                eps = ticker_info.get("forwardEps") or ticker_info.get("trailingEps") or None
                                
                                # Add to active week
                                active_week = data["weeks"][0]
                                if not any(s["ticker"] == t_input for s in active_week.get("stocks", [])):
                                    active_week.setdefault("stocks", []).append({
                                        "id": f"stock-{int(datetime.now().timestamp()*1000)}",
                                        "ticker": t_input,
                                        "company": comp_name,
                                        "timing": timing_input,
                                        "date": "Next Week",
                                        "price": float(cur_price) if cur_price else None,
                                        "eps_est": float(eps) if eps else None,
                                        "market_cap_b": mkt_cap_b,
                                        "actual_dir": None,
                                        "actual_pct": None,
                                        "votes": {}
                                    })
                                    save_data(data)
                                    st.success(f"✅ Added {t_input} ({comp_name}) — Market Cap: ${mkt_cap_b}B (Over $50B)!")
                                    st.rerun()
                                else:
                                    st.info(f"{t_input} is already in the lineup.")
                            else:
                                st.error(f"❌ {t_input} Market Cap is ${mkt_cap_b}B. Only stocks > $50B qualify!")
                        except Exception as e:
                            st.error(f"Error fetching ticker {t_input}: {e}")

st.divider()

# Main Navigation Tabs
tab_matchups, tab_leaderboard = st.tabs([
    "🎯 Weekly Matchups & Voting", 
    "🏆 Friends Leaderboard"
])

# Tab 1: Weekly Matchups & Voting
with tab_matchups:
    weeks_dict = {w["name"]: w["id"] for w in data["weeks"]}
    selected_week_name = st.selectbox("📅 Select Week Round:", list(weeks_dict.keys()), index=0)
    current_week = next(w for w in data["weeks"] if w["id"] == weeks_dict[selected_week_name])
    
    stocks = current_week.get("stocks", [])
    total_stocks = len(stocks)
    my_votes_count = sum(1 for s in stocks if active_user_id in s.get("votes", {}))
    
    stat_c1, stat_c2, stat_c3 = st.columns(3)
    stat_c1.metric("Total Matchups", total_stocks)
    stat_c2.metric("Your Predictions", f"{my_votes_count} / {total_stocks}")
    stat_c3.metric("Active League Members", len(data["users"]))
    
    st.divider()
    
    if not stocks:
        st.info("No stock earnings matchups added for this week yet.")
    else:
        # Table Header
        h_ticker, h_date, h_price, h_cons, h_pick = st.columns([1.8, 1.4, 1.4, 2.8, 2.6])
        with h_ticker:
            st.markdown("**Ticker & Company**")
        with h_date:
            st.markdown("**Date & Time**")
        with h_price:
            st.markdown("**Price & Est.**")
        with h_cons:
            st.markdown("**Consensus & Votes**")
        with h_pick:
            st.markdown("**Your Pick (PIN Unlocked)**" if st.session_state.authenticated else "**Your Pick**")
        
        st.divider()
        
        # Table Rows
        for stock in stocks:
            votes = stock.get("votes", {})
            my_vote = votes.get(active_user_id)
            
            total_votes = len(votes)
            up_votes = sum(1 for v in votes.values() if v == "UP")
            down_votes = sum(1 for v in votes.values() if v == "DOWN")
            neutral_votes = sum(1 for v in votes.values() if v == "NEUTRAL")
            
            up_pct = int((up_votes / total_votes * 100)) if total_votes > 0 else 33
            down_pct = int((down_votes / total_votes * 100)) if total_votes > 0 else 33
            neutral_pct = 100 - up_pct - down_pct if total_votes > 0 else 34
            
            row_c1, row_c2, row_c3, row_c4, row_c5 = st.columns([1.8, 1.4, 1.4, 2.8, 2.6])
            
            with row_c1:
                cap_str = f" • ${stock['market_cap_b']}B" if stock.get("market_cap_b") else ""
                st.markdown(f"**{stock['ticker']}** <span style='font-size:0.75rem; color:#94a3b8;'>{cap_str}</span>", unsafe_allow_html=True)
                st.caption(f"{stock.get('company', stock['ticker'])[:20]}")
            
            with row_c2:
                st.write(f"**{stock.get('date', 'TBD')}**")
                t_badge = "AMC" if "AMC" in stock.get('timing', 'AMC') else "BMO"
                st.caption(f"`{t_badge}`")
                
            with row_c3:
                p_str = f"${stock.get('price'):.2f}" if stock.get("price") else "N/A"
                eps_str = f"${stock.get('eps_est'):.2f}" if stock.get("eps_est") else "N/A"
                st.write(f"**{p_str}**")
                st.caption(f"EPS: {eps_str}")
            
            with row_c4:
                st.progress(up_pct / 100)
                st.caption(f"🟢 {up_votes} | ⚪ {neutral_votes} | 🔴 {down_votes}")
                chips = []
                for u in data["users"]:
                    if u["id"] in votes:
                        v = votes[u["id"]]
                        v_icon = "🟢" if v == "UP" else ("🔴" if v == "DOWN" else "⚪")
                        chips.append(f"{u['avatar']} {u['name'].split()[0]} {v_icon}")
                if chips:
                    st.caption(" ".join(chips))
            
            with row_c5:
                b1, b2, b3 = st.columns(3)
                with b1:
                    btn_up_type = "primary" if my_vote == "UP" else "secondary"
                    if st.button("🟢", key=f"btn_up_{stock['id']}", disabled=not st.session_state.authenticated, type=btn_up_type, use_container_width=True):
                        stock.setdefault("votes", {})[active_user_id] = "UP"
                        save_data(data)
                        st.rerun()
                with b2:
                    btn_neu_type = "primary" if my_vote == "NEUTRAL" else "secondary"
                    if st.button("⚪", key=f"btn_neu_{stock['id']}", disabled=not st.session_state.authenticated, type=btn_neu_type, use_container_width=True):
                        stock.setdefault("votes", {})[active_user_id] = "NEUTRAL"
                        save_data(data)
                        st.rerun()
                with b3:
                    btn_down_type = "primary" if my_vote == "DOWN" else "secondary"
                    if st.button("🔴", key=f"btn_down_{stock['id']}", disabled=not st.session_state.authenticated, type=btn_down_type, use_container_width=True):
                        stock.setdefault("votes", {})[active_user_id] = "DOWN"
                        save_data(data)
                        st.rerun()
            
            st.divider()

# Tab 2: Leaderboard
with tab_leaderboard:
    st.subheader("🏆 League Standings & Scorecard")
    
    scores = {u["id"]: {"name": u["name"], "avatar": u["avatar"], "wins": 0, "losses": 0, "total": 0} for u in data["users"]}
    
    for w in data["weeks"]:
        for s in w.get("stocks", []):
            actual = s.get("actual_dir")
            if actual:
                for uid in scores.keys():
                    pick = s.get("votes", {}).get(uid)
                    if pick:
                        scores[uid]["total"] += 1
                        if pick == actual:
                            scores[uid]["wins"] += 1
                        else:
                            scores[uid]["losses"] += 1
                            
    leaderboard_list = []
    for uid, stats in scores.items():
        total = stats["total"]
        wins = stats["wins"]
        win_rate = (wins / total * 100) if total > 0 else 0.0
        points = wins * 10
        leaderboard_list.append({
            "Player": f"{stats['avatar']} {stats['name']}",
            "Points": f"{points} pts",
            "Win Rate": f"{win_rate:.1f}%",
            "Record (W-L)": f"{wins}W - {stats['losses']}L",
            "_points_num": points,
            "_win_rate_num": win_rate
        })
    
    leaderboard_list.sort(key=lambda x: (x["_points_num"], x["_win_rate_num"]), reverse=True)
    
    df_lb = pd.DataFrame(leaderboard_list).drop(columns=["_points_num", "_win_rate_num"])
    df_lb.index = range(1, len(df_lb) + 1)
    st.dataframe(df_lb, use_container_width=True)
