import streamlit as st
import numpy as np
import joblib

from utils.model_loader import load_model

# ---------- LOAD MODEL ----------
model = load_model()

# ---------- LOAD MODEL COLUMNS ----------
model_columns = joblib.load("model_columns.pkl")

# ---------- FEATURE NAMES ----------
FEATURE_NAMES = [
    "tenure",
    "monthly_charges",
    "total_charges",
    "contract",
    "internet_service",
    "online_security",
    "tech_support"
]

# ---------- PARSE INPUT ----------
def parse_named_input(text: str):

    try:
        parts = text.replace("predict", "").strip().split(",")

        data = {}

        for part in parts:

            key, value = part.strip().split("=")

            data[key.strip()] = float(value.strip())

        missing = [
            f for f in FEATURE_NAMES
            if f not in data
        ]

        if missing:

            return None, f"""
⚠️ Missing features:

{', '.join(missing)}
"""

        return data, None

    except:

        return None, """
❌ Invalid format.

✅ Example:

predict tenure=5,
monthly_charges=70,
total_charges=300,
contract=1,
internet_service=1,
online_security=0,
tech_support=1
"""


# ---------- PREDICTION ----------
def predict_churn(user_data):

    # ---------- CREATE ALL MODEL COLUMNS ----------
    input_data = {
        col: 0
        for col in model_columns
    }

    # ---------- NUMERICAL FEATURES ----------
    if "tenure" in user_data:
        input_data["tenure"] = user_data["tenure"]

    if "monthly_charges" in user_data:
        input_data["MonthlyCharges"] = user_data["monthly_charges"]

    if "total_charges" in user_data:
        input_data["TotalCharges"] = user_data["total_charges"]

    # ---------- CONTRACT ENCODING ----------
    contract = int(user_data["contract"])

    if contract == 1:
        if "Contract_One year" in input_data:
            input_data["Contract_One year"] = 1

    elif contract == 2:
        if "Contract_Two year" in input_data:
            input_data["Contract_Two year"] = 1

    # ---------- INTERNET SERVICE ----------
    if int(user_data["internet_service"]) == 1:

        if "InternetService_Fiber optic" in input_data:
            input_data["InternetService_Fiber optic"] = 1

    # ---------- ONLINE SECURITY ----------
    if int(user_data["online_security"]) == 1:

        if "OnlineSecurity_Yes" in input_data:
            input_data["OnlineSecurity_Yes"] = 1

    # ---------- TECH SUPPORT ----------
    if int(user_data["tech_support"]) == 1:

        if "TechSupport_Yes" in input_data:
            input_data["TechSupport_Yes"] = 1

    # ---------- FINAL INPUT ----------
    final_input = np.array(
        [list(input_data.values())]
    )

    # ---------- PREDICT ----------
    prediction = model.predict(final_input)[0]

    prob = model.predict_proba(final_input)[0][1]

    # ---------- RISK LEVEL ----------
    if prob < 0.4:
        risk = "🟢 LOW"

    elif prob < 0.7:
        risk = "🟡 MEDIUM"

    else:
        risk = "🔴 HIGH"

    # ---------- RESPONSE ----------
    if prediction == 1:

        response = f"""
⚠️ Customer is likely to churn

📊 Churn Probability: {prob*100:.2f}%
🚨 Risk Level: {risk}

💡 Recommended Actions:
• Offer loyalty discounts
• Improve technical support
• Encourage yearly contracts
• Increase customer engagement
"""

    else:

        response = f"""
✅ Customer is likely to stay

📊 Confidence: {(1-prob)*100:.2f}%
🚨 Risk Level: {risk}

💡 Customer appears stable and satisfied.
"""

    return response, prob


