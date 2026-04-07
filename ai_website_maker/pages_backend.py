import time

import streamlit as st

from .pipelines import build_backend_config, export_zip
from .state import initialize_state
from .ui_components import step_bar


def backend_wizard() -> None:
    step_bar("backend_wizard")

    st.markdown('<h1 class="wizard-title">Backend Setup</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="wizard-caption">Configure integrations for enquiry logging, alerts, and payments.</p>',
        unsafe_allow_html=True,
    )

    with st.expander("Google integration - enquiry logs to Docs/Sheets", expanded=True):
        st.caption("Provide credentials from Google Cloud Console (OAuth 2.0 client).")
        g1, g2 = st.columns(2)
        with g1:
            st.session_state["google_project_id"] = st.text_input("Project ID", value=st.session_state.get("google_project_id", ""), key="bk_gpi")
            st.session_state["google_client_id"] = st.text_input("Client ID", value=st.session_state.get("google_client_id", ""), key="bk_gci")
            st.session_state["google_client_secret"] = st.text_input("Client secret", value=st.session_state.get("google_client_secret", ""), type="password", key="bk_gcs")
        with g2:
            st.session_state["google_refresh_token"] = st.text_input("Refresh token", value=st.session_state.get("google_refresh_token", ""), type="password", key="bk_grt")
            st.session_state["google_doc_id"] = st.text_input("Target Doc/Sheet ID", value=st.session_state.get("google_doc_id", ""), key="bk_gdi")

    with st.expander("WhatsApp alerts - notify admin on each enquiry", expanded=False):
        w1, w2 = st.columns(2)
        with w1:
            st.session_state["whatsapp_provider"] = st.selectbox(
                "Provider", ["Twilio", "Meta WhatsApp Cloud API"],
                index=["Twilio", "Meta WhatsApp Cloud API"].index(
                    st.session_state.get("whatsapp_provider", "Twilio")
                ) if st.session_state.get("whatsapp_provider") in ["Twilio", "Meta WhatsApp Cloud API"] else 0,
                key="bk_wap",
            )
            st.session_state["whatsapp_from"] = st.text_input(
                "Sender WhatsApp number", value=st.session_state.get("whatsapp_from", ""),
                placeholder="+1 555-000-0000", key="bk_wfr",
            )
        with w2:
            st.session_state["whatsapp_to_admin"] = st.text_input(
                "Admin WhatsApp number", value=st.session_state.get("whatsapp_to_admin", ""),
                placeholder="+1 555-999-9999", key="bk_wta",
            )

    with st.expander("Email alerts", expanded=False):
        e1, e2 = st.columns(2)
        with e1:
            st.session_state["email_provider"] = st.selectbox(
                "Email provider", ["SMTP", "Gmail API", "SendGrid"],
                index=["SMTP", "Gmail API", "SendGrid"].index(
                    st.session_state.get("email_provider", "SMTP")
                ) if st.session_state.get("email_provider") in ["SMTP", "Gmail API", "SendGrid"] else 0,
                key="bk_epv",
            )
            st.session_state["email_host"] = st.text_input("SMTP host", value=st.session_state.get("email_host", ""), placeholder="smtp.gmail.com", key="bk_eh")
            st.session_state["email_port"] = st.text_input("SMTP port", value=st.session_state.get("email_port", "587"), key="bk_ep")
        with e2:
            st.session_state["email_user"] = st.text_input("Email username", value=st.session_state.get("email_user", ""), key="bk_eu")
            st.session_state["email_password"] = st.text_input("App password", value=st.session_state.get("email_password", ""), type="password", key="bk_epw")
            st.session_state["admin_email"] = st.text_input("Admin email (recipient)", value=st.session_state.get("admin_email", ""), placeholder="you@company.com", key="bk_ae")

    with st.expander("Payment gateway", expanded=False):
        p1, p2 = st.columns(2)
        with p1:
            st.session_state["payment_gateway"] = st.selectbox(
                "Gateway", ["Stripe", "Razorpay", "PayPal"],
                index=["Stripe", "Razorpay", "PayPal"].index(
                    st.session_state.get("payment_gateway", "Stripe")
                ) if st.session_state.get("payment_gateway") in ["Stripe", "Razorpay", "PayPal"] else 0,
                key="bk_pg",
            )
            st.session_state["payment_public_key"] = st.text_input("Public key", value=st.session_state.get("payment_public_key", ""), key="bk_ppk")
        with p2:
            st.session_state["payment_secret_key"] = st.text_input("Secret key", value=st.session_state.get("payment_secret_key", ""), type="password", key="bk_psk")
            st.session_state["currency"] = st.text_input("Currency code", value=st.session_state.get("currency", "USD"), placeholder="USD / INR / EUR", key="bk_cur")

    st.info(
        "All values are packaged into **backend/config.json** inside the zip. "
        "The backend stub shows exactly where to insert each SDK call."
    )
    st.markdown("&nbsp;", unsafe_allow_html=True)

    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        if st.button("<- Back to Frontend", use_container_width=True):
            st.session_state["step"] = "frontend_wizard"
            st.rerun()
    with bc2:
        if st.button("Build Package", type="primary", use_container_width=True):
            with st.spinner("Packaging your website..."):
                time.sleep(0.6)
                st.session_state["backend_config"] = build_backend_config()
    with bc3:
        if st.button("Start Over All", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            initialize_state()
            st.rerun()

    if st.session_state.get("backend_config"):
        st.success("Package ready! Click below to download your complete website.")
        z = export_zip()
        st.download_button(
            "Download generated_website_package.zip",
            data=z,
            file_name="generated_website_package.zip",
            mime="application/zip",
            use_container_width=True,
        )
