# Coastal Project

This repository contains a modular Streamlit app for generating business websites.

## Project layout

- app.py: Entry point.
- ai_website_maker/: Main modular package.
- Previuos Versuion/: Legacy monolithic version kept for reference.

Main package modules:

- ai_website_maker/app_runner.py: App bootstrap and page routing.
- ai_website_maker/pages_frontend.py: Frontend wizard page.
- ai_website_maker/pages_backend.py: Backend setup page.
- ai_website_maker/pipelines.py: Generation and export pipelines.
- ai_website_maker/ai_clients.py: Mock and Claude provider clients.
- ai_website_maker/prompt_builder.py: Prompt construction logic.
- ai_website_maker/ui_components.py: Shared Streamlit UI widgets.
- ai_website_maker/styles.py: Global CSS injection.
- ai_website_maker/state.py: Session state initialization.
- ai_website_maker/data.py: Palettes, templates, and defaults.

## Requirements

- Python 3.10+
- pip

Python packages used by the app:

- streamlit
- requests

## Setup

1. Open a terminal in the project root.
2. (Optional) Create and activate a virtual environment.
3. Install dependencies:

pip install streamlit requests

## Run the app

From the project root, run:

streamlit run app.py

Then open the URL shown in the terminal (usually http://localhost:8501).

## Usage flow

1. Fill in frontend wizard details (business, design, products, contact).
2. Generate with Mock AI or Claude API.
3. Refine output with revision prompts.
4. Go to Backend Setup to configure integrations.
5. Build and download the generated package.

## Notes

- app.py is intentionally minimal and only calls run_app().
- The legacy implementation is in Previuos Versuion/.
- If you use Claude API mode, provide your API key in the app UI.
