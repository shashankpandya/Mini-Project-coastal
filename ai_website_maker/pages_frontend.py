import streamlit as st
import streamlit.components.v1 as components

from .data import PALETTES
from .pipelines import generate_frontend
from .state import initialize_state
from .ui_components import render_palette_preview, render_templates, section_header, step_bar


def frontend_wizard() -> None:
    step_bar("frontend_wizard")

    st.markdown('<h1 class="wizard-title">AI Website Maker</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="wizard-caption">Generate a full business website in minutes - no code required.</p>',
        unsafe_allow_html=True,
    )

    section_header("1", "Website Basics")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state["website_use"] = st.selectbox(
            "Website use", ["Business", "Personal", "Portfolio", "E-commerce"],
            index=["Business", "Personal", "Portfolio", "E-commerce"].index(
                st.session_state["website_use"]
            ) if st.session_state["website_use"] in ["Business", "Personal", "Portfolio", "E-commerce"] else 0,
        )
        st.session_state["business_type"] = st.text_input(
            "Business type / niche", value=st.session_state["business_type"],
            placeholder="e.g. Marketing Agency, SaaS, Bakery...",
        )
        st.session_state["owner_name"] = st.text_input(
            "Owner / admin name", value=st.session_state["owner_name"],
            placeholder="Your full name or brand name",
        )
    with c2:
        team_opts = ["Solo", "1-5", "6-20", "21-50", "50+"]
        cur = st.session_state["team_size"].replace("\u2013", "-")
        st.session_state["team_size"] = st.selectbox(
            "Team size", team_opts,
            index=team_opts.index(cur) if cur in team_opts else 1,
        )
        st.session_state["brand_story"] = st.text_area(
            "Brand message / tagline", value=st.session_state["brand_story"],
            height=106, placeholder="What makes you different? One or two sentences.",
        )

    section_header("2", "Colours & Template")
    palette_names = list(PALETTES.keys())
    st.session_state["palette_name"] = st.selectbox(
        "Choose colour palette",
        palette_names,
        index=palette_names.index(st.session_state["palette_name"])
        if st.session_state["palette_name"] in palette_names else 0,
    )
    render_palette_preview(st.session_state["palette_name"])

    st.markdown("&nbsp;", unsafe_allow_html=True)
    render_templates()

    st.markdown("**Upload images** (drag-and-drop into the site)")
    u1, u2, u3 = st.columns(3)
    with u1:
        st.session_state["home_files"] = st.file_uploader(
            "Home page images", ["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=True, key="home_upload",
        )
    with u2:
        st.session_state["portfolio_files"] = st.file_uploader(
            "Portfolio images", ["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=True, key="portfolio_upload",
        )
    with u3:
        st.session_state["service_files"] = st.file_uploader(
            "Product / service images", ["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=True, key="service_upload",
        )

    section_header("3", "Products & Pricing")
    product_data = st.data_editor(
        st.session_state["products"],
        num_rows="dynamic",
        use_container_width=True,
        key="products_editor",
        column_config={
            "type": st.column_config.SelectboxColumn(
                "Type", options=["Service", "Product", "Subscription"], required=True
            ),
            "price": st.column_config.NumberColumn("Price ($)", min_value=0, format="$%.2f"),
        },
    )
    if hasattr(product_data, "to_dict"):
        st.session_state["products"] = product_data.to_dict(orient="records")
    elif isinstance(product_data, list):
        st.session_state["products"] = [dict(r) for r in product_data]

    section_header("4", "Contact & Enquiry Settings")
    s1, s2 = st.columns(2)
    with s1:
        st.session_state["company_phone"] = st.text_input(
            "Company phone", value=st.session_state["company_phone"],
            placeholder="+1 555-000-1234",
        )
        st.session_state["company_email"] = st.text_input(
            "Company email", value=st.session_state["company_email"],
            placeholder="hello@yourcompany.com",
        )
    with s2:
        st.session_state["enquiry_placeholder"] = st.text_area(
            "Enquiry form placeholder text",
            value=st.session_state["enquiry_placeholder"], height=90,
        )

    section_header("5", "AI Generation")
    ai_opts = ["Mock AI", "Claude API"]
    st.session_state["ai_provider"] = st.radio(
        "AI source", ai_opts, horizontal=True,
        index=ai_opts.index(st.session_state["ai_provider"])
        if st.session_state["ai_provider"] in ai_opts else 0,
    )

    if st.session_state["ai_provider"] == "Claude API":
        st.session_state["claude_api_key"] = st.text_input(
            "Claude API key",
            value=st.session_state["claude_api_key"],
            type="password",
            help="Used only in this session. Never stored.",
        )
        if not st.session_state["claude_api_key"]:
            st.info("Enter your Anthropic API key above, or switch to Mock AI for an instant preview.")

    if st.button("Generate Website", type="primary", use_container_width=True):
        generate_frontend()

    if st.session_state["generated_html"]:
        st.success("Website generated successfully!")
        st.markdown("&nbsp;", unsafe_allow_html=True)
        components.html(st.session_state["generated_html"], height=780, scrolling=True)

        section_header("R", "Refine with AI")
        st.session_state["revision_prompt"] = st.text_area(
            "Describe changes to apply",
            value=st.session_state["revision_prompt"],
            placeholder="e.g. Make the hero darker and more premium. Add a monthly/yearly pricing toggle.",
            height=100,
        )

        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            if st.button("Apply Changes", use_container_width=True):
                if st.session_state["revision_prompt"].strip():
                    generate_frontend(change_request=st.session_state["revision_prompt"])
                    st.session_state["revision_prompt"] = ""
                else:
                    st.warning("Enter a change request first.")
        with rc2:
            if st.button("Start Over", use_container_width=True):
                keep = {"step": "frontend_wizard"}
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.session_state.update(keep)
                initialize_state()
                st.rerun()
        with rc3:
            if st.button("Backend Setup ->", use_container_width=True):
                st.session_state["step"] = "backend_wizard"
                st.rerun()

        if st.session_state["revision_log"]:
            st.caption("Revisions: " + "  >  ".join(st.session_state["revision_log"]))
