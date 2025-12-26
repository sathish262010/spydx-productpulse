import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from db.db_config import get_connection

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="spydX ProductPulse",
    layout="wide",
    page_icon="🕷️"
)

# ---------------- SPYDER THEME CSS ----------------
st.markdown("""
<style>
/* PRODUCT PATTERN BACKGROUND */
body {
    background-color: #020617;
    background-image:
        repeating-linear-gradient(
            45deg,
            rgba(255,255,255,0.03) 0px,
            rgba(255,255,255,0.03) 1px,
            transparent 1px,
            transparent 60px
        );
    color: #e5e7eb;
}

/* PRODUCT ICON OVERLAY */
body::before {
    content: "📱 💻 🧺 🏏 🎧 🖥️ 🧊 🛒 📺 ⌚";
    position: fixed;
    inset: 0;
    font-size: 80px;
    letter-spacing: 80px;
    line-height: 160px;
    opacity: 0.04;
    white-space: pre-wrap;
    pointer-events: none;
    z-index: 0;
}

/* MAIN CONTENT ABOVE BACKGROUND */
.block-container {
    position: relative;
    z-index: 1;
}

/* CARD */
.card {
    background: rgba(15, 23, 42, 0.95);
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.6);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 60px rgba(56,189,248,0.3);
}

/* SECTION TITLES */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #38bdf8;
    margin: 40px 0 15px;
}

/* DOWNLOAD BUTTON */
.stDownloadButton > button {
    background: linear-gradient(90deg, #38bdf8, #22c55e);
    color: #020617;
    font-weight: 700;
    border-radius: 12px;
    padding: 10px 18px;
    border: none;
    box-shadow: 0 10px 25px rgba(56,189,248,0.4);
    transition: all 0.3s ease;
}

.stDownloadButton > button:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 20px 45px rgba(34,197,94,0.5);
}
</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------
st.title("🕷️ spydX ProductPulse")
st.caption("Cyber-Style E-Commerce Intelligence Dashboard")

# ---------------- DATA ----------------
@st.cache_data
def load_inventory():
    return pd.read_sql("SELECT * FROM inventory", get_connection())

@st.cache_data
def load_category_summary():
    return pd.read_sql("SELECT * FROM category_summary", get_connection())

inventory_df = load_inventory()
category_df = load_category_summary()

# ---------------- SIDEBAR ----------------
st.sidebar.header("🎯 Category Filter")
categories = ["All"] + sorted(inventory_df["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Choose Category", categories)

# ---------------- FILTER ----------------
if selected_category != "All":
    inventory_f = inventory_df[inventory_df["category"] == selected_category]
    category_f = category_df[category_df["category"] == selected_category]
else:
    inventory_f = inventory_df
    category_f = category_df

# ---------------- KPI CARDS ----------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">📦 TOTAL PRODUCTS</div>
        <div class="metric-value">{inventory_f.shape[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">📊 TOTAL STOCK</div>
        <div class="metric-value">{inventory_f["stock_quantity"].sum()}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    avg_price = int(inventory_f["price"].mean()) if not inventory_f.empty else 0
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">💰 AVG PRICE</div>
        <div class="metric-value">₹ {avg_price}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- INVENTORY ----------------
st.markdown("<div class='section-title'>📦 Inventory Details</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.dataframe(
    inventory_f,
    use_container_width=True,
    height=420
)

st.download_button(
    label="⬇ Download Inventory Report",
    data=inventory_f.to_csv(index=False),
    file_name="inventory_report.csv",
    mime="text/csv"
)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CATEGORY ANALYTICS ----------------
st.markdown("<div class='section-title'>📊 Category Intelligence</div>", unsafe_allow_html=True)

if not category_f.empty:
    colA, colB = st.columns(2)

    with colA:
        fig1 = px.bar(
            category_f,
            x="category",
            y="avg_demand_score",
            color="category",
            color_discrete_sequence=px.colors.qualitative.Vivid,
            template="plotly_dark",
            title="Demand Signal Strength"
        )
        fig1.update_layout(
            bargap=0.5,
            bargroupgap=0.25,
            transition_duration=600
        )
        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        fig2 = px.bar(
            category_f,
            x="category",
            y="positive_share",
            color="category",
            color_discrete_sequence=px.colors.qualitative.Prism,
            template="plotly_dark",
            title="Positive Customer Signal (%)"
        )
        fig2.update_layout(
            bargap=0.5,
            bargroupgap=0.25,
            transition_duration=600
        )
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("No analytics available for selected category")
