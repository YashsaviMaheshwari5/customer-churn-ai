import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def show():

    # ---------- LOAD DATA ----------
    df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    # ---------- HEADER ----------
    st.markdown("## 📊 Admin Dashboard")

    # ---------- KPI CARDS ----------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Customers", len(df), "+12%")
    col2.metric("⚠️ Churn Rate", f"{df['Churn'].mean()*100:.1f}%", "-2%")
    col3.metric("💰 Avg Charges", f"${df['MonthlyCharges'].mean():.0f}", "+5%")
    col4.metric("📅 Avg Tenure", f"{df['tenure'].mean():.0f}", "+3%")

    st.divider()

    # ---------- MAIN CHART ----------
    col1, col2 = st.columns([2,1])

    with col1:

        st.markdown("### 📈 Customer Trends")

        # Create grouped data
        trend = df.groupby("tenure")["MonthlyCharges"].mean().reset_index()

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=trend["tenure"],
            y=trend["MonthlyCharges"],
            name="Charges",
            opacity=0.6
        ))

        fig.add_trace(go.Scatter(
            x=trend["tenure"],
            y=trend["MonthlyCharges"],
            mode='lines+markers',
            name="Trend"
        ))

        fig.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=30, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

    # ---------- DONUT CHART ----------
    with col2:

        st.markdown("### 🎯 Churn Overview")

        fig2 = px.pie(
            df,
            names="Churn",
            hole=0.6
        )

        fig2.update_layout(height=400)

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ---------- BOTTOM STATS ----------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💵 Total Revenue", f"${df['MonthlyCharges'].sum():,.0f}", "+14%")
    col2.metric("📉 Churn Count", df["Churn"].sum(), "-8%")
    col3.metric("📊 Retention", f"{(1-df['Churn'].mean())*100:.1f}%", "+15%")
    col4.metric("📦 Plans Active", len(df)-df["Churn"].sum(), "+7%")

    st.divider()

    # ---------- PROGRESS SECTION ----------
    st.markdown("### 🎯 Targets")

    st.progress(0.71, text="Revenue Target 71%")
    st.progress(0.54, text="Expenses Target 54%")
    st.progress(0.32, text="Spending Target 32%")
    st.progress(0.89, text="Growth Target 89%")