import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Churn Risk Dashboard", page_icon="📊", layout="wide")

# ---- Custom CSS for background and styling ----
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        color: #f0f0f0;
    }
    div[data-testid="stMetric"] {
        background-color: #2d2d44;
        border: 1px solid #44445a;
        padding: 15px;
        border-radius: 12px;
    }
    section[data-testid="stSidebar"] {
        background-color: #16161f;
    }
    h1, h2, h3 {
        color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

conn = sqlite3.connect("ecommerce.db")

# ---- Sidebar ----
st.sidebar.title("🔎 Filters")
risk_filter = st.sidebar.selectbox("Filter by risk level", ["All", "High", "Medium", "Low"])
st.sidebar.markdown("---")
st.sidebar.caption("E-Commerce Churn Analytics Project")
st.sidebar.caption("Built with Python, SQL, ML & Streamlit")

# ---- Load data ----
data = pd.read_sql("SELECT * FROM customers", conn)
if risk_filter != "All":
    data = data[data["churn_risk"] == risk_filter]

high_risk_spend = data[data["churn_risk"] == "High"]["total_spend"].sum()

# ---- Title ----
st.title("📊 E-Commerce Customer Churn Risk Dashboard")
st.write("Identifying customers at risk of churning, so the business can act before losing them.")

# ---- Tabs ----
tab1, tab2, tab3 = st.tabs(["📊 Overview", "⚠️ At-Risk Customers", "✉️ Retention & Predictions"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", len(data))
    col2.metric("High Risk Customers", len(data[data["churn_risk"] == "High"]))
    col3.metric("Revenue at Risk", f"£{high_risk_spend:,.0f}")
    st.caption("Revenue at Risk = total spend from customers currently flagged High risk.")

    fig = px.pie(data, names="churn_risk", title="Customer Risk Distribution", hole=0.4,
                 color="churn_risk",
                 color_discrete_map={"High": "#e74c3c", "Medium": "#f39c12", "Low": "#2ecc71"})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#f0f0f0")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Customers Most Likely to Churn")
    st.dataframe(
        data[data["churn_risk"] == "High"].sort_values("total_spend", ascending=False),
        use_container_width=True
    )

with tab3:
    st.subheader("🤖 ML Model: Predicted Churn Probability")
    data_sorted = data.sort_values("churn_probability", ascending=False)
    st.dataframe(
        data_sorted[["Customer ID", "frequency", "total_spend", "churn_probability", "churn_risk"]].head(20),
        use_container_width=True
    )

    st.subheader("✉️ Suggested Retention Message")
    high_risk_customers = data[data["churn_risk"] == "High"]["Customer ID"]
    if len(high_risk_customers) > 0:
        selected_id = st.selectbox("Select a high-risk customer", high_risk_customers)
        st.info(f"Hi Customer {int(selected_id)}, we miss you! Here's 10% off your next order.")
    else:
        st.write("No high-risk customers in current filter.")