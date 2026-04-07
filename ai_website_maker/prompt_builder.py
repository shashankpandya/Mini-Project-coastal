import textwrap

import streamlit as st

from .data import PALETTES
def build_prompt(change_request: str = "") -> str:
    palette = PALETTES[st.session_state["palette_name"]]
    products_text = "\n".join(
        [f"- {p['type']}: {p['name']} | {p['description']} | ${float(p['price']):.2f}"
         for p in st.session_state["products"]]
    )
    base = f"""
    Build a responsive website frontend in one standalone HTML file with embedded CSS and JS.

    Website focus: {st.session_state['website_use']}
    Business type: {st.session_state['business_type']}
    Owner/team: {st.session_state['owner_name']} / team size {st.session_state['team_size']}
    Brand story: {st.session_state['brand_story']}
    Template style: {st.session_state['template_name']}

    Color palette:
    - Primary: {palette['primary']}
    - Secondary: {palette['secondary']}
    - Accent: {palette['accent']}
    - Background: {palette['background']}
    - Surface: {palette['surface']}
    - Text: {palette['text']}

    Must include these sections:
    1) Hero and business intro with animated CTA.
    2) Products and services with pricing cards.
    3) Support / Enquiry section with name, phone, email, and message fields.
    4) Company contact details shown clearly: {st.session_state['company_phone']} and {st.session_state['company_email']}.
    5) Testimonials, FAQs, about section, and footer.

    Products and services:
    {products_text}

    Use modern styling, mobile responsive layout, smooth scroll, and clear CTA buttons.
    Output ONLY the raw HTML, no markdown, no commentary.
    """
    if change_request.strip():
        base += f"\n\nUser requested changes:\n{change_request.strip()}\n"
    return textwrap.dedent(base).strip()



