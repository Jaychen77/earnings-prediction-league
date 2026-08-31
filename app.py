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

# Default Data
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
                    "date": "Aug 25 (Tue)",
                    "timing": "AMC (After Close)",
                    "price": 665.00,
                    "eps_est": 1.85,
                    "market_cap_b": 182.4,
                    "actual_dir": "UP",
                    "actual_pct": 3.2,
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
                    "actual_dir": "UP",
                    "actual_pct": 1.8,
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
                    "actual_dir": "DOWN",
                    "actual_pct": -6.4,
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
                    "actual_dir": "UP",
                    "actual_pct": 2.1,
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
                    "actual_dir": "DOWN",
                    "actual_pct": -14.7,
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
                    "actual_dir": "UP",
                    "actual_pct": 0.9,
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
                    "actual_dir": "UP",
                    "actual_pct": 4.3,
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
                    "actual_dir": "DOWN",
                    "actual_pct": -28.5,
                    "votes": {}
                },
                {
                    "id": "s-9",
                    "ticker": "IBIT",
                    "company": "iShares Bitcoin Trust ETF",
                    "date": "Weekly Macro / ETF",
                    "timing": "Weekly Tracker (Mon-Fri)",
                    "price": 36.50,
                    "eps_est": None,
                    "market_cap_b": 22.5,
                    "actual_dir": "DOWN",
                    "actual_pct": -4.2,
                    "votes": {}
                },
                {
                    "id": "s-10",
                    "ticker": "USO",
                    "company": "United States Oil Fund",
                    "date": "Weekly Macro / ETF",
                    "timing": "Weekly Tracker (Mon-Fri)",
                    "price": 75.20,
                    "eps_est": None,
                    "market_cap_b": 1.4,
                    "actual_dir": "DOWN",
                    "actual_pct": -1.5,
                    "votes": {}
                },
                {
                    "id": "s-11",
                    "ticker": "LOW",
                    "company": "Lowe's Companies, Inc.",
                    "date": "Weekly Stock Tracker",
                    "timing": "Weekly Tracker (Mon-Fri)",
                    "price": 242.80,
                    "eps_est": None,
                    "market_cap_b": 138.0,
                    "actual_dir": "UP",
                    "actual_pct": 1.2,
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
                    "date": "Sep 02 (Wed)",
                    "timing": "AMC (After Close)",
                    "price": 160.00,
                    "eps_est": 1.20,
                    "market_cap_b": 745.0,
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
                    "date": "Sep 01 (Tue)",
                    "timing": "BMO (Before Open)",
                    "price": 4.10,
                    "eps_est": -0.31,
                    "market_cap_b": 8.5,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w35-4",
                    "ticker": "MDB",
                    "company": "MongoDB, Inc.",
                    "date": "Sep 01 (Tue)",
                    "timing": "AMC (After Close)",
                    "price": 285.00,
                    "eps_est": 0.49,
                    "market_cap_b": 21.0,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w35-5",
                    "ticker": "GTLB",
                    "company": "GitLab Inc.",
                    "date": "Sep 01 (Tue)",
                    "timing": "AMC (After Close)",
                    "price": 48.50,
                    "eps_est": 0.10,
                    "market_cap_b": 7.8,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w35-6",
                    "ticker": "HPE",
                    "company": "Hewlett Packard Enterprise",
                    "date": "Sep 02 (Wed)",
                    "timing": "AMC (After Close)",
                    "price": 18.50,
                    "eps_est": 0.47,
                    "market_cap_b": 24.2,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w35-7",
                    "ticker": "ZS",
                    "company": "Zscaler, Inc.",
                    "date": "Sep 03 (Thu)",
                    "timing": "AMC (After Close)",
                    "price": 195.00,
                    "eps_est": 0.69,
                    "market_cap_b": 29.5,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w35-8",
                    "ticker": "DOCU",
                    "company": "DocuSign, Inc.",
                    "date": "Sep 03 (Thu)",
                    "timing": "AMC (After Close)",
                    "price": 57.00,
                    "eps_est": 0.80,
                    "market_cap_b": 11.8,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w35-9",
                    "ticker": "IBIT",
                    "company": "iShares Bitcoin Trust ETF",
                    "date": "Weekly Macro / ETF",
                    "timing": "Weekly Tracker (Mon-Fri)",
                    "price": 34.80,
                    "eps_est": None,
                    "market_cap_b": 21.5,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w35-10",
                    "ticker": "USO",
                    "company": "United States Oil Fund",
                    "date": "Weekly Macro / ETF",
                    "timing": "Weekly Tracker (Mon-Fri)",
                    "price": 74.50,
                    "eps_est": None,
                    "market_cap_b": 1.4,
                    "actual_dir": None,
                    "actual_pct": None,
                    "votes": {}
                },
                {
                    "id": "s-w35-11",
                    "ticker": "QQQ",
                    "company": "Invesco QQQ Trust ETF",
                    "date": "Weekly Macro / ETF",
                    "timing": "Weekly Tracker (Mon-Fri)",
                    "price": 475.00,
                    "eps_est": None,
                    "market_cap_b": 280.0,
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

SCHEMA_VERSION = "v4"
DATA_FILE = os.path.join(os.path.dirname(__file__), f"league_data_{SCHEMA_VERSION}.json")
SUPABASE_TABLE = "earningsbeat_state"

def _merge_defaults(saved):
    """Merge default weeks into saved data while preserving user votes & custom stock additions."""
    for def_week in DEFAULT_DATA["weeks"]:
        saved_week = next((w for w in saved.get("weeks", []) if w["id"] == def_week["id"]), None)
        if saved_week:
            # Sync metadata / name
            saved_week["name"] = def_week["name"]
            saved_week["date_range"] = def_week["date_range"]
            
            existing_stocks_by_ticker = {s["ticker"]: s for s in saved_week.get("stocks", [])}
            for def_s in def_week.get("stocks", []):
                t = def_s["ticker"]
                if t in existing_stocks_by_ticker:
                    s_curr = existing_stocks_by_ticker[t]
                    # Update company, date, timing, eps_est from defaults if missing or updated
                    s_curr["company"] = def_s.get("company", s_curr.get("company"))
                    s_curr["date"] = def_s.get("date", s_curr.get("date"))
                    s_curr["timing"] = def_s.get("timing", s_curr.get("timing"))
                    if s_curr.get("actual_dir") is None and def_s.get("actual_dir") is not None:
                        s_curr["actual_dir"] = def_s["actual_dir"]
                        s_curr["actual_pct"] = def_s.get("actual_pct")
                else:
                    saved_week.setdefault("stocks", []).append(def_s)
        else:
            saved.setdefault("weeks", []).append(def_week)
    return saved

def is_stock_locked(stock):
    """Checks if a stock has reported earnings (actual_dir present) or if 1 hour before earnings cutoff passed."""
    if stock.get("actual_dir") is not None:
        return True, "Reported (Locked)"
    
    d_str = stock.get("date", "")
    timing = stock.get("timing", "")

    # Macro/Weekly tracker cutoff: Monday 9:30 AM ET market open of the active week
    if "Weekly" in d_str or "Tracker" in timing:
        # If today is Friday after 4pm, lock week
        now = datetime.now()
        if now.weekday() >= 5 or (now.weekday() == 4 and now.hour >= 16):
            return True, "Week Closed (Locked)"
        return False, ""
    
    # Check by report date & timing for standard earnings
    months = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, 
              "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
    try:
        now = datetime.now()
        for m_name, m_num in months.items():
            if m_name in d_str.lower():
                import re
                day_matches = re.findall(r'\b(\d{1,2})\b', d_str)
                if day_matches:
                    day = int(day_matches[-1])
                    year = now.year
                    
                    # 1 hour before earnings:
                    # BMO reports at 9:00 AM ET -> Cutoff is 8:00 AM ET
                    # AMC reports at 4:00 PM ET -> Cutoff is 3:00 PM ET
                    hour = 15 if "AMC" in timing.upper() else 8
                    lock_time = datetime(year, m_num, day, hour, 0)
                    
                    if now > lock_time:
                        return True, "Cutoff Passed (1h before earnings)"
    except Exception:
        pass
        
    return False, ""


def get_supabase():
    try:
        from supabase import create_client
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception:
        return None

def load_data():
    # 1. Try Supabase
    sb = get_supabase()
    if sb:
        try:
            resp = sb.table(SUPABASE_TABLE).select("state_json").eq("id", 1).execute()
            if resp.data and len(resp.data) > 0:
                # Row found — load from Supabase
                saved = json.loads(resp.data[0]["state_json"])
                return _merge_defaults(saved)
            else:
                # Table is empty — seed it with default data right now
                seed = _merge_defaults(dict(DEFAULT_DATA))
                sb.table(SUPABASE_TABLE).upsert({
                    "id": 1,
                    "state_json": json.dumps(seed),
                    "updated_at": datetime.now().isoformat()
                }).execute()
                return seed
        except Exception as e:
            st.warning(f"⚠️ Supabase error: {e}")

    # 2. Fallback: local file
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return _merge_defaults(json.load(f))
        except Exception:
            pass

    return DEFAULT_DATA

def save_data(data):
    # Always write local backup
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

    # Save to Supabase (upsert single row with id=1)
    sb = get_supabase()
    if sb:
        try:
            state_json = json.dumps(data)
            sb.table(SUPABASE_TABLE).upsert({
                "id": 1,
                "state_json": state_json,
                "updated_at": datetime.now().isoformat()
            }).execute()
        except Exception as e:
            st.warning(f"⚠️ Supabase save error: {e}")

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
VOTE_PASSWORD = st.secrets.get("app", {}).get("passcode", "stock2026")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "data" not in st.session_state:
    st.session_state.data = load_data()
    sync_daily_stock_data(st.session_state.data)
    # Immediately populate Google Sheet with initial tables on startup
    save_data(st.session_state.data)

data = st.session_state.data

if "active_user_id" not in st.session_state:
    st.session_state.active_user_id = None

# Top Bar Header: Branding | Who Are You | Passcode
h_col1, h_col2, h_col3 = st.columns([2.2, 2.0, 1.8])
with h_col1:
    st.markdown("## 📈 Earnings**Beat**")
    st.caption("Predict stock price direction by Friday close • Mega-caps (>$50B)")

with h_col2:
    user_labels = ["— Select who you are —"] + [f"{u['avatar']} {u['name']}" for u in data["users"]]
    user_id_map = {f"{u['avatar']} {u['name']}": u['id'] for u in data["users"]}
    selected_label = st.selectbox(
        "👤 Who are you?",
        user_labels,
        index=0,
        help="Pick your name before voting"
    )
    if selected_label == "— Select who you are —":
        active_user_id = None
        st.session_state.active_user_id = None
    else:
        active_user_id = user_id_map[selected_label]
        st.session_state.active_user_id = active_user_id

with h_col3:
    if not st.session_state.authenticated:
        pass_val = st.text_input(
            "🔑 League Passcode",
            key="global_pass_key",
            placeholder="stock****",
            help="Enter passcode to enable voting"
        )
        if pass_val:
            if pass_val.strip() == VOTE_PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Unlocked!")
                st.rerun()
            else:
                st.caption("❌ Wrong passcode")
    else:
        st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)
        st.success("🔓 League Unlocked")

