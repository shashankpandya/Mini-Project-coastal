import io
import json
import textwrap
import time
import zipfile
from typing import Dict, List, Tuple

import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Website Maker Wizard", page_icon="WS", layout="wide")

PALETTES: Dict[str, Dict[str, str]] = {
    "Coastal Blue": {
        "primary": "#0B4F6C",
        "secondary": "#1F7A8C",
        "accent": "#E36414",
        "background": "#F5F9FC",
        "surface": "#FFFFFF",
        "text": "#132A3B",
    },
    "Forest Commerce": {
        "primary": "#1F5C3A",
        "secondary": "#2B8A57",
        "accent": "#E9A23B",
        "background": "#F4F8F4",
        "surface": "#FFFFFF",
        "text": "#1A2A22",
    },
    "Metro Slate": {
        "primary": "#1E293B",
        "secondary": "#334155",
        "accent": "#F97316",
        "background": "#F8FAFC",
        "surface": "#FFFFFF",
        "text": "#0F172A",
    },
}

TEMPLATES: List[Dict[str, str]] = [
    {
        "name": "Agency Showcase",
        "description": "Bold hero + service cards + pricing strip + trust badges.",
        "home_preview": "https://images.unsplash.com/photo-1460925895917-afdab827c52f",
        "portfolio_preview": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40",
    },
    {
        "name": "Studio Minimal",
        "description": "Minimal layout with strong typography and product storytelling.",
        "home_preview": "https://images.unsplash.com/photo-1497366754035-f200968a6e72",
        "portfolio_preview": "https://images.unsplash.com/photo-1497215842964-222b430dc094",
    },
    {
        "name": "Retail Launch",
        "description": "Product-forward landing page with pricing and enquiry conversion blocks.",
        "home_preview": "https://images.unsplash.com/photo-1483985988355-763728e1935b",
        "portfolio_preview": "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a",
    },
]

DEFAULT_PRODUCTS = [
    {"type": "Service", "name": "Starter Consulting", "description": "Discovery + strategy", "price": 499.0},
    {"type": "Product", "name": "Business Website Pack", "description": "5-page responsive site", "price": 1499.0},
]


