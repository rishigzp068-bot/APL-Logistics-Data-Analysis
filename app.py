# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="APL Logistics | Late Delivery Risk",
    page_icon="🚚",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    # Change this filename only if your GitHub dataset has a different name
    try:
        df = pd.read_excel("APL_Logistics.xlsx")
    except Exception:
        try:
            df = pd.read_excel("APL_Logistics.xlsb", engine="pyxlsb")
        except Exception:
            # Fallback to EDA workbook
            df = pd.read_excel("APL_Logistics EDA .xlsx")

    return df


df = load_data()

# -----------------------------
# CLEAN COLUMN NAMES
# -----------------------------
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace("\n", " ", regex=False)
)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def find_col(possible_names):
    for name in possible_names:
        for col in df.columns:
            if col.lower().strip() == name.lower().strip():
                return col
    return None


late_col = find_col([
    "Late_delivery_risk",
    "Late Delivery Risk",
    "Late_delivery risk"
])

shipping_mode_col = find_col([
    "Shipping Mode",
    "Shipping_Mode"
])

region_col = find_col([
    "Order Region",
    "Region",
    "Order_Region"
])

market_col = find_col([
    "Market"
])

segment_col = find_col([
    "Customer Segment",
    "Customer_Segment"
])

real_days_col = find_col([
    "Days for shipping (real)",
    "Days for Shipping (Real)"
])

scheduled_days_col = find_col([
    "Days for shipment (scheduled)",
    "Days for Shipment (Scheduled)"
])

quantity_col = find_col([
    "Order Item Quantity",
    "Order_Item_Quantity"
])

profit_col = find_col([
    "Order Profit Per Order",
    "Order_Profit_Per_Order"
])

sales_col = find_col([
    "Sales per customer",
    "Sales Per Customer",
    "Order Item Total",
    "Order Item Sales"
])

discount_col = find_col([
    "Order Item Discount Rate",
    "Order Item Discount",
    "Order_Item_Discount_Rate"
])

status_col = find_col([
    "Delivery Status",
    "Delivery_Status"
])

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
if real_days_col and scheduled_days_col:
    df["Shipping Delay"] = (
        pd.to_numeric(df[real_days_col], errors="coerce")
        - pd.to_numeric(df[scheduled_days_col], errors="coerce")
    )
else:
    df["Shipping Delay"] = 0

if scheduled_days_col and quantity_col:
    scheduled = pd.to_numeric(
        df[scheduled_days_col], errors="coerce"
    ).fillna(0)

    quantity = pd.to_numeric(
        df[quantity_col], errors="coerce"
    ).fillna(0)

    df["Shipping Pressure"] = scheduled / (quantity + 1)
else:
    df["Shipping Pressure"] = 0

if quantity_col:
    quantity = pd.to_numeric(
        df[quantity_col], errors="coerce"
    ).fillna(0)

    df["High Quantity"] = np.where(quantity > 5, 1, 0)
else:
    df["High Quantity"] = 0

if profit_col:
    profit = pd.to_numeric(
        df[profit_col], errors="coerce"
    ).fillna(0)

    df["Profit Flag"] = np.where(profit > 0, 1, 0)
else:
    df["Profit Flag"] = 0

if discount_col and quantity_col:
    discount = pd.to_numeric(
        df[discount_col], errors="coerce"
    ).fillna(0)

    quantity = pd.to_numeric(
        df[quantity_col], errors="coerce"
    ).fillna(0)

    df["Discount Impact"] = discount * quantity
else:
    df["Discount Impact"] = 0

# -----------------------------
# RISK CALCULATION
# -----------------------------
if late_col:
    risk_values = pd.to_numeric(
        df[late_col], errors="coerce"
    ).fillna(0)

    # If binary late-risk field exists
    df["Risk Probability"] = risk_values

    # Handle datasets where risk is represented as 0/1
    if df["Risk Probability"].max() <= 1:
        df["Risk Probability"] = df["Risk Probability"].astype(float)
    else:
        df["Risk Probability"] = (
            df["Risk Probability"] / df["Risk Probability"].max()
        )
