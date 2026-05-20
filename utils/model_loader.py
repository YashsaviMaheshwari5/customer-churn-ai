import os
import joblib

# Optional: cache for Streamlit
try:
    import streamlit as st
    USE_CACHE = True
except:
    USE_CACHE = False


def _load_model_internal():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    possible_paths = [
        os.path.join(BASE_DIR, "model.pkl"),
        os.path.join(BASE_DIR, "models", "churn_model.pkl"),
        os.path.join(BASE_DIR, "saved_models", "model.pkl")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return joblib.load(path)

    raise FileNotFoundError(
        f"❌ Model file not found.\nChecked paths:\n" + "\n".join(possible_paths)
    )


# ---------- PUBLIC FUNCTION ----------
if USE_CACHE:
    @st.cache_resource
    def load_model():
        return _load_model_internal()
else:
    def load_model():
        return _load_model_internal()