def initialize_state() -> None:
    """Seed Streamlit session state once so all wizard steps can reuse values."""
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

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_palette_preview(palette_name: str) -> None:
    """Show a quick visual swatch preview for the selected color palette."""
    palette = PALETTES[palette_name]
    cols = st.columns(6)
    labels = ["primary", "secondary", "accent", "background", "surface", "text"]
    for idx, label in enumerate(labels):
        with cols[idx]:
            st.markdown(
                f"""
                <div style='padding:10px;border-radius:10px;background:{palette[label]};
                color:{'#FFFFFF' if label in ['primary', 'secondary', 'accent'] else palette['text']};
                border:1px solid #d8dee5;min-height:66px'>
                <strong>{label}</strong><br>{palette[label]}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_templates() -> None:
    """Render template chooser and image previews used in the wizard."""
    st.subheader("Template suggestions")
    template_names = [t["name"] for t in TEMPLATES]
    selected = st.radio("Choose template", template_names, index=template_names.index(st.session_state["template_name"]))
    st.session_state["template_name"] = selected

    chosen = [t for t in TEMPLATES if t["name"] == selected][0]
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("Home preview")
        st.image(chosen["home_preview"], use_container_width=True)
    with c2:
        st.markdown("Portfolio preview")
        st.image(chosen["portfolio_preview"], use_container_width=True)
    st.caption(chosen["description"])


def build_prompt(change_request: str = "") -> str:
    """Build the frontend-generation prompt from current wizard inputs."""
    palette = PALETTES[st.session_state["palette_name"]]
    products_text = "\n".join(
        [
            f"- {p['type']}: {p['name']} | {p['description']} | ${float(p['price']):.2f}"
            for p in st.session_state["products"]
        ]
    )
    base_prompt = f"""
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
    1) Hero and business intro.
    2) Products and services with pricing cards.
    3) Support / Enquiry section with name, phone, email, and message fields.
    4) Company contact details shown clearly: {st.session_state['company_phone']} and {st.session_state['company_email']}.
    5) Typical filler blocks: testimonials, FAQs, about section, and footer.

    Products and services:
    {products_text}

    Use modern styling, mobile responsive layout, and clear CTA buttons.
    """

    if change_request.strip():
        base_prompt += f"\n\nUser requested changes:\n{change_request.strip()}\n"

    return textwrap.dedent(base_prompt).strip()


def mock_ai_frontend(prompt: str) -> str:
    """Generate deterministic HTML locally when external AI is unavailable."""
    del prompt
    palette = PALETTES[st.session_state["palette_name"]]
    products_cards = "\n".join(
        [
            f"""
            <article class=\"card\">
              <span class=\"pill\">{item['type']}</span>
              <h3>{item['name']}</h3>
              <p>{item['description']}</p>
              <div class=\"price\">${float(item['price']):.2f}</div>
              <button>Choose Plan</button>
            </article>
            """
            for item in st.session_state["products"]
        ]
    )

    return f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{st.session_state['business_type'] or 'Business'} | Smart Site</title>
  <style>
    :root {{
      --primary: {palette['primary']};
      --secondary: {palette['secondary']};
      --accent: {palette['accent']};
      --bg: {palette['background']};
      --surface: {palette['surface']};
      --text: {palette['text']};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--text);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background:
        radial-gradient(circle at 10% 10%, rgba(255,255,255,0.85), transparent 55%),
        linear-gradient(145deg, var(--bg), #eef4f8);
    }}
    .container {{ width: min(1120px, 92%); margin: 0 auto; }}
    .hero {{ padding: 72px 0 48px; }}
    .hero h1 {{ font-size: clamp(2rem, 5vw, 3.4rem); margin: 0 0 12px; color: var(--primary); }}
    .hero p {{ max-width: 760px; line-height: 1.6; }}
    .hero .cta {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 20px; }}
    button, .btn {{
      background: var(--accent);
      color: #fff;
      border: 0;
      border-radius: 999px;
      padding: 11px 18px;
      cursor: pointer;
      font-weight: 600;
    }}
    .btn.alt {{ background: var(--secondary); text-decoration: none; }}
    .section {{ padding: 42px 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }}
    .card {{
      background: var(--surface);
      border-radius: 14px;
      padding: 18px;
      box-shadow: 0 8px 26px rgba(0,0,0,0.08);
    }}
    .pill {{ display: inline-block; padding: 4px 10px; border-radius: 999px; background: #e7eef4; font-size: 0.8rem; }}
    .price {{ font-size: 1.5rem; font-weight: bold; margin: 10px 0 14px; color: var(--secondary); }}
    .contact {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .panel {{ background: var(--surface); border-radius: 14px; padding: 18px; box-shadow: 0 8px 26px rgba(0,0,0,0.08); }}
    input, textarea {{ width: 100%; padding: 11px; margin-bottom: 10px; border: 1px solid #d8dee5; border-radius: 9px; }}
    footer {{ padding: 24px 0 42px; color: #6b7280; }}
    @media (max-width: 840px) {{ .contact {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <header class=\"hero\">
    <div class=\"container\">
      <h1>{st.session_state['business_type'] or 'Your Business'}, made for growth.</h1>
      <p>{st.session_state['brand_story'] or 'A clean, conversion-friendly website template generated by your wizard.'}</p>
      <div class=\"cta\">
        <a href=\"#products\" class=\"btn alt\">Explore Offers</a>
        <a href=\"#enquiry\" class=\"btn\">Contact Us</a>
      </div>
    </div>
  </header>

  <section id=\"products\" class=\"section\">
    <div class=\"container\">
      <h2>Products and Services</h2>
      <div class=\"grid\">
        {products_cards}
      </div>
    </div>
  </section>

  <section class=\"section\">
    <div class=\"container grid\">
      <article class=\"card\"><h3>Why clients choose us</h3><p>Fast onboarding, clear pricing, and practical business outcomes.</p></article>
      <article class=\"card\"><h3>Testimonials</h3><p>\"Excellent team and transparent process from day one.\"</p></article>
      <article class=\"card\"><h3>FAQs</h3><p>Flexible plans, upgrade options, and support channels included.</p></article>
    </div>
  </section>

  <section id=\"enquiry\" class=\"section\">
    <div class=\"container contact\">
      <div class=\"panel\">
        <h2>Support and Enquiry</h2>
        <input placeholder=\"Your name\" />
        <input placeholder=\"Phone number\" />
        <input placeholder=\"Email address\" />
        <textarea rows=\"5\" placeholder=\"{st.session_state['enquiry_placeholder']}\"></textarea>
        <button>Submit Enquiry</button>
      </div>
      <aside class=\"panel\">
        <h3>Company Contact</h3>
        <p><strong>Phone:</strong> {st.session_state['company_phone'] or 'Not set'}</p>
        <p><strong>Email:</strong> {st.session_state['company_email'] or 'Not set'}</p>
        <p>All enquiries are routed to admin workflows in backend setup.</p>
      </aside>
    </div>
  </section>

  <footer>
    <div class=\"container\">{st.session_state['owner_name'] or 'Business Owner'} | Team size: {st.session_state['team_size']} | Template: {st.session_state['template_name']}</div>
  </footer>
</body>
</html>
""".strip()


