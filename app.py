import streamlit as st
from streamlit_option_menu import option_menu

# ---------- IMPORT PAGES ----------
from my_pages import (
    dashboard,
    prediction,
    model_comparison,
    chatbot,
    about
)

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Churn AI",
    page_icon="🤖",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

/* Main Background */
[data-testid="stAppViewContainer"] {
    background-color: #FFFFFF;
}

/* Text */
h1, h2, h3, h4, h5, h6, p {
    color: #1A1A1A;
}

/* Buttons */
.stButton > button {
    background-color: #FF6B00;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 18px;
    font-weight: bold;
}

/* Chat Input */
.stChatInput input {
    border-radius: 10px;
}

/* Remove top padding */
.block-container {
    padding-top: 1rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #F7F7F7;
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- LOGIN PAGE ----------
def login():

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.title("🤖 Churn AI Dashboard")

        st.markdown("""
Welcome to the AI-powered Customer Churn Prediction System.
""")

        st.divider()

        username = st.text_input("👤 Username", key="login_username")
        password = st.text_input("🔒 Password", type="password", key="login_password")

        if st.button("🚀 Login", use_container_width=True):

            # SIMPLE LOGIN
            if username == "admin" and password == "1234":

                st.session_state.logged_in = True

                st.success("✅ Login Successful")

                st.rerun()

            else:
                st.error("❌ Invalid username or password")


# ---------- MAIN APPLICATION ----------
def main_app():

    # ---------- SIDEBAR ----------
    with st.sidebar:

        st.title("🤖 Churn AI")

        st.caption("Customer Churn Prediction System")

        st.divider()

        selected = option_menu(
            menu_title="Navigation",

            options=[
                "Dashboard",
                "Prediction",
                "Model Comparison",
                "Chatbot",
                "About"
            ],

            icons=[
                "bar-chart",
                "cpu",
                "graph-up",
                "chat-dots",
                "info-circle"
            ],

            menu_icon="cast",

            default_index=0
        )

        st.divider()

        # ---------- LOGOUT ----------
        if st.button("🚪 Logout", use_container_width=True):

            st.session_state.logged_in = False

            st.rerun()

    # ---------- PAGE CONTENT ----------
    if selected == "Dashboard":
        dashboard.show()

    elif selected == "Prediction":
        prediction.show()

    elif selected == "Model Comparison":
        model_comparison.show()

    elif selected == "Chatbot":
        chatbot.show()

    elif selected == "About":
        about.show()

    # ---------- FOOTER ----------
    st.divider()

    st.markdown("""
<center>

Made with ❤️ using Streamlit & Machine Learning

</center>
""", unsafe_allow_html=True)


# ---------- RUN ----------
if not st.session_state.logged_in:

    login()

else:

    main_app()