# Show prompt if no user selected
if active_user_id is None:
    st.error("👆 **Please select who you are** from the dropdown above to cast your predictions.")


# Protected Controls: Add Member, Add Custom Stock/ETF, & Resolve Outcomes - ONLY visible if passcode unlocked
if st.session_state.authenticated:
    c_ctrl1, c_ctrl2, c_ctrl3 = st.columns(3)
    with c_ctrl1:
        with st.expander("👤 Add Member", expanded=False):
            with st.form("add_user_form", clear_on_submit=True):
                u_col1, u_col2 = st.columns([2, 1])
                with u_col1:
                    new_friend_name = st.text_input("Display Name")
                with u_col2:
                    new_friend_avatar = st.selectbox("Avatar", ["🦁", "🚀", "🐺", "🦉", "⚡", "🎯", "💎", "🔥", "👑", "🦊", "🐻", "🦄", "🦅", "🦈"])
                
                if st.form_submit_button("➕ Add Member"):
                    if new_friend_name.strip():
                        new_user = {
                            "id": f"user-{int(datetime.now().timestamp()*1000)}",
                            "name": new_friend_name.strip(),
                            "avatar": new_friend_avatar
                        }
                        data["users"].append(new_user)
                        save_data(data)
                        st.success(f"Added {new_friend_name}!")
                        st.rerun()

    with c_ctrl2:
        with st.expander("📊 Add Ticker", expanded=False):
            with st.form("add_custom_ticker_form", clear_on_submit=True):
                new_t_input = st.text_input("Ticker (e.g. TSLA, NVDA)").upper().strip()
                t_type = st.selectbox("Category", ["Weekly Macro / ETF", "Weekly Stock Tracker", "Earnings Matchup (AMC)", "Earnings Matchup (BMO)"])
                target_w_name = st.selectbox("Target Week", [w["name"] for w in data["weeks"]])
                
                if st.form_submit_button("➕ Add Ticker"):
                    if new_t_input:
                        try:
                            t_info = yf.Ticker(new_t_input).info or {}
                            c_name = t_info.get("shortName") or t_info.get("longName") or new_t_input
                            c_price = t_info.get("currentPrice") or t_info.get("previousClose") or t_info.get("regularMarketPrice") or None
                            c_mkt_cap = t_info.get("marketCap", 0) or 0
                            c_mkt_cap_b = round(c_mkt_cap / 1e9, 1) if c_mkt_cap else 0
                            c_eps = t_info.get("forwardEps") or t_info.get("trailingEps") or None

                            target_w = next(w for w in data["weeks"] if w["name"] == target_w_name)
                            if not any(s["ticker"] == new_t_input for s in target_w.get("stocks", [])):
                                is_macro = "Macro" in t_type or "Tracker" in t_type
                                target_w.setdefault("stocks", []).append({
                                    "id": f"s-custom-{int(datetime.now().timestamp()*1000)}",
                                    "ticker": new_t_input,
                                    "company": c_name,
                                    "date": t_type if is_macro else "This Week",
                                    "timing": "Weekly Tracker (Mon-Fri)" if is_macro else ("AMC (After Close)" if "AMC" in t_type else "BMO (Before Open)"),
                                    "price": float(c_price) if c_price else None,
                                    "eps_est": float(c_eps) if (c_eps and not is_macro) else None,
                                    "market_cap_b": c_mkt_cap_b if c_mkt_cap_b else None,
                                    "actual_dir": None,
                                    "actual_pct": None,
                                    "votes": {},
                                    "notes": {}
                                })
                                save_data(data)
                                st.success(f"✅ Added {new_t_input} to {target_w['name']}!")
                                st.rerun()
                            else:
                                st.info(f"{new_t_input} is already in {target_w_name}.")
                        except Exception as e:
                            st.error(f"Error adding ticker {new_t_input}: {e}")

    with c_ctrl3:
        with st.expander("⚖️ Resolve Outcomes (Win/Loss)", expanded=False):
            res_week_names = [w["name"] for w in data["weeks"]]
            sel_res_w_name = st.selectbox("Week to Grade:", res_week_names, key="sel_res_w")
            sel_res_w = next(w for w in data["weeks"] if w["name"] == sel_res_w_name)
            
            with st.form("resolve_outcomes_form"):
                st.caption("Set official Friday outcomes to compute win/loss records:")
                res_stock_list = sel_res_w.get("stocks", [])
                temp_results = {}
                for s in res_stock_list:
                    cur_dir = s.get("actual_dir") or "None"
                    cur_pct = s.get("actual_pct") if s.get("actual_pct") is not None else 0.0
                    
                    r_c1, r_c2, r_c3 = st.columns([1.5, 2, 2])
                    with r_c1:
                        st.markdown(f"**{s['ticker']}**")
                    with r_c2:
                        dir_opts = ["None", "UP", "NEUTRAL", "DOWN"]
                        dir_idx = dir_opts.index(cur_dir) if cur_dir in dir_opts else 0
                        new_dir = st.selectbox("Dir", dir_opts, index=dir_idx, key=f"res_dir_{s['id']}", label_visibility="collapsed")
                    with r_c3:
                        new_pct = st.number_input("% Chg", value=float(cur_pct), step=0.1, format="%.1f", key=f"res_pct_{s['id']}", label_visibility="collapsed")
                    temp_results[s["id"]] = (new_dir, new_pct)
                    
                if st.form_submit_button("💾 Save Official Results"):
                    for s in res_stock_list:
                        d_val, p_val = temp_results[s["id"]]
                        s["actual_dir"] = None if d_val == "None" else d_val
                        s["actual_pct"] = p_val if d_val != "None" else None
                    save_data(data)
                    st.success("✅ Recorded official outcomes & updated leaderboard!")
                    st.rerun()

