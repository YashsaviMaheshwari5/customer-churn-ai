import streamlit as st
from database import add_user, login_user

st.set_page_config(page_title="Login", layout="wide")

# --- SESSION ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- CSS ---
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #6aa3d8, #3f7fbf);
}

/* GLASS CARD */
.card {
    width: 380px;
    padding: 35px;
    border-radius: 20px;
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(18px);
    box-shadow: 0px 15px 40px rgba(0,0,0,0.3);
    text-align: center;
    color: white;
}

/* BUTTON */
.stButton > button {
    width: 100%;
    background: #0b3c6f;
    color: white;
    border-radius: 10px;
    padding: 12px;
    font-size: 16px;
}

/* SOCIAL */
.social-container {
    display: flex;
    gap: 10px;
}
.social-btn {
    flex: 1;
    padding: 10px;
    border-radius: 10px;
    background: white;
    color: black;
    text-align: center;
}

/* TEXT */
.divider {
    margin: 15px 0;
    font-size: 12px;
    opacity: 0.7;
}
.footer {
    font-size: 12px;
    opacity: 0.8;
}

</style>
""", unsafe_allow_html=True)

# --- LAYOUT ---
col1, col2 = st.columns([1,1])

# LEFT SIDE (no image yet)
with col1:
    st.markdown("<h1 style='color:white;'>Welcome Back 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:white;'>Login to continue your journey</p>", unsafe_allow_html=True)

# RIGHT SIDE
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("<h2>🔐 Login</h2>", unsafe_allow_html=True)

    menu = ["Login", "Register"]
    choice = st.radio("", menu, horizontal=True)

    # LOGIN
    if choice == "Login":
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")

        if st.button("Sign in"):
            user = login_user(email, password)
            if user:
                st.session_state["logged_in"] = True
                st.success("Login Successful 🎉")
                st.switch_page("app.py")
            else:
                st.error("Invalid email or password")

    # REGISTER
    else:
        new_email = st.text_input("📧 Email")
        new_password = st.text_input("🔒 Password", type="password")

        if st.button("Create Account"):
            if add_user(new_email, new_password):
                st.success("Account Created ✅")
            else:
                st.error("User already exists")

    # SOCIAL
    st.markdown('<div class="divider">or continue with</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="social-container">
        <div class="social-btn">🔴 Google</div>
        <div class="social-btn">⚫ GitHub</div>
        <div class="social-btn">🔵 Facebook</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="footer">Use Register if new user</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)