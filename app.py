# tcc.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Telco Customer Churn Dashboard", layout="wide")
# --- Custom CSS Styling ---
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
        }
        .main-title {
            background-color: #636EFA;
            padding: 20px;
            border-radius: 8px;
            color: white;
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        footer {visibility: hidden;}
        
    background-color: #f4f4f4;

    </style>
""", unsafe_allow_html=True)



# Load dataset
df = pd.read_csv("cleaned_telco_churn_with_gender.csv")
df.columns = df.columns.str.strip().str.lower()

# Convert churn to numeric
df['churn_numeric'] = df['churn'].map({'Yes': 1, 'No': 0})

# Sidebar Filters
st.sidebar.title("🔍 Filter Customers")
with st.sidebar.expander("Filter Options", expanded=True):
    gender = st.multiselect("Gender", df['gender_x'].unique())
    internet = st.multiselect("Internet Service", df['internetservice'].unique())

# Apply filters
filtered_df = df.copy()
if gender:
    filtered_df = filtered_df[filtered_df['gender_x'].isin(gender)]
if internet:
    filtered_df = filtered_df[filtered_df['internetservice'].isin(internet)]

# KPIs
churn_rate = filtered_df['churn_numeric'].mean()
total_customers = filtered_df.shape[0]

st.markdown('<div class="main-title">📉 Telco Customer Churn Dashboard</div>', unsafe_allow_html=True)
kpi1, kpi2 = st.columns(2)
kpi1.metric("🔁 Churn Rate", f"{churn_rate:.2%}")
kpi2.metric("👥 Total Customers", f"{total_customers:,}")

st.markdown("---")

# 📊 Visual 1: Contract Type vs Churn
st.subheader("📊 Churn by Contract Type")
fig1 = px.histogram(filtered_df, x="contract", color="churn", barmode="group", title="Churn by Contract Type")
st.plotly_chart(fig1, use_container_width=True)

# 🕒 Tenure Distribution
st.subheader("🕒 Tenure Distribution by Churn")
fig2 = px.histogram(filtered_df, x="tenure", nbins=30, color="churn", title="Tenure Distribution")
st.plotly_chart(fig2, use_container_width=True)

# 💰 Monthly vs Total Charges
st.subheader("💰 Monthly Charges vs Total Charges")
fig3 = px.scatter(filtered_df, x="monthlycharges", y="totalcharges", color="churn", title="Charges Comparison")
st.plotly_chart(fig3, use_container_width=True)

# 🌐 Internet Service vs Churn
st.subheader("🌐 Internet Service Type vs Churn")
fig4 = px.histogram(filtered_df, x="internetservice", color="churn", barmode="group", title="Internet Service Breakdown")
st.plotly_chart(fig4, use_container_width=True)

# 🔁 Correlation Heatmap
st.subheader("📌 Correlation Heatmap (Numeric)")
corr_df = filtered_df.select_dtypes(include='number').corr()
fig5 = px.imshow(corr_df, text_auto=True, title="Correlation Heatmap")
st.plotly_chart(fig5, use_container_width=True)

# 📎 Show Data
with st.expander("📋 Show Filtered Data"):
    st.dataframe(filtered_df)

# Footer
st.markdown("---")
st.markdown("✅ Built with ❤️ by Ramya | 💼 (https://www.linkedin.com/in/ramyasadineni) | 📧 ramya@gmail.com")

