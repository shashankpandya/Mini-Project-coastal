import streamlit as st

from .pages_backend import backend_wizard
from .pages_frontend import frontend_wizard
from .state import initialize_state
from .styles import apply_global_styles


def run_app() -> None:
    st.set_page_config(
        page_title="AI Website Maker",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    apply_global_styles()
    initialize_state()

    if st.session_state["step"] == "frontend_wizard":
        frontend_wizard()
    else:
        backend_wizard()