def claude_generate(prompt: str) -> Tuple[bool, str]:
    """Call Anthropic Claude and return (success, html_or_error_message)."""
    key = st.session_state.get("claude_api_key", "").strip()
    if not key:
        return False, "Claude API key is missing."

    body = {
        "model": "claude-3-5-sonnet-latest",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    try:
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=body, timeout=90)
        if response.status_code >= 300:
            return False, f"Claude API error: {response.status_code} {response.text[:300]}"

        data = response.json()
        chunks = data.get("content", [])
        text_blocks = [x.get("text", "") for x in chunks if x.get("type") == "text"]
        html = "\n".join(text_blocks).strip()
        if not html:
            return False, "Claude API returned no text."
        return True, html
    except Exception as exc:
        # Keep the UI flow alive by returning an actionable error string.
        return False, f"Claude API call failed: {exc}"


def generate_frontend(change_request: str = "") -> None:
    """Generate HTML via selected provider and store it in session state."""
    prompt = build_prompt(change_request=change_request)

    with st.spinner("Generating frontend with AI..."):
        progress = st.progress(0)
        for i in range(1, 101, 10):
            time.sleep(0.12)
            progress.progress(i)

        if st.session_state["ai_provider"] == "Claude API":
            ok, result = claude_generate(prompt)
            if ok:
                st.session_state["generated_html"] = result
            else:
                # Graceful fallback keeps the product usable even with API/key failures.
                st.warning(f"{result} Falling back to mock AI output.")
                st.session_state["generated_html"] = mock_ai_frontend(prompt)
        else:
            st.session_state["generated_html"] = mock_ai_frontend(prompt)

    if change_request.strip():
        st.session_state["revision_log"].append(change_request.strip())


def build_backend_config() -> Dict[str, str]:
    """Collect backend-related values into a serializable config map."""
    return {
        "google_project_id": st.session_state.get("google_project_id", ""),
        "google_client_id": st.session_state.get("google_client_id", ""),
        "google_client_secret": st.session_state.get("google_client_secret", ""),
        "google_refresh_token": st.session_state.get("google_refresh_token", ""),
        "google_doc_id": st.session_state.get("google_doc_id", ""),
        "whatsapp_provider": st.session_state.get("whatsapp_provider", "Twilio"),
        "whatsapp_from": st.session_state.get("whatsapp_from", ""),
        "whatsapp_to_admin": st.session_state.get("whatsapp_to_admin", ""),
        "email_provider": st.session_state.get("email_provider", "SMTP"),
        "email_host": st.session_state.get("email_host", ""),
        "email_port": str(st.session_state.get("email_port", "587")),
        "email_user": st.session_state.get("email_user", ""),
        "email_password": st.session_state.get("email_password", ""),
        "admin_email": st.session_state.get("admin_email", ""),
        "payment_gateway": st.session_state.get("payment_gateway", "Stripe"),
        "payment_public_key": st.session_state.get("payment_public_key", ""),
        "payment_secret_key": st.session_state.get("payment_secret_key", ""),
        "currency": st.session_state.get("currency", "USD"),
    }


def export_zip() -> bytes:
    """Package generated frontend plus backend scaffold into a downloadable zip."""
    frontend_html = st.session_state.get("generated_html", "") or mock_ai_frontend("")
    backend_config = build_backend_config()

    backend_stub = textwrap.dedent(
        """
        import json
        from pathlib import Path

        CONFIG = json.loads(Path("config.json").read_text(encoding="utf-8"))

        def handle_enquiry(payload: dict) -> None:
            # Next step: send to Google Docs/Sheets, WhatsApp, and email based on CONFIG.
            print("Received enquiry:", payload)

        if __name__ == "__main__":
            print("Backend scaffold loaded.")
        """
    ).strip() + "\n"

    run_server_script = textwrap.dedent(
        """
        @echo off
        cd frontend
        python -m http.server 8000
        """
    ).strip() + "\n"

    readme = textwrap.dedent(
        """
        Generated project package

        1) Open terminal in this folder.
        2) Run run_localhost.bat
        3) Visit http://localhost:8000

        Backend notes:
        - backend/config.json contains all setup values collected in wizard.
        - backend/backend_stub.py is a starting point for integrations.
        """
    ).strip() + "\n"

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("frontend/index.html", frontend_html)
        zf.writestr("backend/config.json", json.dumps(backend_config, indent=2))
        zf.writestr("backend/backend_stub.py", backend_stub)
        zf.writestr("run_localhost.bat", run_server_script)
        zf.writestr("README_generated.txt", readme)

    return buf.getvalue()


