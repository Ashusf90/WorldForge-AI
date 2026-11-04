import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    cloud_key = st.secrets.get("GEMINI_API_KEY", "")
    cloud_model = st.secrets.get("GEMINI_MODEL", "")
except Exception:
    cloud_key = ""
    cloud_model = ""

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or cloud_key

GEMINI_MODEL = (
    os.getenv("GEMINI_MODEL")
    or cloud_model
    or "gemini-flash-lite-latest"
)

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing!")