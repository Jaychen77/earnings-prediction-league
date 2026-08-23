import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="EarningsBeat — Stock Prediction League",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark FinTech Aesthetics)
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetricValue"] {
        font-size: 26px;
        font-weight: 700;
    }
    .stock-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .badge-bullish {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: bold;
    }
    .badge-bearish {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: bold;
    }
    .podium-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = os.path.join(os.path.dirname(__file__), "league_data.json")

# Default Sample Data
DEFAULT_DATA = {
    "users": [
        {"id": "user-1", "name": "Alex M. (You)", "avatar": "🦁"},
        {"id": "user-2", "name": "Brian K.", "avatar": "🚀"},
        {"id": "user-3", "name": "Chloe T.", "avatar": "🐺"},
        {"id": "user-4", "name": "David L.", "avatar": "🦉"},
        {"id": "user-5", "name": "Emma R.", "avatar": "⚡"}
    ],
    "weeks": [
        {
            "id": "week-2026-33",
            "name": "Week 33 (Aug 17 - Aug 21, 2026)",
            "date_range": "Aug 17 - Aug 21, 2026",
            "stocks": [
                {
                    "id": "s-1",
                    "ticker": "CSCO",
                    "company": "Cisco Systems",
                    "date": "2026-08-19",
                    "timing": "AMC",
                    "price": 49.50,
                    "eps_est": 0.85,
                    "actual_dir": "UP",
                    "actual_pct": 7.2,
                    "votes": {"user-1": "UP", "user-2": "UP", "user-3": "DOWN", "user-4": "UP", "user-5": "UP"}
                },
                {
                    "id": "s-2",
                    "ticker": "WMT",
                    "company": "Walmart Inc.",
                    "date": "2026-08-20",
                    "timing": "BMO",
                    "price": 68.20,
                    "eps_est": 0.65,
                    "actual_dir": "UP",
                    "actual_pct": 6.5,
                    "votes": {"user-1": "UP", "user-2": "DOWN", "user-3": "UP", "user-4": "UP", "user-5": "DOWN"}
                },
                {
                    "id": "s-3",
                    "ticker": "TGT",
                    "company": "Target Corp",
                    "date": "2026-08-21",
                    "timing": "BMO",
                    "price": 135.00,
                    "eps_est": 2.18,
                    "actual_dir": "UP",
                    "actual_pct": 11.2,
                    "votes": {"user-1": "DOWN", "user-2": "DOWN", "user-3": "UP", "user-4": "DOWN", "user-5": "DOWN"}
                }
            ]
        },
        {
            "id": "week-2026-34",
            "name": "Week 34 (Aug 24 - Aug 28, 2026)",
            "date_range": "Aug 24 - Aug 28, 2026",
            "stocks": [
                {
                    "id": "s-4",
                    "ticker": "NVDA",
                    "company": "NVIDIA Corp",
                    "date": "2026-08-26",
                    "timing": "AMC",
                    "price": 128.50,
                    "eps_est": 0.68,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {"user-1": "UP", "user-2": "UP", "user-3": "DOWN", "user-4": "UP"}
                },
                {
                    "id": "s-5",
                    "ticker": "CRWD",
                    "company": "CrowdStrike",
                    "date": "2026-08-27",
                    "timing": "AMC",
                    "price": 265.40,
                    "eps_est": 0.98,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {"user-1": "DOWN", "user-2": "DOWN", "user-3": "DOWN", "user-5": "UP"}
                },
                {
                    "id": "s-6",
                    "ticker": "SNOW",
                    "company": "Snowflake Inc",
                    "date": "2026-08-26",
                    "timing": "AMC",
                    "price": 132.80,
                    "eps_est": 0.16,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {"user-2": "UP", "user-3": "UP", "user-4": "DOWN"}
                },
                {
                    "id": "s-7",
                    "ticker": "DELL",
                    "company": "Dell Technologies",
                    "date": "2026-08-28",
                    "timing": "AMC",
                    "price": 139.10,
                    "eps_est": 1.73,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {"user-1": "UP", "user-3": "UP", "user-5": "UP"}
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

# Load data into session state
if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# Sidebar: Active Voter & Navigation
st.sidebar.title("📈 EarningsBeat")
st.sidebar.caption("Weekly Stock Up/Down Prediction League")

user_options = {f"{u['avatar']} {u['name']}": u['id'] for u in data["users"]}
selected_user_label = st.sidebar.selectbox("Voting As:", list(user_options.keys()), index=0)
active_user_id = user_options[selected_user_label]

with st.sidebar.expander("➕ Add Friend to League"):
    with st.form("add_friend_form", clear_on_submit=True):
        new_name = st.text_input("Friend's Name")
        new_avatar = st.selectbox("Emoji Avatar", ["🦁", "🚀", "🐺", "🦉", "⚡", "🎯", "💎", "🔥"])
        if st.form_submit_button("Add Friend"):
            if new_name.strip():
                new_user_id = f"user-{len(data['users']) + 1}"
                data["users"].append({"id": new_user_id, "name": new_name.strip(), "avatar": new_avatar})
                save_data(data)
                st.session_state.data = data
                st.rerun()

# Main Tabs
tab_matchups, tab_leaderboard, tab_admin = st.tabs(["🎯 Weekly Matchups & Voting", "🏆 Friends Leaderboard", "⚙️ Manage Slates & Results"])

# Tab 1: Weekly Matchups & Voting
with tab_matchups:
    weeks_dict = {w["name"]: w["id"] for w in data["weeks"]}
    selected_week_name = st.selectbox("Select Week:", list(weeks_dict.keys()), index=len(weeks_dict)-1)
    current_week = next(w for w in data["weeks"] if w["id"] == weeks_dict[selected_week_name])
    
    # Top stats
    stocks = current_week.get("stocks", [])
    total_stocks = len(stocks)
    my_votes_count = sum(1 for s in stocks if active_user_id in s.get("votes", {}))
    resolved_count = sum(1 for s in stocks if s.get("actual_dir"))
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matchups", total_stocks)
    col2.metric("Your Predictions", f"{my_votes_count} / {total_stocks}")
    col3.metric("Resolved Outcomes", f"{resolved_count} / {total_stocks}")
    col4.metric("Active League Members", len(data["users"]))
    
    st.divider()
    
    if not stocks:
        st.info("No stock earnings matchups added for this week yet. Add one in the 'Manage Slates' tab!")
    else:
        st.subheader("Vote Up 🟢 or Down 🔴 on Upcoming Earnings")
        for stock in stocks:
            votes = stock.get("votes", {})
            my_vote = votes.get(active_user_id)
            
            # Consensus calculations
            total_votes = len(votes)
            up_votes = sum(1 for v in votes.values() if v == "UP")
            up_pct = int((up_votes / total_votes * 100)) if total_votes > 0 else 50
            down_pct = 100 - up_pct
            
            with st.container():
                c_info, c_consensus, c_action = st.columns([2.5, 2, 2.5])
                
                with c_info:
                    timing_str = f"({stock.get('timing', 'AMC')})"
                    st.markdown(f"### **{stock['ticker']}** `{timing_str}`")
                    st.caption(f"{stock['company']} • Report Date: {stock.get('date', 'TBD')}")
                    p_str = f"${stock.get('price'):.2f}" if stock.get("price") else "N/A"
                    eps_str = f"${stock.get('eps_est'):.2f}" if stock.get("eps_est") else "N/A"
                    st.write(f"💵 **Prior Price:** {p_str} | 📊 **Est. EPS:** {eps_str}")
                    
                    if stock.get("actual_dir"):
                        res_color = "🟢 Rallied (UP)" if stock["actual_dir"] == "UP" else "🔴 Dropped (DOWN)"
                        pct_str = f" ({stock.get('actual_pct'):+.1f}%)" if stock.get("actual_pct") is not None else ""
                        st.markdown(f"**Outcome:** `{res_color}{pct_str}`")
                
                with c_consensus:
                    st.write("**Group Consensus**")
                    st.progress(up_pct / 100)
                    st.caption(f"🟢 {up_pct}% UP ({up_votes}) | 🔴 {down_pct}% DOWN ({total_votes - up_votes})")
                    
                    # Display friends who voted
                    chips = []
                    for u in data["users"]:
                        if u["id"] in votes:
                            v_icon = "🟢" if votes[u["id"]] == "UP" else "🔴"
                            chips.append(f"{u['avatar']} {u['name'].split()[0]} {v_icon}")
                    if chips:
                        st.write(" ".join(chips))
                    else:
                        st.caption("No votes yet")
                
                with c_action:
                    st.write("**Cast Your Prediction**")
                    b_col1, b_col2 = st.columns(2)
                    is_resolved = stock.get("actual_dir") is not None
                    
                    with b_col1:
                        btn_up_type = "primary" if my_vote == "UP" else "secondary"
                        if st.button(f"🟢 UP", key=f"btn_up_{stock['id']}", disabled=is_resolved, type=btn_up_type, use_container_width=True):
                            stock.setdefault("votes", {})[active_user_id] = "UP"
                            save_data(data)
                            st.rerun()
                            
                    with b_col2:
                        btn_down_type = "primary" if my_vote == "DOWN" else "secondary"
                        if st.button(f"🔴 DOWN", key=f"btn_down_{stock['id']}", disabled=is_resolved, type=btn_down_type, use_container_width=True):
                            stock.setdefault("votes", {})[active_user_id] = "DOWN"
                            save_data(data)
                            st.rerun()
                
                st.divider()

# Tab 2: Leaderboard
with tab_leaderboard:
    st.subheader("🏆 League Standings & Accuracy Leaderboard")
    
    # Calculate Leaderboard
    user_stats = {u["id"]: {"user": u, "wins": 0, "losses": 0, "total": 0, "points": 0} for u in data["users"]}
    
    for w in data["weeks"]:
        for s in w.get("stocks", []):
            if s.get("actual_dir"):
                for uid, vote in s.get("votes", {}).items():
                    if uid in user_stats:
                        user_stats[uid]["total"] += 1
                        if vote == s["actual_dir"]:
                            user_stats[uid]["wins"] += 1
                            user_stats[uid]["points"] += 100
                            if s.get("actual_pct") and abs(s["actual_pct"]) >= 8:
                                user_stats[uid]["points"] += 25
                        else:
                            user_stats[uid]["losses"] += 1
    
    leaderboard_list = []
    for uid, s in user_stats.items():
        win_rate = (s["wins"] / s["total"] * 100) if s["total"] > 0 else 0.0
        leaderboard_list.append({
            "Friend": f"{s['user']['avatar']} {s['user']['name']}",
            "Points": s["points"],
            "Win Rate (%)": f"{win_rate:.1f}%",
            "Record": f"{s['wins']}W - {s['losses']}L",
            "Total Predictions": s["total"],
            "_win_rate_num": win_rate
        })
    
    leaderboard_list.sort(key=lambda x: (x["Points"], x["_win_rate_num"]), reverse=True)
    
    # Podium display for Top 3
    if len(leaderboard_list) >= 3:
        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown(f"### 👑 #1 {leaderboard_list[0]['Friend']}")
            st.metric("Points", leaderboard_list[0]['Points'], f"Win Rate: {leaderboard_list[0]['Win Rate (%)']}")
        with p2:
            st.markdown(f"### 🥈 #2 {leaderboard_list[1]['Friend']}")
            st.metric("Points", leaderboard_list[1]['Points'], f"Win Rate: {leaderboard_list[1]['Win Rate (%)']}")
        with p3:
            st.markdown(f"### 🥉 #3 {leaderboard_list[2]['Friend']}")
            st.metric("Points", leaderboard_list[2]['Points'], f"Win Rate: {leaderboard_list[2]['Win Rate (%)']}")
            
    st.divider()
    
    df_lb = pd.DataFrame(leaderboard_list).drop(columns=["_win_rate_num"])
    df_lb.index = range(1, len(df_lb) + 1)
    st.dataframe(df_lb, use_container_width=True)

# Tab 3: Admin Management (Add Stock / Resolve Outcomes)
with tab_admin:
    st.subheader("⚙️ Add Matchups & Record Actual Outcomes")
    
    c_add, c_res = st.columns(2)
    
    with c_add:
        st.markdown("### ➕ Add Stock Matchup")
        with st.form("add_stock_form", clear_on_submit=True):
            target_week_name = st.selectbox("Target Week", [w["name"] for w in data["weeks"]])
            ticker = st.text_input("Ticker Symbol (e.g. AAPL, AMZN)").upper().strip()
            company = st.text_input("Company Name (e.g. Apple Inc.)")
            timing = st.selectbox("Timing", ["AMC (After Close)", "BMO (Before Open)", "During Market"])
            report_date = st.date_input("Report Date", datetime.now()).strftime("%Y-%m-%d")
            price = st.number_input("Prior Close Price ($)", min_value=0.0, step=0.5)
            eps_est = st.number_input("Consensus EPS Estimate ($)", min_value=-50.0, max_value=100.0, step=0.05)
            
            if st.form_submit_button("Add to Weekly Slate"):
                if ticker and company:
                    target_week = next(w for w in data["weeks"] if w["name"] == target_week_name)
                    new_stock = {
                        "id": f"stock-{int(datetime.now().timestamp()*1000)}",
                        "ticker": ticker,
                        "company": company,
                        "timing": timing.split()[0],
                        "date": report_date,
                        "price": price if price > 0 else None,
                        "eps_est": eps_est if eps_est != 0 else None,
                        "actual_dir": None,
                        "actual_pct": None,
                        "votes": {}
                    }
                    target_week.setdefault("stocks", []).append(new_stock)
                    save_data(data)
                    st.success(f"Added {ticker} to {target_week_name}!")
                    st.rerun()
    
    with c_res:
        st.markdown("### ⚖️ Resolve Earnings Outcome")
        unresolved_stocks = []
        for w in data["weeks"]:
            for s in w.get("stocks", []):
                unresolved_stocks.append((f"{s['ticker']} ({w['name'].split()[0]})", s))
        
        if unresolved_stocks:
            stock_labels = [label for label, s in unresolved_stocks]
            chosen_label = st.selectbox("Select Matchup to Resolve:", stock_labels)
            chosen_stock = next(s for label, s in unresolved_stocks if label == chosen_label)
            
            with st.form("resolve_form"):
                actual_dir = st.radio("Actual Price Reaction:", ["UP (Beat / Rallied)", "DOWN (Miss / Dropped)"])
                pct_move = st.number_input("Actual % Move (e.g. +6.5 or -4.2):", step=0.1)
                
                if st.form_submit_button("Confirm & Tally Points"):
                    chosen_stock["actual_dir"] = "UP" if "UP" in actual_dir else "DOWN"
                    chosen_stock["actual_pct"] = pct_move
                    save_data(data)
                    st.success(f"Outcome saved for {chosen_stock['ticker']}!")
                    st.rerun()
        else:
            st.info("No pending matchups found.")
