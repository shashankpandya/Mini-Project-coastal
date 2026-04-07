import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');
    
        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }
    
        /* â”€â”€ Page background â”€â”€ */
        .stApp {
            background: #0a0a0f;
            color: #e8e8f0;
        }
    
        /* â”€â”€ Hide Streamlit chrome â”€â”€ */
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1100px; }
    
        /* â”€â”€ Animated page title â”€â”€ */
        .wizard-title {
            font-family: 'DM Serif Display', Georgia, serif;
            font-size: clamp(2rem, 5vw, 3.2rem);
            font-weight: 400;
            background: linear-gradient(135deg, #a78bfa, #f472b6, #fb923c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmer 4s ease-in-out infinite alternate;
            background-size: 200% 200%;
            margin-bottom: 0.25rem;
        }
        @keyframes shimmer {
            0%   { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
    
        .wizard-caption {
            color: #6b7180;
            font-size: 0.95rem;
            letter-spacing: 0.02em;
            margin-bottom: 2.5rem;
        }
    
        /* â”€â”€ Section headers â”€â”€ */
        .section-header {
            display: flex;
            align-items: center;
            gap: 10px;
            font-family: 'DM Serif Display', Georgia, serif;
            font-size: 1.35rem;
            font-weight: 400;
            color: #c4c4d8;
            border-bottom: 1px solid #1e1e2e;
            padding-bottom: 10px;
            margin: 2.2rem 0 1rem;
        }
        .section-num {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px; height: 28px;
            border-radius: 50%;
            background: linear-gradient(135deg, #7c3aed, #db2777);
            color: white;
            font-size: 0.8rem;
            font-weight: 700;
            font-family: 'DM Sans', sans-serif;
            flex-shrink: 0;
        }
    
        /* â”€â”€ Input fields â”€â”€ */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {
            background: #12121c !important;
            border: 1px solid #2a2a3d !important;
            border-radius: 10px !important;
            color: #e8e8f0 !important;
            transition: border-color 0.25s ease, box-shadow 0.25s ease;
        }
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #7c3aed !important;
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
        }
    
        /* â”€â”€ Labels â”€â”€ */
        .stTextInput label, .stTextArea label,
        .stSelectbox label, .stRadio label,
        .stFileUploader label {
            color: #9090a8 !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
        }
    
        /* â”€â”€ Primary button â”€â”€ */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #7c3aed, #db2777) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 600 !important;
            letter-spacing: 0.03em !important;
            padding: 0.65rem 1.5rem !important;
            transition: opacity 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
            box-shadow: 0 4px 20px rgba(124, 58, 237, 0.35) !important;
        }
        .stButton > button[kind="primary"]:hover {
            opacity: 0.92 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 8px 30px rgba(124, 58, 237, 0.5) !important;
        }
        .stButton > button[kind="primary"]:active {
            transform: translateY(0px) !important;
        }
    
        /* â”€â”€ Secondary buttons â”€â”€ */
        .stButton > button:not([kind="primary"]) {
            background: #12121c !important;
            border: 1px solid #2a2a3d !important;
            border-radius: 12px !important;
            color: #c4c4d8 !important;
            font-weight: 500 !important;
            transition: border-color 0.2s ease, background 0.2s ease, transform 0.15s ease !important;
        }
        .stButton > button:not([kind="primary"]):hover {
            background: #1a1a2e !important;
            border-color: #7c3aed !important;
            transform: translateY(-1px) !important;
        }
    
        /* â”€â”€ Download button â”€â”€ */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #065f46, #047857) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 20px rgba(4, 120, 87, 0.3) !important;
            transition: opacity 0.2s ease, transform 0.15s ease !important;
        }
        .stDownloadButton > button:hover {
            opacity: 0.9 !important;
            transform: translateY(-1px) !important;
        }
    
        /* â”€â”€ Expanders (backend wizard) â”€â”€ */
        .streamlit-expanderHeader {
            background: #12121c !important;
            border: 1px solid #2a2a3d !important;
            border-radius: 12px !important;
            color: #c4c4d8 !important;
            font-weight: 500 !important;
            transition: border-color 0.2s ease;
        }
        .streamlit-expanderHeader:hover {
            border-color: #7c3aed !important;
        }
        .streamlit-expanderContent {
            background: #0d0d18 !important;
            border: 1px solid #2a2a3d !important;
            border-top: none !important;
            border-radius: 0 0 12px 12px !important;
        }
    
        /* â”€â”€ Success / info / warning banners â”€â”€ */
        .stSuccess {
            background: #0d2318 !important;
            border: 1px solid #065f46 !important;
            border-radius: 10px !important;
            color: #6ee7b7 !important;
        }
        .stInfo {
            background: #0d1a30 !important;
            border: 1px solid #1e3a5f !important;
            border-radius: 10px !important;
            color: #93c5fd !important;
        }
        .stWarning {
            background: #1f1500 !important;
            border: 1px solid #78350f !important;
            border-radius: 10px !important;
            color: #fcd34d !important;
        }
    
        /* â”€â”€ Radio buttons â”€â”€ */
        .stRadio > div {
            gap: 12px !important;
        }
        .stRadio > div > label {
            background: #12121c !important;
            border: 1px solid #2a2a3d !important;
            border-radius: 10px !important;
            padding: 8px 16px !important;
            transition: border-color 0.2s ease;
            color: #c4c4d8 !important;
            text-transform: none !important;
            font-size: 0.9rem !important;
            letter-spacing: 0 !important;
        }
        .stRadio > div > label:hover {
            border-color: #7c3aed !important;
        }
    
        /* â”€â”€ Data editor â”€â”€ */
        .stDataEditor {
            border: 1px solid #2a2a3d !important;
            border-radius: 12px !important;
            overflow: hidden;
        }
    
        /* â”€â”€ File uploader â”€â”€ */
        .stFileUploader > div {
            background: #12121c !important;
            border: 1px dashed #2a2a3d !important;
            border-radius: 12px !important;
            transition: border-color 0.2s ease;
        }
        .stFileUploader > div:hover {
            border-color: #7c3aed !important;
        }
    
        /* â”€â”€ Progress bar â”€â”€ */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #7c3aed, #db2777, #fb923c) !important;
            background-size: 200% 100% !important;
            animation: progress-shimmer 1.5s linear infinite;
            border-radius: 99px !important;
        }
        @keyframes progress-shimmer {
            0%   { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
    
        /* â”€â”€ Caption / help text â”€â”€ */
        .stCaption, small, .stMarkdown small {
            color: #555570 !important;
        }
    
        /* â”€â”€ Palette swatch card â”€â”€ */
        .swatch-wrap {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin: 12px 0 6px;
        }
        .swatch {
            flex: 1;
            min-width: 80px;
            padding: 12px 10px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.07);
            font-size: 0.75rem;
            font-weight: 600;
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .swatch:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }
    
        /* â”€â”€ Template card â”€â”€ */
        .template-card {
            background: #12121c;
            border: 1px solid #2a2a3d;
            border-radius: 14px;
            overflow: hidden;
            transition: border-color 0.2s ease, transform 0.2s ease;
        }
        .template-card:hover { border-color: #7c3aed; transform: translateY(-2px); }
        .template-card img { width: 100%; height: 140px; object-fit: cover; }
        .template-card-body { padding: 12px 14px; }
    
        /* â”€â”€ Spinner override â”€â”€ */
        .stSpinner > div { border-top-color: #7c3aed !important; }
    
        /* â”€â”€ Divider â”€â”€ */
        hr { border-color: #1e1e2e !important; }
    
        /* â”€â”€ Step indicator bar at the top â”€â”€ */
        .step-bar {
            display: flex;
            align-items: center;
            gap: 0;
            margin-bottom: 2.5rem;
            background: #12121c;
            border: 1px solid #2a2a3d;
            border-radius: 14px;
            padding: 16px 24px;
        }
        .step-item {
            display: flex;
            align-items: center;
            gap: 8px;
            flex: 1;
            position: relative;
        }
        .step-item:not(:last-child)::after {
            content: '';
            position: absolute;
            right: 0;
            width: 1px;
            height: 24px;
            background: #2a2a3d;
        }
        .step-dot {
            width: 32px; height: 32px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 0.8rem; font-weight: 700;
            flex-shrink: 0;
        }
        .step-dot.active {
            background: linear-gradient(135deg, #7c3aed, #db2777);
            color: white;
            box-shadow: 0 0 16px rgba(124,58,237,0.4);
        }
        .step-dot.done {
            background: #065f46;
            color: #6ee7b7;
        }
        .step-dot.idle {
            background: #1e1e2e;
            color: #555570;
        }
        .step-label {
            font-size: 0.78rem;
            font-weight: 500;
            color: #6b7180;
        }
        .step-label.active { color: #c4c4d8; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    