else:
    # Fallback risk score based on engineered operational factors
    delay_score = np.clip(df["Shipping Delay"] / 5, 0, 1)
    pressure_score = np.clip(df["Shipping Pressure"] / 5, 0, 1)
    quantity_score = df["High Quantity"]

    df["Risk Probability"] = (
        0.50 * delay_score +
        0.30 * pressure_score +
        0.20 * quantity_score
    )

df["Risk Probability"] = df["Risk Probability"].clip(0, 1)

df["Risk Category"] = pd.cut(
    df["Risk Probability"],
    bins=[-0.01, 0.33, 0.66, 1.01],
    labels=["Low", "Medium", "High"]
)

# -----------------------------
# ORDER ID
# -----------------------------
order_id_col = find_col([
    "Order Id",
    "Order ID",
    "Order_Id",
    "Order Item Id",
    "Order Item ID"
])

if order_id_col:
    df["Order ID Display"] = df[order_id_col].astype(str)
else:
    df["Order ID Display"] = np.arange(1, len(df) + 1)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🚚 APL Logistics")

st.sidebar.markdown(
    "### Risk Intelligence Dashboard"
)

st.sidebar.markdown("---")

# Shipping mode
if shipping_mode_col:
    modes = sorted(
        df[shipping_mode_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_modes = st.sidebar.multiselect(
        "Shipping Mode",
        modes,
        default=modes
    )
else:
    selected_modes = []

# Region
if region_col:
    regions = sorted(
        df[region_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_regions = st.sidebar.multiselect(
        "Region",
        regions,
        default=regions
    )
else:
    selected_regions = []

# Market
if market_col:
    markets = sorted(
        df[market_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_markets = st.sidebar.multiselect(
        "Market",
        markets,
        default=markets
    )
else:
    selected_markets = []

# Customer Segment
if segment_col:
    segments = sorted(
        df[segment_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_segments = st.sidebar.multiselect(
        "Customer Segment",
        segments,
        default=segments
    )
else:
    selected_segments = []

# Risk threshold
risk_threshold = st.sidebar.slider(
    "Risk Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.50,
    step=0.05
)

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df.copy()

if shipping_mode_col and selected_modes:
    filtered_df = filtered_df[
        filtered_df[shipping_mode_col]
        .astype(str)
        .isin(selected_modes)
    ]

if region_col and selected_regions:
    filtered_df = filtered_df[
        filtered_df[region_col]
        .astype(str)
        .isin(selected_regions)
    ]

if market_col and selected_markets:
    filtered_df = filtered_df[
        filtered_df[market_col]
        .astype(str)
        .isin(selected_markets)
    ]

if segment_col and selected_segments:
    filtered_df = filtered_df[
        filtered_df[segment_col]
        .astype(str)
        .isin(selected_segments)
    ]

# -----------------------------
# HEADER
# -----------------------------
st.title("🚚 APL Logistics")
st.subheader("Machine Learning-Based Late Delivery Risk Prediction")

st.markdown(
    """
    **Global Supply Chain Operations | Predictive Risk Intelligence Dashboard**
    
    Identify high-risk shipments early, understand major risk drivers,
    and support proactive logistics decision-making.
    """
)

st.markdown("---")

# -----------------------------
# KPI CARDS
# -----------------------------
total_orders = len(filtered_df)

if total_orders > 0:
    avg_risk = filtered_df["Risk Probability"].mean()
    high_risk = (filtered_df["Risk Category"] == "High").sum()
    medium_risk = (filtered_df["Risk Category"] == "Medium").sum()
    low_risk = (filtered_df["Risk Category"] == "Low").sum()
else:
    avg_risk = 0
    high_risk = 0
    medium_risk = 0
    low_risk = 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "📦 Total Orders",
    f"{total_orders:,}"
)

col2.metric(
    "⚠️ High Risk",
    f"{high_risk:,}"
)

col3.metric(
    "🟠 Medium Risk",
    f"{medium_risk:,}"
)

col4.metric(
    "🟢 Low Risk",
    f"{low_risk:,}"
)

col5.metric(
    "📊 Avg Risk",
    f"{avg_risk:.1%}"
)

st.markdown("---")

# -----------------------------
# RISK OVERVIEW
# -----------------------------
st.header("📊 Delay Risk Overview")

c1, c2 = st.columns(2)

with c1:
    risk_counts = (
        filtered_df["Risk Category"]
        .value_counts()
        .reindex(["Low", "Medium", "High"])
        .fillna(0)
        .reset_index()
    )

    risk_counts.columns = ["Risk Category", "Orders"]

    fig = px.bar(
        risk_counts,
        x="Risk Category",
        y="Orders",
        title="Orders by Risk Category",
        text="Orders"
    )

    fig.update_layout(
        xaxis_title="Risk Category",
        yaxis_title="Number of Orders",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

with c2:
    risk_pie = (
        filtered_df["Risk Category"]
        .value_counts()
        .reindex(["Low", "Medium", "High"])
        .fillna(0)
        .reset_index()
    )

    risk_pie.columns = ["Risk Category", "Orders"]

    fig = px.pie(
        risk_pie,
        names="Risk Category",
        values="Orders",
        title="Risk Distribution",
        hole=0.45
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# SHIPPING DELAY
# -----------------------------
st.header("⏱️ Shipping Performance")

c1, c2 = st.columns(2)

with c1:
    if len(filtered_df) > 0:
        delay_data = filtered_df.copy()

        fig = px.histogram(
            delay_data,
            x="Shipping Delay",
            nbins=30,
            title="Shipping Delay Distribution"
        )

        fig.add_vline(
            x=0,
            line_dash="dash",
            annotation_text="On Schedule"
        )

        st.plotly_chart(fig, use_container_width=True)

with c2:
    if len(filtered_df) > 0:
        fig = px.box(
            filtered_df,
            x="Risk Category",
            y="Shipping Delay",
            category_orders={
                "Risk Category": ["Low", "Medium", "High"]
            },
            title="Shipping Delay by Risk Category"
        )

        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# REGION & MODE ANALYSIS
# -----------------------------
st.header("🌎 Region & Shipping Mode Risk Analysis")

c1, c2 = st.columns(2)

with c1:
    if region_col and len(filtered_df) > 0:

        region_analysis = (
            filtered_df
            .groupby(region_col)["Risk Probability"]
            .mean()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )

        region_analysis["Risk Probability"] *= 100

        fig = px.bar(
            region_analysis,
            x="Risk Probability",
            y=region_col,
            orientation="h",
            title="Average Risk by Region",
            labels={
                "Risk Probability": "Average Risk (%)"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

with c2:
    if shipping_mode_col and len(filtered_df) > 0:

        mode_analysis = (
            filtered_df
            .groupby(shipping_mode_col)["Risk Probability"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        mode_analysis["Risk Probability"] *= 100

        fig = px.bar(
            mode_analysis,
            x=shipping_mode_col,
            y="Risk Probability",
            title="Average Risk by Shipping Mode",
            labels={
                "Risk Probability": "Average Risk (%)"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# MARKET ANALYSIS
# -----------------------------
if market_col and len(filtered_df) > 0:

    st.header("🌐 Market Risk Analysis")

    market_analysis = (
        filtered_df
        .groupby(market_col)
        .agg(
            Orders=("Risk Probability", "count"),
            Average_Risk=("Risk Probability", "mean")
        )
        .reset_index()
    )

    market_analysis["Average Risk (%)"] = (
        market_analysis["Average_Risk"] * 100
    )

    fig = px.bar(
        market_analysis,
        x=market_col,
        y="Average Risk (%)",
        text="Orders",
        title="Average Late Delivery Risk by Market"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# ORDER LEVEL RISK
# -----------------------------
st.header("🎯 Order-Level Risk Prediction")

high_risk_orders = filtered_df[
    filtered_df["Risk Probability"] >= risk_threshold
].copy()

high_risk_orders = high_risk_orders.sort_values(
    "Risk Probability",
    ascending=False
)

display_columns = [
    "Order ID Display",
    "Risk Probability",
    "Risk Category",
    "Shipping Delay",
    "Shipping Pressure"
]

if shipping_mode_col:
    display_columns.append(shipping_mode_col)

if region_col:
    display_columns.append(region_col)

if market_col:
    display_columns.append(market_col)

if segment_col:
    display_columns.append(segment_col)

display_columns = [
    col for col in display_columns
    if col in high_risk_orders.columns
]

risk_table = high_risk_orders[display_columns].copy()

risk_table["Risk Probability"] = (
    risk_table["Risk Probability"] * 100
).round(2).astype(str) + "%"

st.write(
    f"Showing **{len(risk_table):,}** orders above the selected "
    f"risk threshold of **{risk_threshold:.0%}**."
)

st.dataframe(
    risk_table,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# TOP HIGH RISK ORDERS
# -----------------------------
st.header("🚨 Top High-Risk Orders")

top_risk = filtered_df.sort_values(
    "Risk Probability",
    ascending=False
).head(10)

top_table = top_risk[
    [
        "Order ID Display",
        "Risk Probability",
        "Risk Category",
        "Shipping Delay",
        "Shipping Pressure"
    ]
].copy()

top_table["Risk Probability"] = (
    top_table["Risk Probability"] * 100
).round(2).astype(str) + "%"

st.dataframe(
    top_table,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# RISK DRIVERS
# -----------------------------
st.header("🔍 Key Risk Drivers")

driver_values = {
    "Shipping Delay": abs(
        filtered_df["Shipping Delay"].mean()
    ),
    "Shipping Pressure": abs(
        filtered_df["Shipping Pressure"].mean()
    ),
    "High Quantity Orders": (
        filtered_df["High Quantity"].mean()
    ),
    "Discount Impact": abs(
        filtered_df["Discount Impact"].mean()
    )
}

driver_df = (
    pd.DataFrame(
        list(driver_values.items()),
        columns=["Risk Driver", "Impact"]
    )
    .sort_values("Impact", ascending=False)
)

fig = px.bar(
    driver_df,
    x="Impact",
    y="Risk Driver",
    orientation="h",
    title="Operational Risk Driver Analysis"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# OPERATIONS ACTION PANEL
# -----------------------------
st.header("🛠️ Operations Action Panel")

high_count = (
    filtered_df["Risk Category"] == "High"
).sum()

if high_count > 0:

    st.warning(
        f"⚠️ **{high_count:,} high-risk orders require proactive attention.**"
    )

    st.markdown(
        """
        **Recommended actions:**

        - Prioritize high-risk shipments for operational review.
        - Monitor shipments with positive shipping delays.
        - Review regions with consistently elevated risk.
        - Evaluate shipping modes associated with higher risk.
        - Consider proactive customer communication.
        - Reallocate operational resources toward high-risk regions.
        - Monitor high-quantity and complex orders closely.
        """
    )

else:

    st.success(
        "✅ No high-risk orders detected under the current filters."
    )

# -----------------------------
# SUMMARY
# -----------------------------
st.markdown("---")

st.header("📌 Executive Summary")

if total_orders > 0:

    st.write(
        f"""
        The current selection contains **{total_orders:,} orders** with an
        average estimated late-delivery risk of **{avg_risk:.1%}**.

        **{high_risk:,} orders** are classified as high risk,
        **{medium_risk:,}** as medium risk, and
        **{low_risk:,}** as low risk.

        The dashboard enables operations teams to identify potentially
        delayed shipments early and prioritize proactive intervention.
        """
    )

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")

st.caption(
    "APL Logistics | Machine Learning-Based Late Delivery Risk Prediction "
    "| Data Analytics & Predictive Intelligence"
)