st.divider()

# Main Navigation Tabs
tab_matchups, tab_leaderboard = st.tabs([
    "📈 Price Direction Picks", 
    "🏆 Friends Leaderboard"
])

# Determine default week index dynamically based on current date
def get_current_week_index(weeks_list):
    now = datetime.now()
    cur_year, cur_week_num, _ = now.isocalendar()
    
    # 1. Match by week number string in id (e.g. week-2026-35)
    week_target_id = f"week-{cur_year}-{cur_week_num:02d}"
    for idx, w in enumerate(weeks_list):
        if w["id"] == week_target_id or f"-{cur_week_num}" in w["id"]:
            return idx
            
    # 2. Match by week title string
    for idx, w in enumerate(weeks_list):
        if f"Week {cur_week_num}" in w["name"]:
            return idx
            
    return 0

# Tab 1: Weekly Matchups & Voting
with tab_matchups:
    weeks_list = data["weeks"]
    weeks_dict = {w["name"]: w["id"] for w in weeks_list}
    default_week_idx = get_current_week_index(weeks_list)
    
    selected_week_name = st.selectbox(
        "📅 Select Week Round:", 
        list(weeks_dict.keys()), 
        index=default_week_idx
    )
    current_week = next(w for w in data["weeks"] if w["id"] == weeks_dict[selected_week_name])
    
    stocks = current_week.get("stocks", [])
    total_stocks = len(stocks)
    my_votes_count = sum(1 for s in stocks if active_user_id in s.get("votes", {}))
    
    stat_c1, stat_c2, stat_c3 = st.columns(3)
    stat_c1.metric("Total Matchups", total_stocks)
    stat_c2.metric("Your Predictions", f"{my_votes_count} / {total_stocks}")
    stat_c3.metric("Active League Members", len(data["users"]))
    
    st.caption("🏁 **Official Rule:** Votes can be changed freely until **1 hour before earnings** (3:00 PM ET for AMC / 8:00 AM ET for BMO), after which they lock permanently. Winners decided by **Friday Market Close Price** vs Pre-Earnings Price. &nbsp; 🟢 **UP** (> +0.5%) &nbsp;|&nbsp; ⚪ **NEUTRAL** (±0.5%) &nbsp;|&nbsp; 🔴 **DOWN** (< -0.5%)")
    st.divider()
    
    if not stocks:
        st.info("No stock earnings matchups added for this week yet.")
    else:
        for stock in stocks:
            votes = stock.get("votes", {})
            my_vote = votes.get(active_user_id) if active_user_id else None

            total_votes = len(votes)
            up_votes = sum(1 for v in votes.values() if v == "UP")
            down_votes = sum(1 for v in votes.values() if v == "DOWN")
            neutral_votes = sum(1 for v in votes.values() if v == "NEUTRAL")
            up_pct = int((up_votes / total_votes * 100)) if total_votes > 0 else 0

            t_badge = "🌙 After Close" if "AMC" in stock.get("timing", "") else "🌅 Before Open"
            p_str = f"${stock.get('price'):.2f}" if stock.get("price") else "—"
            eps_str = f"${stock.get('eps_est'):.2f}" if stock.get("eps_est") else "—"
            cap_str = f"${stock.get('market_cap_b', '')}B" if stock.get("market_cap_b") else ""

            # Check outcome
            actual_dir = stock.get("actual_dir")
            actual_pct = stock.get("actual_pct")

            # Friend picks chips & notes
            chips = []
            notes = stock.get("notes", {})
            for u in data["users"]:
                uid = u["id"]
                u_name = u["name"].split()[0]
                if uid in votes or uid in notes:
                    v = votes.get(uid)
                    v_icon = "🟢" if v == "UP" else ("🔴" if v == "DOWN" else ("⚪" if v == "NEUTRAL" else "⏭️"))
                    
                    # Add win/loss indicator for friends if resolved
                    res_tag = ""
                    if actual_dir and v and v != "SKIP":
                        if v == actual_dir:
                            res_tag = " <span style='color:#4ade80; font-weight:700;'>[WIN +10pts]</span>"
                        else:
                            res_tag = " <span style='color:#f87171; font-weight:700;'>[LOSS]</span>"
                            
                    u_note = f' — "{notes[uid]}"' if uid in notes and notes[uid].strip() else ""
                    chips.append(f"{u['avatar']} **{u_name}** {v_icon}{res_tag}{u_note}")

            # Vote label & My Result
            if my_vote == "UP":
                my_vote_label = "🟢 You picked UP"
            elif my_vote == "DOWN":
                my_vote_label = "🔴 You picked DOWN"
            elif my_vote == "NEUTRAL":
                my_vote_label = "⚪ You picked NEUTRAL"
            elif my_vote == "SKIP":
                my_vote_label = "⏭️ You chose to SKIP (No prediction)"
            else:
                my_vote_label = ""

            # Lock check: Can change vote freely until 1 hour before earnings cutoff
            is_locked, lock_reason = is_stock_locked(stock)
            
            # Can vote/change only if authenticated, user selected, not resolved, and cutoff hasn't passed
            can_vote = st.session_state.authenticated and bool(active_user_id) and not is_locked and actual_dir is None

            # Status badge for card
            if actual_dir:
                pct_str = f" ({actual_pct:+.1f}%)" if actual_pct is not None else ""
                dir_color = "#4ade80" if actual_dir == "UP" else ("#f87171" if actual_dir == "DOWN" else "#94a3b8")
                status_badge = f"<span style='color:{dir_color}; font-weight:800;'>🏁 Resolved: {actual_dir}{pct_str}</span>"
            elif is_locked:
                status_badge = f"<span style='color:#f87171; font-weight:700;'>🔒 {lock_reason}</span>"
            elif my_vote == "SKIP":
                status_badge = "<span style='color:#94a3b8; font-weight:600;'>⏭️ Skipped</span>"
            elif my_vote is not None:
                status_badge = "<span style='color:#38bdf8; font-weight:600;'>✏️ Pick Saved (Editable until cutoff)</span>"
            else:
                status_badge = "<span style='color:#4ade80; font-weight:600;'>🟢 Voting Open</span>"

            # Personal Win / Loss banner on card
            my_result_html = ""
            if actual_dir and my_vote:
                if my_vote == "SKIP":
                    my_result_html = "<div style='margin-top:8px; font-size:0.85rem; font-weight:700; color:#94a3b8;'>⏭️ Result: Skipped (No points scored)</div>"
                elif my_vote == actual_dir:
                    my_result_html = f"<div style='margin-top:8px; font-size:0.88rem; font-weight:800; color:#4ade80;'>🎉 WON! +10 Points (You picked {my_vote} and stock went {actual_dir})</div>"
                else:
                    my_result_html = f"<div style='margin-top:8px; font-size:0.88rem; font-weight:800; color:#f87171;'>❌ LOSS (You picked {my_vote} but stock went {actual_dir})</div>"
            elif my_vote_label:
                my_result_html = f"<div style='margin-top:8px; font-size:0.82rem; font-weight:600; color:#38bdf8;'>{my_vote_label}</div>"

            # Render comments HTML inside card
            notes_html = ""
            if chips:
                chips_lines = "<br>".join([f"<div style='margin-top:4px;'>{c}</div>" for c in chips])
                notes_html = f"<div style='margin-top:10px; padding-top:8px; border-top:1px solid #334155; font-size:0.82rem; color:#cbd5e1;'><strong>💬 Friend Picks & Thoughts:</strong><br>{chips_lines}</div>"

            is_macro_asset = "Macro" in stock.get("date", "") or "Tracker" in stock.get("timing", "") or stock.get("eps_est") is None
            stat_eps_label = "TYPE" if is_macro_asset else "EST. EPS"
            stat_eps_val = "Macro / ETF" if is_macro_asset else f"${stock.get('eps_est'):.2f}"

            st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 12px;
