# import streamlit as st
# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# import plotly.graph_objects as go
# import plotly.express as px

# def show():

#     st.markdown("## 🎯 Prediction Scorecard")

#     # ---------- LOAD DATA ----------
#     df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

#     df.drop("customerID", axis=1, inplace=True)
#     df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
#     df.dropna(inplace=True)
#     df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
#     df = pd.get_dummies(df, drop_first=True)

#     X = df.drop("Churn", axis=1)
#     y = df["Churn"]

#     model = RandomForestClassifier()
#     model.fit(X, y)

#     # ---------- INPUT ----------
#     st.markdown("### 🧾 Enter Customer Details")

#     col1, col2 = st.columns(2)

#     with col1:
#         tenure = st.slider("Tenure", 0, 72, 12)
#         monthly = st.number_input("Monthly Charges", value=50.0)

#     with col2:
#         contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])

#     # ---------- PREDICTION ----------
#     if st.button("🚀 Predict"):

#         input_data = X.iloc[[0]].copy()
#         input_data["tenure"] = tenure
#         input_data["MonthlyCharges"] = monthly
#         input_data["Contract_One year"] = 1 if contract == "One year" else 0
#         input_data["Contract_Two year"] = 1 if contract == "Two year" else 0

#         pred = model.predict(input_data)[0]
#         prob = model.predict_proba(input_data)[0][1]

#         st.markdown("## ✅ Your prediction quality is great!")

#         # ---------- LAYOUT ----------
#         col1, col2, col3 = st.columns([2,2,2])

#         # ---------- GAUGE ----------
#         with col1:
#             fig = go.Figure(go.Indicator(
#                 mode="gauge+number",
#                 value=prob * 100,
#                 title={'text': "Churn Risk (%)"},
#                 gauge={
#                     'axis': {'range': [0, 100]},
#                     'bar': {'color': "red" if pred==1 else "green"},
#                     'steps': [
#                         {'range': [0, 40], 'color': "green"},
#                         {'range': [40, 70], 'color': "yellow"},
#                         {'range': [70, 100], 'color': "red"}
#                     ]
#                 }
#             ))

#             st.plotly_chart(fig, use_container_width=True)

#         # ---------- ABOUT PREDICTION ----------
#         with col2:
#             st.markdown("### 📋 About Your Prediction")

#             st.write(f"**Tenure:** {tenure}")
#             st.write(f"**Monthly Charges:** {monthly}")
#             st.write(f"**Contract Type:** {contract}")

#             result = "CHURN" if pred == 1 else "STAY"
#             st.write(f"**Prediction:** {result}")

#         # ---------- TOP FEATURES ----------
#         with col3:
#             st.markdown("### 📊 Top Predictors")

#             importance = model.feature_importances_

#             feat_df = pd.DataFrame({
#                 "Feature": X.columns,
#                 "Importance": importance
#             }).sort_values(by="Importance", ascending=False).head(5)

#             fig2 = px.bar(
#                 feat_df,
#                 x="Importance",
#                 y="Feature",
#                 orientation='h'
#             )

#             st.plotly_chart(fig2, use_container_width=True)

#         st.divider()

#         # ---------- FINAL RESULT ----------
#         if pred == 1:
#             st.error(f"⚠️ Customer likely to CHURN ({prob:.2f})")
#         else:
#             st.success(f"✅ Customer likely to STAY ({1-prob:.2f})")


import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.model_loader import load_model

def show():

    st.markdown("## 🎯 Prediction Scorecard")

    # ---------- LOAD MODEL ----------
    model = load_model()

    # ---------- LOAD DATA (ONLY FOR FEATURE NAMES) ----------
    df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

    df.drop("customerID", axis=1, inplace=True)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    df = pd.get_dummies(df, drop_first=True)

    X = df.drop("Churn", axis=1)

    # ---------- INPUT ----------
    st.markdown("### 🧾 Enter Customer Details")

    col1, col2 = st.columns(2)

    with col1:
        tenure = st.slider("Tenure", 0, 72, 12)
        monthly = st.number_input("Monthly Charges", value=50.0)

    with col2:
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])

    # ---------- PREDICTION ----------
    if st.button("🚀 Predict"):

        # Create empty input
        input_data = pd.DataFrame([np.zeros(len(X.columns))], columns=X.columns)

        # Fill values
        input_data["tenure"] = tenure
        input_data["MonthlyCharges"] = monthly

        # Reset contract columns
        input_data["Contract_One year"] = 0
        input_data["Contract_Two year"] = 0

        if contract == "One year":
            input_data["Contract_One year"] = 1
        elif contract == "Two year":
            input_data["Contract_Two year"] = 1

        # ---------- PREDICT ----------
        pred = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1]

        result_text = "CHURN" if pred == 1 else "STAY"

        # 🔥 STORE FOR CHATBOT
        st.session_state.last_features = input_data.values.flatten().tolist()
        st.session_state.last_prediction = f"{result_text} ({prob*100:.2f}%)"

        # ---------- UI ----------
        st.markdown("## 📊 Prediction Result")

        col1, col2, col3 = st.columns([2,2,2])

        # ---------- GAUGE ----------
        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                title={'text': "Churn Risk (%)"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "red" if pred==1 else "green"},
                    'steps': [
                        {'range': [0, 40], 'color': "green"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "red"}
                    ]
                }
            ))

            st.plotly_chart(fig, use_container_width=True)

        # ---------- DETAILS ----------
        with col2:
            st.markdown("### 📋 Customer Summary")

            st.write(f"**Tenure:** {tenure}")
            st.write(f"**Monthly Charges:** {monthly}")
            st.write(f"**Contract:** {contract}")
            st.write(f"**Prediction:** {result_text}")

        # ---------- FEATURE IMPORTANCE ----------
        with col3:
            st.markdown("### 📊 Top Predictors")

            try:
                importance = model.feature_importances_

                feat_df = pd.DataFrame({
                    "Feature": X.columns,
                    "Importance": importance
                }).sort_values(by="Importance", ascending=False).head(5)

                fig2 = px.bar(
                    feat_df,
                    x="Importance",
                    y="Feature",
                    orientation='h'
                )

                st.plotly_chart(fig2, use_container_width=True)

            except:
                st.warning("Feature importance not available")

        st.divider()

        # ---------- FINAL RESULT ----------
        if pred == 1:
            st.error(f"⚠️ Customer likely to CHURN ({prob*100:.2f}%)")
        else:
            st.success(f"✅ Customer likely to STAY ({(1-prob)*100:.2f}%)")

        st.success("🤖 You can now ask the chatbot: 'why' or 'last prediction'")