import streamlit as st
import streamlit.components.v1 as components

from .data import PALETTES
from .pipelines import generate_frontend
from .state import initialize_state
from .ui_components import render_palette_preview, render_templates, section_header, step_bar


FRONTEND_QUESTIONS = [
    {"key": "website_use", "label": "Website use", "type": "select", "options": ["Business", "Personal", "Portfolio", "E-commerce"]},
    {"key": "business_type", "label": "Business type / niche", "type": "text", "placeholder": "e.g. Marketing Agency, SaaS, Bakery..."},
    {"key": "owner_name", "label": "Owner / admin name", "type": "text", "placeholder": "Your full name or brand name"},
    {"key": "team_size", "label": "Team size", "type": "select", "options": ["Solo", "1-5", "6-20", "21-50", "50+"]},
    {"key": "brand_story", "label": "Brand message / tagline", "type": "textarea", "placeholder": "What makes you different? One or two sentences."},
    {"key": "palette_name", "label": "Choose colour palette", "type": "palette"},
    {"key": "template_name", "label": "Choose template style", "type": "template"},
    {"key": "home_files", "label": "Home page images", "type": "uploader", "upload_key": "home_upload", "help": "Upload hero and homepage assets."},
    {"key": "portfolio_files", "label": "Portfolio images", "type": "uploader", "upload_key": "portfolio_upload", "help": "Upload portfolio/gallery images."},
    {"key": "service_files", "label": "Product / service images", "type": "uploader", "upload_key": "service_upload", "help": "Upload service or product visuals."},
    {"key": "products", "label": "Products & Pricing", "type": "products"},
    {"key": "company_phone", "label": "Company phone", "type": "text", "placeholder": "+1 555-000-1234"},
    {"key": "company_email", "label": "Company email", "type": "text", "placeholder": "hello@yourcompany.com"},
    {"key": "enquiry_placeholder", "label": "Enquiry form placeholder text", "type": "textarea"},
    {"key": "ai_provider", "label": "AI source", "type": "radio", "options": ["Mock AI", "Claude API"]},
]


def _render_question_card(idx: int) -> None:
    q = FRONTEND_QUESTIONS[idx]
    total = len(FRONTEND_QUESTIONS)
    label = q["label"]
    qtype = q["type"]

    st.markdown(
        f'<div class="question-shell fade-slide"><div class="question-kicker">Question {idx + 1} of {total}</div><h3>{label}</h3></div>',
        unsafe_allow_html=True,
    )

    if qtype == "text":
        st.session_state[q["key"]] = st.text_input(
            label,
            value=st.session_state[q["key"]],
            placeholder=q.get("placeholder", ""),
            key=f"q_{q['key']}",
            label_visibility="collapsed",
        )
    elif qtype == "textarea":
        st.session_state[q["key"]] = st.text_area(
            label,
            value=st.session_state[q["key"]],
            placeholder=q.get("placeholder", ""),
            height=110,
            key=f"q_{q['key']}",
            label_visibility="collapsed",
        )
    elif qtype == "select":
        options = q["options"]
        current = st.session_state[q["key"]].replace("\u2013", "-") if isinstance(st.session_state[q["key"]], str) else st.session_state[q["key"]]
        st.session_state[q["key"]] = st.selectbox(
            label,
            options,
            index=options.index(current) if current in options else 0,
            key=f"q_{q['key']}",
            label_visibility="collapsed",
        )
    elif qtype == "radio":
        options = q["options"]
        st.session_state[q["key"]] = st.radio(
            label,
            options,
            horizontal=True,
            index=options.index(st.session_state[q["key"]]) if st.session_state[q["key"]] in options else 0,
            key=f"q_{q['key']}",
            label_visibility="collapsed",
        )
        if st.session_state["ai_provider"] == "Claude API":
            st.session_state["claude_api_key"] = st.text_input(
                "Claude API key",
                value=st.session_state["claude_api_key"],
                type="password",
                help="Used only in this session. Never stored.",
            )
    elif qtype == "palette":
        palette_names = list(PALETTES.keys())
        st.session_state["palette_name"] = st.selectbox(
            label,
            palette_names,
            index=palette_names.index(st.session_state["palette_name"]) if st.session_state["palette_name"] in palette_names else 0,
            key="q_palette_name",
            label_visibility="collapsed",
        )
        render_palette_preview(st.session_state["palette_name"])
    elif qtype == "template":
        render_templates()
    elif qtype == "uploader":
        st.caption(q.get("help", ""))
        st.session_state[q["key"]] = st.file_uploader(
            label,
            ["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=True,
            key=q["upload_key"],
            label_visibility="collapsed",
        )
    elif qtype == "products":
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


def _render_summary() -> None:
    st.markdown('<div class="question-shell fade-slide"><div class="question-kicker">Summary</div><h3>Review your answers</h3></div>', unsafe_allow_html=True)

    cards = [
        ("Website use", st.session_state["website_use"]),
        ("Business type", st.session_state["business_type"] or "-"),
        ("Owner", st.session_state["owner_name"] or "-"),
        ("Team size", st.session_state["team_size"]),
        ("Brand message", st.session_state["brand_story"] or "-"),
        ("Palette", st.session_state["palette_name"]),
        ("Template", st.session_state["template_name"]),
        ("Home images", str(len(st.session_state.get("home_files") or []))),
        ("Portfolio images", str(len(st.session_state.get("portfolio_files") or []))),
        ("Service images", str(len(st.session_state.get("service_files") or []))),
        ("Products", str(len(st.session_state.get("products") or []))),
        ("Phone", st.session_state["company_phone"] or "-"),
        ("Email", st.session_state["company_email"] or "-"),
        ("Enquiry placeholder", st.session_state["enquiry_placeholder"] or "-"),
        ("AI source", st.session_state["ai_provider"]),
    ]

    st.markdown('<div class="summary-grid">', unsafe_allow_html=True)
    for title, value in cards:
        st.markdown(
            f'<div class="summary-card"><div class="summary-title">{title}</div><div class="summary-value">{value}</div></div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def frontend_wizard() -> None:
    step_bar("frontend_wizard")

    st.markdown('<h1 class="wizard-title">AI Website Maker</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="wizard-caption">Generate a full business website in minutes - no code required.</p>',
        unsafe_allow_html=True,
    )

    total_steps = len(FRONTEND_QUESTIONS)
    current_step = int(st.session_state.get("frontend_question_step", 0))
    current_step = max(0, min(current_step, total_steps))
    st.session_state["frontend_question_step"] = current_step

    progress_pct = int((current_step / total_steps) * 100) if total_steps else 0
    section_header("Q", "Build Your Site Questionnaire")
    st.progress(progress_pct / 100 if total_steps else 0)
    st.caption(f"Completion: {progress_pct}%")

    with st.container():
        if current_step < total_steps:
            _render_question_card(current_step)
        else:
            _render_summary()

    left, mid, right = st.columns([1, 2, 1])
    with left:
        if st.button("Back", use_container_width=True, disabled=current_step == 0):
            st.session_state["frontend_question_step"] = max(0, current_step - 1)
            st.rerun()
    with right:
        if current_step < total_steps:
            if st.button("Next", type="primary", use_container_width=True):
                st.session_state["frontend_question_step"] = min(total_steps, current_step + 1)
                st.rerun()
        else:
            if st.button("Generate Website", type="primary", use_container_width=True):
                if st.session_state["ai_provider"] == "Claude API" and not st.session_state["claude_api_key"]:
                    st.warning("Enter your Anthropic API key above, or switch to Mock AI for an instant preview.")
                else:
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