">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:6px;">
        <div>
            <span style="font-size:1.25rem; font-weight:800; color:#f8fafc;">{stock['ticker']}</span>
            <span style="font-size:0.8rem; color:#94a3b8; margin-left:8px;">{cap_str}</span><br>
            <span style="font-size:0.85rem; color:#cbd5e1;">{stock.get('company', stock['ticker'])}</span>
        </div>
        <div style="text-align:right;">
            <span style="font-size:0.8rem; color:#38bdf8; font-weight:600;">{stock.get('date','TBD')}</span><br>
            <span style="font-size:0.75rem; color:#94a3b8;">{t_badge}</span><br>
            <span style="font-size:0.75rem;">{status_badge}</span>
        </div>
    </div>
    <div style="display:flex; gap:20px; margin-top:10px; flex-wrap:wrap;">
        <div><span style="color:#94a3b8; font-size:0.75rem;">PRICE</span><br><span style="font-weight:700; color:#f8fafc;">{p_str}</span></div>
        <div><span style="color:#94a3b8; font-size:0.75rem;">{stat_eps_label}</span><br><span style="font-weight:700; color:#f8fafc;">{stat_eps_val}</span></div>
        <div><span style="color:#94a3b8; font-size:0.75rem;">VOTES</span><br><span style="font-weight:700; color:#f8fafc;">🟢{up_votes} ⚪{neutral_votes} 🔴{down_votes}</span></div>
    </div>
    {notes_html}
    {my_result_html}
