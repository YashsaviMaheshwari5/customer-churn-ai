import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

def show():

    st.markdown("## 📊 Model Comparison Dashboard")

    # ---------- 3D CARD CSS ----------
    st.markdown("""
    <style>
    .card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 8px 8px 20px rgba(0,0,0,0.6),
                    -4px -4px 10px rgba(255,255,255,0.05);
        transition: 0.3s;
    }
    .card:hover {
        transform: translateY(-5px) scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- LOAD DATA ----------
    df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

    df.drop("customerID", axis=1, inplace=True)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    df = pd.get_dummies(df, drop_first=True)

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # ---------- MODELS ----------
    lr = LogisticRegression(max_iter=1000)
    rf = RandomForestClassifier()

    lr.fit(X_train, y_train)
    rf.fit(X_train, y_train)

    # ---------- METRICS ----------
    models = {
        "Logistic Regression": lr,
        "Random Forest": rf
    }

    results = []

    for name, model in models.items():
        pred = model.predict(X_test)

        results.append({
            "Model": name,
            "Accuracy": accuracy_score(y_test, pred),
            "Precision": precision_score(y_test, pred),
            "Recall": recall_score(y_test, pred)
        })

    res_df = pd.DataFrame(results)

    # ---------- TOP METRICS ----------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("🏆 Best Accuracy", f"{res_df['Accuracy'].max():.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("📊 Best Precision", f"{res_df['Precision'].max():.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ---------- BAR CHART ----------
    st.markdown("### 📈 Accuracy Comparison")

    fig1 = px.bar(
        res_df,
        x="Model",
        y="Accuracy",
        color="Model",
        text_auto=True
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ---------- RADAR CHART ----------
    # st.markdown("### 🧠 Model Performance Radar")

    fig2 = go.Figure()

    for i in range(len(res_df)):
        fig2.add_trace(go.Scatterpolar(
            r=[
                res_df.loc[i, "Accuracy"],
                res_df.loc[i, "Precision"],
                res_df.loc[i, "Recall"]
            ],
            theta=["Accuracy", "Precision", "Recall"],
            fill='toself',
            name=res_df.loc[i, "Model"]
        ))

    fig2.update_layout(polar=dict(radialaxis=dict(visible=True)))

    st.plotly_chart(fig2, use_container_width=True)

    # ---------- PIE CHART ----------
    st.markdown("### 🎯 Model Share")

    fig3 = px.pie(
        res_df,
        names="Model",
        values="Accuracy",
        hole=0.5
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # ---------- TABLE ----------
    st.markdown("### 📋 Detailed Comparison")

    st.dataframe(res_df, use_container_width=True)