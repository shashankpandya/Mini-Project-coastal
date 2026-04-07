import streamlit as st

from .data import DEFAULT_PRODUCTS, TEMPLATES
def initialize_state() -> None:
    defaults = {
        "step": "frontend_wizard",
        "website_use": "Business",
        "business_type": "",
        "owner_name": "",
        "team_size": "1-5",
        "brand_story": "",
        "palette_name": "Coastal Blue",
        "template_name": TEMPLATES[0]["name"],
        "products": DEFAULT_PRODUCTS,
        "company_phone": "",
        "company_email": "",
        "enquiry_placeholder": "Tell us what you need help with.",
        "portfolio_files": [],
        "home_files": [],
        "service_files": [],
        "ai_provider": "Mock AI",
        "claude_api_key": "",
        "generated_html": "",
        "revision_prompt": "",
        "revision_log": [],
        "backend_config": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v