</div>
""", unsafe_allow_html=True)

            # Vote buttons — 4 options: UP, NEU, DOWN, SKIP
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                btn_up_type = "primary" if my_vote == "UP" else "secondary"
                if st.button("🟢 UP", key=f"btn_up_{stock['id']}", disabled=not can_vote, type=btn_up_type, use_container_width=True):
                    stock.setdefault("votes", {})[active_user_id] = "UP"
                    save_data(data)
                    st.rerun()
            with b2:
                btn_neu_type = "primary" if my_vote == "NEUTRAL" else "secondary"
                if st.button("⚪ NEU", key=f"btn_neu_{stock['id']}", disabled=not can_vote, type=btn_neu_type, use_container_width=True):
                    stock.setdefault("votes", {})[active_user_id] = "NEUTRAL"
                    save_data(data)
                    st.rerun()
            with b3:
                btn_down_type = "primary" if my_vote == "DOWN" else "secondary"
                if st.button("🔴 DOWN", key=f"btn_down_{stock['id']}", disabled=not can_vote, type=btn_down_type, use_container_width=True):
                    stock.setdefault("votes", {})[active_user_id] = "DOWN"
                    save_data(data)
                    st.rerun()
            with b4:
                btn_skip_type = "primary" if my_vote == "SKIP" else "secondary"
                if st.button("⏭️ SKIP", key=f"btn_skip_{stock['id']}", disabled=not can_vote, type=btn_skip_type, use_container_width=True):
                    stock.setdefault("votes", {})[active_user_id] = "SKIP"
                    save_data(data)
                    st.rerun()

            # Thoughts & Analysis note box (Feature 1)
            if st.session_state.authenticated and active_user_id and not is_locked and actual_dir is None:
                cur_note = stock.setdefault("notes", {}).get(active_user_id, "")
                with st.expander("💬 Add Your Thought / Reason / Price Target", expanded=bool(cur_note)):
                    c_txt, c_btn = st.columns([4, 1])
                    with c_txt:
                        new_note = st.text_input(
                            "Your Commentary", 
                            value=cur_note, 
                            key=f"note_input_{stock['id']}", 
                            placeholder="e.g. Guidance will disappoint, fading into morning open...",
                            label_visibility="collapsed"
                        )
                    with c_btn:
                        if st.button("Save", key=f"save_note_{stock['id']}", use_container_width=True):
                            if new_note.strip():
                                stock["notes"][active_user_id] = new_note.strip()
                            elif active_user_id in stock["notes"]:
                                del stock["notes"][active_user_id]
                            save_data(data)
                            st.success("Saved!")
                            st.rerun()

            st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)



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
                    if pick and pick != "SKIP":
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
    
    st.caption("ℹ️ **Scoring Rule:** 1 Win (+10 pts) per correct call evaluated at **Friday 4:00 PM ET close**. Stocks you did not pick do not count as losses.")
