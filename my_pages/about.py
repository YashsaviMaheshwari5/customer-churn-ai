import streamlit as st
from pathlib import Path


def show():
    # 🔥 Page config
    st.set_page_config(page_title="About Me", layout="wide")

    # 🎨 Clean modern styling
    st.markdown("""
        <style>
        .main-container {
            padding: 20px 40px;
        }
        .profile-img img {
            border-radius: 50%;
            border: 4px solid #4CAF50;
            box-shadow: 0px 6px 20px rgba(0,0,0,0.2);
        }
        .name {
            font-size: 36px;
            font-weight: bold;
        }
        .role {
            font-size: 18px;
            color: gray;
            margin-bottom: 10px;
        }
        .section {
            padding: 15px;
            border-radius: 12px;
            background-color: #f9f9f9;
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 📁 Image path (FIXED)
    BASE_DIR = Path(__file__).resolve().parent
    image_path = BASE_DIR / "assets" / "profile.jpg"

    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # 🚀 HERO SECTION (Image LEFT + Text RIGHT)
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<div class='profile-img'>", unsafe_allow_html=True)
        st.image(str(image_path), width=220)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='name'>Hi, I'm Yashsavi 👋</div>", unsafe_allow_html=True)
        st.markdown("<div class='role'>BTech CSE-AI Student | ML Enthusiast</div>", unsafe_allow_html=True)

        st.write("""
        🎓 Studying at Chitkara University  
        🤖 Passionate about Machine Learning & AI  
        📊 Built Customer Churn Prediction System  
        💡 Love solving real-world problems using data  
        """)

    st.markdown("---")

    # ⚡ Skills
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("⚡ Skills")
    st.write("""
    - Python 🐍  
    - Machine Learning 🤖  
    - Data Analysis 📊  
    - Streamlit Development 🌐  
    - SQL & Databases 🗄️  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # 🚀 Projects
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🚀 Projects")
    st.write("""
    - Customer Churn Prediction using Classification  
    - Student Performance Predictor  
    - ML Model Comparison Dashboard  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # 📬 Contact
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📬 Contact")
    st.write("""
    📧 Email: yashsavi8591.beaift24@chitkara.edu.in  
    🔗 LinkedIn: https://linkedin.com/in/Yashsavi Maheshwari 
    💻 GitHub: https://github.com/YashsaviMaheshwari5  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # 🎯 Footer
    st.markdown("""
        <center>
        <p style='color:gray;'>✨ Built with Streamlit | AI Portfolio</p>
        </center>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)