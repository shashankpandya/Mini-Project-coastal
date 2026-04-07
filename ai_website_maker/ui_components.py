import streamlit as st

from .data import PALETTES, TEMPLATES


def section_header(num: str, text: str) -> None:
    st.markdown(
        f"""<div class="section-header">
            <span class="section-num">{num}</span>{text}
        </div>""",
        unsafe_allow_html=True,
    )


def step_bar(active: str) -> None:
    steps = [
        ("01", "Basics", "frontend_wizard"),
        ("02", "Design", "frontend_wizard"),
        ("03", "Generate", "frontend_wizard"),
        ("04", "Backend", "backend_wizard"),
    ]
    # Map active step to index
    active_idx = 0 if active == "frontend_wizard" else 3
    if active == "frontend_wizard" and st.session_state.get("generated_html"):
        active_idx = 2

    items_html = ""
    for i, (num, label, _) in enumerate(steps):
        if i < active_idx:
            cls = "done"; icon = "OK"
        elif i == active_idx:
            cls = "active"; icon = num
        else:
            cls = "idle"; icon = num
        lbl_cls = "active" if i == active_idx else ""
        items_html += f"""
        <div class="step-item">
            <div class="step-dot {cls}">{icon}</div>
            <span class="step-label {lbl_cls}">{label}</span>
        </div>"""

    st.markdown(f'<div class="step-bar">{items_html}</div>', unsafe_allow_html=True)


def render_palette_preview(palette_name: str) -> None:
    palette = PALETTES[palette_name]
    labels = ["primary", "secondary", "accent", "background", "surface", "text"]
    swatches = ""
    for label in labels:
        color = palette[label]
        light = label in ["background", "surface"]
        text_color = palette["text"] if light else "#FFFFFF"
        swatches += f"""
        <div class="swatch" style="background:{color};color:{text_color};">
            <div style="font-size:0.65rem;opacity:0.7;margin-bottom:3px">{label}</div>
            {color}
        </div>"""
    st.markdown(f'<div class="swatch-wrap">{swatches}</div>', unsafe_allow_html=True)


def render_templates() -> None:
    template_names = [t["name"] for t in TEMPLATES]
    chosen_name = st.radio(
        "Choose template style",
        template_names,
        index=template_names.index(st.session_state["template_name"]),
        horizontal=True,
    )
    st.session_state["template_name"] = chosen_name
    chosen = next(t for t in TEMPLATES if t["name"] == chosen_name)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Home preview**")
        st.image(chosen["home_preview"], use_container_width=True)
    with c2:
        st.markdown("**Portfolio preview**")
        st.image(chosen["portfolio_preview"], use_container_width=True)
    st.caption(f"- {chosen['description']}")



