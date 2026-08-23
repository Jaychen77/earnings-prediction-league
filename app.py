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

# Custom Styling (Dark FinTech Aesthetics, hide sidebar)
st.markdown("""
<style>
    /* Hide Streamlit Sidebar completely */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }
    div[data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Modern FinTech Header */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 18px 24px;
        margin-bottom: 20px;
    }
    
    .stock-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: 700;
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

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                saved = json.load(f)
                # Ensure all default week stocks exist in saved
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
        except Exception:
            pass
    return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

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

data = st.session_state.data

# Top Bar Header: Voter Selector, Add User for Jay, & League Branding
h_col1, h_col2 = st.columns([3, 2])
with h_col1:
    st.markdown("## 📈 Earnings**Beat**")
    st.caption("Weekly Stock Up/Down Prediction League • Mega & Large Caps (>$50B Market Cap)")

with h_col2:
    user_options = {f"{u['avatar']} {u['name']}": u['id'] for u in data["users"]}
    selected_user_label = st.selectbox("🎯 Voting As:", list(user_options.keys()), index=0)
    active_user_id = user_options[selected_user_label]

# Commissioner Control: Add User & Add Stock (> $50B Market Cap)
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
        for stock in stocks:
            votes = stock.get("votes", {})
            my_vote = votes.get(active_user_id)
            
            total_votes = len(votes)
            up_votes = sum(1 for v in votes.values() if v == "UP")
            up_pct = int((up_votes / total_votes * 100)) if total_votes > 0 else 50
            down_pct = 100 - up_pct
            
            with st.container():
                c_info, c_consensus, c_action = st.columns([2.5, 2, 2.5])
                
                with c_info:
                    timing_str = f"({stock.get('timing', 'AMC')})"
                    cap_badge = f" • 🏛️ Cap: ${stock['market_cap_b']}B" if stock.get("market_cap_b") else ""
                    st.markdown(f"### **{stock['ticker']}** `{timing_str}`")
                    st.caption(f"{stock.get('company', stock['ticker'])}{cap_badge} • Report Date: {stock.get('date', 'TBD')}")
                    p_str = f"${stock.get('price'):.2f}" if stock.get("price") else "N/A"
                    eps_str = f"${stock.get('eps_est'):.2f}" if stock.get("eps_est") else "N/A"
                    st.write(f"💵 **Price:** {p_str} | 📊 **Est. EPS:** {eps_str}")
                
                with c_consensus:
                    st.write("**Group Consensus**")
                    st.progress(up_pct / 100)
                    st.caption(f"🟢 {up_pct}% UP ({up_votes}) | 🔴 {down_pct}% DOWN ({total_votes - up_votes})")
                    
                    chips = []
                    for u in data["users"]:
                        if u["id"] in votes:
                            v_icon = "🟢" if votes[u["id"]] == "UP" else "🔴"
                            chips.append(f"{u['avatar']} {u['name']} {v_icon}")
                    if chips:
                        st.write(" ".join(chips))
                    else:
                        st.caption("No votes submitted yet")
                
                with c_action:
                    st.write("**Cast Your Prediction**")
                    if not st.session_state.authenticated:
                        with st.popover("🔒 Unlock Voting (PIN)"):
                            pin_try = st.text_input("Enter Voting PIN", type="password", key=f"pin_{stock['id']}")
                            if st.button("Unlock", key=f"btn_unlock_{stock['id']}"):
                                if pin_try == VOTE_PASSWORD:
                                    st.session_state.authenticated = True
                                    st.success("Unlocked! You can now cast your votes.")
                                    st.rerun()
                                else:
                                    st.error("Incorrect PIN")
                    
                    b_col1, b_col2 = st.columns(2)
                    
                    with b_col1:
                        btn_up_type = "primary" if my_vote == "UP" else "secondary"
                        if st.button(f"🟢 UP", key=f"btn_up_{stock['id']}", disabled=not st.session_state.authenticated, type=btn_up_type, use_container_width=True):
                            stock.setdefault("votes", {})[active_user_id] = "UP"
                            save_data(data)
                            st.rerun()
                            
                    with b_col2:
                        btn_down_type = "primary" if my_vote == "DOWN" else "secondary"
                        if st.button(f"🔴 DOWN", key=f"btn_down_{stock['id']}", disabled=not st.session_state.authenticated, type=btn_down_type, use_container_width=True):
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