# ---------- EXPLAIN PREDICTION ----------
def explain_prediction(prob):

    try:

        importance = model.feature_importances_

        top_idx = np.argmax(importance)

        top_feature = model_columns[top_idx]

        if prob > 0.7:

            return f"""
📊 High churn risk detected.

🔥 Most influential feature:
➡️ {top_feature}

Possible Reasons:
• High monthly charges
• Weak customer engagement
• No long-term contract
"""

        elif prob > 0.4:

            return f"""
📊 Moderate churn risk.

🔥 Key feature affecting prediction:
➡️ {top_feature}

💡 Recommendation:
Customer may respond well to discounts or support improvements.
"""

        else:

            return f"""
📊 Customer appears stable.

🔥 Stability influenced by:
➡️ {top_feature}

✅ Low churn probability detected.
"""

    except:

        return "⚠️ Explanation unavailable."


# ---------- INTENT DETECTION ----------
def detect_intent(text):

    text = text.lower()

    intents = {

        "predict": [
            "predict",
            "check churn",
            "analyze customer"
        ],

        "explain": [
            "why",
            "reason",
            "explain"
        ],

        "model": [
            "model",
            "algorithm"
        ],

        "retention": [
            "retention",
            "reduce churn"
        ],

        "help": [
            "help",
            "guide"
        ],

        "last_prediction": [
            "last prediction"
        ]
    }

    for intent, keywords in intents.items():

        for keyword in keywords:

            if keyword in text:
                return intent

    return "general"


# ---------- BOT RESPONSE ----------
def get_bot_response(user_input):

    intent = detect_intent(user_input)

    # ---------- PREDICT ----------
    if intent == "predict":

        values, error = parse_named_input(user_input)

        if error:
            return error

        result, prob = predict_churn(values)

        st.session_state.last_prediction = result
        st.session_state.last_probability = prob

        return result

    # ---------- EXPLAIN ----------
    elif intent == "explain":

        if "last_probability" in st.session_state:

            return explain_prediction(
                st.session_state.last_probability
            )

        return "⚠️ Please make a prediction first."

    # ---------- LAST PREDICTION ----------
    elif intent == "last_prediction":

        if "last_prediction" in st.session_state:
            return st.session_state.last_prediction

        return "⚠️ No previous prediction available."

    # ---------- RETENTION ----------
    elif intent == "retention":

        return """
📈 Customer Retention Strategies:

• Improve customer support
• Offer loyalty discounts
• Encourage yearly subscriptions
• Reduce monthly charges
"""

    # ---------- MODEL ----------
    elif intent == "model":

        return """
🤖 Current AI Model:

• Random Forest Classifier
• Optimized using GridSearchCV
• Trained on Telco Churn Dataset
"""

    # ---------- HELP ----------
    elif intent == "help":

        return """
🤖 Available Commands:

• predict ...
• why
• model
• retention
• last prediction

✅ Example:

predict tenure=5,
monthly_charges=70,
total_charges=300,
contract=1,
internet_service=1,
online_security=0,
tech_support=1
"""

    # ---------- GENERAL ----------
    return """
🤖 I didn't fully understand that.

Try:
• predict ...
• why
• retention
• model
• help
"""


# ---------- MAIN UI ----------
def show():

    st.title("💬 Smart AI Churn Assistant")

    st.success(
        "🤖 AI Assistant is online and ready."
    )

    # ---------- HELP PANEL ----------
    with st.expander("📘 Example Usage"):

        st.markdown("""
### Example Prediction

predict tenure=5,
monthly_charges=70,
total_charges=300,
contract=1,
internet_service=1,
online_security=0,
tech_support=1

### Other Commands

• why  
• retention  
• model  
• help  
• last prediction
""")

    # ---------- SESSION ----------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ---------- DISPLAY CHAT ----------
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---------- USER INPUT ----------
    user_input = st.chat_input(
        "Ask something about churn..."
    )

    # ---------- HANDLE INPUT ----------
    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):

            with st.spinner("🤖 Analyzing..."):

                response = get_bot_response(user_input)

                st.markdown(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    # ---------- CLEAR CHAT ----------
    if st.button("🧹 Clear Chat"):

        st.session_state.messages = []

        st.rerun()