def frontend_wizard() -> None:
    """Render and handle the frontend setup step of the multi-step wizard."""
    st.title("AI Website Maker Wizard")
    st.caption("Business/personal website builder with frontend generation and backend setup wizard.")

    st.header("1) Website basics")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state["website_use"] = st.selectbox("Website use", ["Business", "Personal"], index=0)
        st.session_state["business_type"] = st.text_input("Business type / niche", value=st.session_state["business_type"])
        st.session_state["owner_name"] = st.text_input("Who are you? (owner/admin name)", value=st.session_state["owner_name"])
    with c2:
        team_options = ["Solo", "1-5", "6-20", "21-50", "50+"]
        default_team = team_options.index(st.session_state["team_size"]) if st.session_state["team_size"] in team_options else 1
        st.session_state["team_size"] = st.selectbox("Team size", team_options, index=default_team)
        st.session_state["brand_story"] = st.text_area("Brand message", value=st.session_state["brand_story"], height=100)

    st.header("2) Color palette")
    palette_names = list(PALETTES.keys())
    default_palette = palette_names.index(st.session_state["palette_name"]) if st.session_state["palette_name"] in palette_names else 0
    st.session_state["palette_name"] = st.selectbox("Choose palette", palette_names, index=default_palette)
    render_palette_preview(st.session_state["palette_name"])

    st.header("3) Template and images")
    render_templates()

    st.markdown("Upload images for drag-and-drop style portfolio/home population")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.session_state["home_files"] = st.file_uploader(
            "Home page images", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key="home_upload"
        )
    with p2:
        st.session_state["portfolio_files"] = st.file_uploader(
            "Portfolio images", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key="portfolio_upload"
        )
    with p3:
        st.session_state["service_files"] = st.file_uploader(
            "Product/service images", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key="service_upload"
        )

    st.header("4) Products and pricing")
    product_data = st.data_editor(
        st.session_state["products"],
        num_rows="dynamic",
        use_container_width=True,
        key="products_editor",
    )
    # Streamlit can return either a DataFrame-like object or list depending on versions.
    if hasattr(product_data, "to_dict"):
        st.session_state["products"] = product_data.to_dict(orient="records")
    elif isinstance(product_data, list):
        st.session_state["products"] = [dict(row) for row in product_data]

    st.header("5) Support / enquiry settings")
    s1, s2 = st.columns(2)
    with s1:
        st.session_state["company_phone"] = st.text_input("Company phone", value=st.session_state["company_phone"])
        st.session_state["company_email"] = st.text_input("Company email", value=st.session_state["company_email"])
    with s2:
        st.session_state["enquiry_placeholder"] = st.text_area(
            "Default enquiry placeholder",
            value=st.session_state["enquiry_placeholder"],
            height=90,
            
        )

    st.header("6) AI frontend generation")
    ai_options = ["Mock AI", "Claude API"]
    ai_index = ai_options.index(st.session_state["ai_provider"]) if st.session_state["ai_provider"] in ai_options else 0
    st.session_state["ai_provider"] = st.radio("AI source", ai_options, horizontal=True, index=ai_index)

    if st.session_state["ai_provider"] == "Claude API":
        st.session_state["claude_api_key"] = st.text_input(
            "Claude API key",
            value=st.session_state["claude_api_key"],
            type="password",
            help="Key is used for the request in this session only.",
        )

    if st.button("Generate frontend", type="primary", use_container_width=True):
        generate_frontend(change_request="")

    if st.session_state["generated_html"]:
        st.success("Frontend generated. Preview below.")
        components.html(st.session_state["generated_html"], height=760, scrolling=True)

        st.subheader("Make changes with prompt")
        st.session_state["revision_prompt"] = st.text_area(
            "Describe changes",
            value=st.session_state["revision_prompt"],
            placeholder="Example: Make the hero more premium and add monthly/yearly pricing switch.",
            height=110,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Apply changes", use_container_width=True):
                generate_frontend(change_request=st.session_state["revision_prompt"])
                st.session_state["revision_prompt"] = ""
        with c2:
            if st.button("Start over", use_container_width=True):
                # Preserve only the current step while resetting all other fields.
                keep = {"step": "frontend_wizard"}
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.session_state.update(keep)
                initialize_state()
                st.rerun()
        with c3:
            if st.button("Move to backend setup", use_container_width=True):
                st.session_state["step"] = "backend_wizard"
                st.rerun()

        if st.session_state["revision_log"]:
            st.caption("Revisions applied: " + " | ".join(st.session_state["revision_log"]))


def backend_wizard() -> None:
    """Render and handle backend integration setup before export."""
    st.title("Backend Setup Wizard")
    st.caption("Configure enquiry handling, alerts, and payment gateway details.")

    with st.expander("Google integration (for enquiry logs)", expanded=True):
        st.markdown("Provide Google Developer Console credentials so backend can write enquiries to admin Google Docs/Sheets.")
        g1, g2 = st.columns(2)
        with g1:
            st.session_state["google_project_id"] = st.text_input(
                "Google project ID", value=st.session_state.get("google_project_id", "")
            )
            st.session_state["google_client_id"] = st.text_input(
                "Google client ID", value=st.session_state.get("google_client_id", "")
            )
            st.session_state["google_client_secret"] = st.text_input(
                "Google client secret", value=st.session_state.get("google_client_secret", ""), type="password"
            )
        with g2:
            st.session_state["google_refresh_token"] = st.text_input(
                "Google refresh token", value=st.session_state.get("google_refresh_token", ""), type="password"
            )
            st.session_state["google_doc_id"] = st.text_input(
                "Target Google doc/sheet ID", value=st.session_state.get("google_doc_id", "")
            )

    with st.expander("WhatsApp alert automation", expanded=True):
        w1, w2 = st.columns(2)
        with w1:
            st.session_state["whatsapp_provider"] = st.selectbox(
                "Provider", ["Twilio", "Meta WhatsApp Cloud API"], index=0
            )
            st.session_state["whatsapp_from"] = st.text_input(
                "Sender WhatsApp number", value=st.session_state.get("whatsapp_from", "")
            )
        with w2:
            st.session_state["whatsapp_to_admin"] = st.text_input(
                "Admin WhatsApp number", value=st.session_state.get("whatsapp_to_admin", "")
            )

    with st.expander("Email alert automation", expanded=True):
        e1, e2 = st.columns(2)
        with e1:
            st.session_state["email_provider"] = st.selectbox("Email provider", ["SMTP", "Gmail API", "SendGrid"], index=0)
            st.session_state["email_host"] = st.text_input("SMTP host", value=st.session_state.get("email_host", ""))
            st.session_state["email_port"] = st.text_input("SMTP port", value=st.session_state.get("email_port", "587"))
        with e2:
            st.session_state["email_user"] = st.text_input("Email username", value=st.session_state.get("email_user", ""))
            st.session_state["email_password"] = st.text_input(
                "Email password/app password", value=st.session_state.get("email_password", ""), type="password"
            )
            st.session_state["admin_email"] = st.text_input("Admin email", value=st.session_state.get("admin_email", ""))

    with st.expander("Payment gateway", expanded=True):
        p1, p2 = st.columns(2)
        with p1:
            st.session_state["payment_gateway"] = st.selectbox("Gateway", ["Stripe", "Razorpay", "PayPal"], index=0)
            st.session_state["payment_public_key"] = st.text_input(
                "Public key", value=st.session_state.get("payment_public_key", "")
            )
        with p2:
            st.session_state["payment_secret_key"] = st.text_input(
                "Secret key", value=st.session_state.get("payment_secret_key", ""), type="password"
            )
            st.session_state["currency"] = st.text_input("Currency", value=st.session_state.get("currency", "USD"))

    st.info("These values are packaged into backend config in this step. Live API integrations can be activated in the next step.")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Back to frontend", use_container_width=True):
            st.session_state["step"] = "frontend_wizard"
            st.rerun()
    with c2:
        if st.button("Build package", type="primary", use_container_width=True):
            st.session_state["backend_config"] = build_backend_config()
    with c3:
        if st.button("Start over all", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            initialize_state()
            st.rerun()

    if st.session_state.get("backend_config"):
        st.success("Package ready. Download zip below.")
        z = export_zip()
        st.download_button(
            "Download generated website zip",
            data=z,
            file_name="generated_website_package.zip",
            mime="application/zip",
            use_container_width=True,
        )


initialize_state()

# Route to current wizard step based on persisted session state.
if st.session_state["step"] == "frontend_wizard":
    frontend_wizard()
else:
    backend_wizard()
