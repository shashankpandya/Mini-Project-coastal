# AI Website Maker Wizard

A no-code, AI-powered website builder built with **Streamlit**. Fill out a guided wizard, hit **Generate**, and receive a complete, ready-to-deploy HTML website — optionally enhanced by Claude (Anthropic's AI) — plus a backend integration scaffold and a downloadable ZIP package.

---

## What It Does

### Frontend Wizard (Step 1 → 3)

| Step | What you configure | What it produces |
|------|-------------------|-----------------|
| **Website Basics** | Business type, owner name, team size, brand story | Personalized copy injected into the site |
| **Colours & Template** | 5 built-in colour palettes, 3 layout templates, image uploads | Visual identity applied across every section |
| **Products & Pricing** | Editable table of services/products with prices | Pricing cards rendered in the generated site |
| **Contact Settings** | Phone, email, enquiry placeholder text | Populated contact section and enquiry form |
| **AI Generation** | Mock AI or Claude API (via your own key) | A single-file, responsive HTML website |

The generated website includes:
- Sticky navigation bar
- Animated hero section with CTA buttons
- Products & services pricing cards
- Testimonials / trust badges
- Enquiry form with contact panel
- Footer with business info

### Backend Setup Wizard (Step 4)

Configure integrations that the backend scaffold will use:

| Integration | Purpose |
|-------------|---------|
| **Google Docs/Sheets** | Log each enquiry to a spreadsheet automatically |
| **WhatsApp (Twilio or Meta Cloud API)** | Ping the admin on every new enquiry |
| **Email (SMTP / Gmail API / SendGrid)** | Send email notifications to the admin inbox |
| **Payment gateway (Stripe / Razorpay / PayPal)** | Accept payments from the pricing cards |

### Export & Download

Click **Build Package** → **Download ZIP** to receive:

```
generated_website_package.zip
├── frontend/
│   └── index.html          ← Your complete website (open in any browser)
├── backend/
│   ├── config.json         ← All credentials/settings from the wizard
│   └── backend_stub.py     ← Python scaffold ready to wire up
├── run_localhost.bat        ← Double-click to preview locally (Windows)
└── README_generated.txt    ← Deployment guide tailored to your inputs
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install streamlit requests
```

### 2. Run the app

```bash
streamlit run app.py
```

The wizard opens at `http://localhost:8501`.

### 3. Generate your site

1. Fill in the wizard fields (all are optional — defaults are sensible).
2. Choose **Mock AI** for an instant result, or **Claude API** with your Anthropic key for a richer AI-generated site.
3. Click **⚡ Generate Website**.
4. Iterate with the revision prompt box.
5. Click **Backend Setup →** to configure integrations.
6. Click **📦 Build Package** and download the ZIP.

---

## AI Providers

| Provider | What it does | When to use |
|----------|-------------|-------------|
| **Mock AI** | Generates a deterministic, well-styled HTML site locally | Quick preview; no API key needed |
| **Claude API** | Sends your inputs to `claude-opus-4-5` for a bespoke, fully custom site | When you have an Anthropic API key and want richer output |

Your API key is used only within the current browser session and is never persisted.

---

## File Reference

| File | Purpose |
|------|---------|
| `app.py` | The entire Streamlit application |
| `README.md` | This file |

---

## Architecture Notes

- **All state** lives in `st.session_state`, keyed by field name. The `initialize_state()` function seeds defaults on first load.
- **Two wizard screens** (`frontend_wizard`, `backend_wizard`) are routed via `st.session_state["step"]`.
- **Mock AI** (`mock_ai_frontend`) generates HTML using Python f-strings — no network call, no latency.
- **Claude API** (`claude_generate`) calls `POST /v1/messages` with a structured prompt; falls back to Mock AI on any error so the app never breaks.
- **`export_zip()`** bundles the HTML, a `config.json` (all backend fields), a `backend_stub.py` scaffold, a `.bat` launcher, and a README into an in-memory ZIP returned as bytes.
- The generated site is a **single standalone HTML file** with embedded CSS and JS — no build step, no dependencies.

---

## Customisation

- **Add palettes** — extend the `PALETTES` dict with any hex values.
- **Add templates** — append to the `TEMPLATES` list with Unsplash (or your own) preview URLs.
- **Change the AI model** — edit the `"model"` key in `claude_generate()`.
- **Extend backend fields** — add keys to `build_backend_config()` and the corresponding `st.text_input` calls in `backend_wizard()`.

---

## Requirements

- Python ≥ 3.9
- `streamlit`
- `requests`
- Internet access (for Google Fonts, Unsplash preview images, and optional Claude API calls)

---

*Generated with ❤️ by AI Website Maker Wizard*
