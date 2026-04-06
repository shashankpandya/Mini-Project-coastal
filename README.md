# AI Website Maker Wizard (Business/Portfolio)

This project is a step-by-step website maker wizard built with Streamlit.

## What it does

- Runs from a Python script and opens in a browser window.
- Collects website intent (business/personal), identity, team size, palette, and template preferences.
- Lets users upload product/service and portfolio/home images (drag-and-drop upload supported by Streamlit uploader).
- Captures support/enquiry configuration (company phone/email and enquiry fields).
- Generates frontend HTML via:
  - Mock AI mode (default, no API key needed), or
  - Claude API mode (if API key is provided).
- Supports iterative changes with user prompts until satisfied.
- Includes backend setup wizard inputs for Google integration, WhatsApp alerts, email alerts, and payment gateway setup.
- Exports a zip package that runs locally.

## Quick start

1. Create and activate your Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   streamlit run app.py
   ```
4. Open the URL shown by Streamlit (usually `http://localhost:8501`).

## Notes

- Backend integrations are scaffolded in this step (configuration-driven), as requested.
- Real production backend wiring and secure secret management can be implemented in the next step.
