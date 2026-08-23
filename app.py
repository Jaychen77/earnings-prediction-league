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

# Fixed default users (Jay, Stan, Edwin only - adding new users disabled)
DEFAULT_DATA = {
    "users": [
        {"id": "user-1", "name": "Jay", "avatar": "🦁"},
        {"id": "user-2", "name": "Stan", "avatar": "🚀"},
        {"id": "user-3", "name": "Edwin", "avatar": "🐺"}
    ],
    "weeks": [
        {
            "id": "week-current",
            "name": "Week of " + datetime.now().strftime("%b %d, %Y"),
            "date_range": datetime.now().strftime("%b %d, %Y"),
            "stocks": [
                {
                    "id": "s-1",
                    "ticker": "NVDA",
                    "company": "NVIDIA Corporation",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "timing": "AMC",
                    "price": 128.50,
                    "eps_est": 0.68,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-2",
                    "ticker": "CRWD",
                    "company": "CrowdStrike Holdings",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "timing": "AMC",
                    "price": 265.40,
                    "eps_est": 0.98,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-3",
                    "ticker": "SNOW",
                    "company": "Snowflake Inc",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "timing": "AMC",
                    "price": 132.80,
                    "eps_est": 0.16,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-4",
                    "ticker": "DELL",
                    "company": "Dell Technologies",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "timing": "AMC",
                    "price": 139.10,
                    "eps_est": 1.73,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                }
            ]
        }
    ]
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# Top Bar Header: Voter Selector, Add User for Jay, & League Branding
h_col1, h_col2 = st.columns([3, 2])
with h_col1:
    st.markdown("## 📈 Earnings**Beat**")
    st.caption("Weekly Stock Up/Down Prediction League")

with h_col2:
    user_options = {f"{u['avatar']} {u['name']}": u['id'] for u in data["users"]}
    selected_user_label = st.selectbox("🎯 Voting As:", list(user_options.keys()), index=0)
    active_user_id = user_options[selected_user_label]

# Only You Can Add Users
with st.expander("👤 Add New Friend to League (Commissioner)", expanded=False):
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

st.divider()

# Main Navigation Tabs
tab_matchups, tab_leaderboard = st.tabs([
    "🎯 Weekly Matchups & Voting", 
    "🏆 Friends Leaderboard"
])

# Tab 1: Weekly Matchups & Voting
with tab_matchups:
    top_c1, top_c2 = st.columns([3, 1])
    with top_c1:
        weeks_dict = {w["name"]: w["id"] for w in data["weeks"]}
        selected_week_name = st.selectbox("📅 Select Week Round:", list(weeks_dict.keys()), index=0)
        current_week = next(w for w in data["weeks"] if w["id"] == weeks_dict[selected_week_name])
    with top_c2:
        st.write("")
        st.write("")
        if st.button("🔄 Auto-Update via yfinance", use_container_width=True):
            with st.spinner("Fetching live stock prices and EPS estimates..."):
                for stock in current_week.get("stocks", []):
                    try:
                        t_obj = yf.Ticker(stock["ticker"])
                        info = t_obj.info or {}
                        p = info.get("currentPrice") or info.get("previousClose") or info.get("regularMarketPrice")
                        eps = info.get("forwardEps") or info.get("trailingEps")
                        if p:
                            stock["price"] = float(p)
                        if eps:
                            stock["eps_est"] = float(eps)
                    except Exception:
                        pass
                save_data(data)
                st.success("Updated live market data!")
                st.rerun()
    
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
                    st.markdown(f"### **{stock['ticker']}** `{timing_str}`")
                    st.caption(f"{stock.get('company', stock['ticker'])} • Report Date: {stock.get('date', 'TBD')}")
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
                    b_col1, b_col2 = st.columns(2)
                    
                    with b_col1:
                        btn_up_type = "primary" if my_vote == "UP" else "secondary"
                        if st.button(f"🟢 UP", key=f"btn_up_{stock['id']}", type=btn_up_type, use_container_width=True):
                            stock.setdefault("votes", {})[active_user_id] = "UP"
                            save_data(data)
                            st.rerun()
                            
                    with b_col2:
                        btn_down_type = "primary" if my_vote == "DOWN" else "secondary"
                        if st.button(f"🔴 DOWN", key=f"btn_down_{stock['id']}", type=btn_down_type, use_container_width=True):
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
