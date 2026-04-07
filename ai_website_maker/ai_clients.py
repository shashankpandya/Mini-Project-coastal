from typing import Tuple

import requests
import streamlit as st

from .data import PALETTES
def mock_ai_frontend(prompt: str) -> str:
    del prompt
    palette = PALETTES[st.session_state["palette_name"]]
    cards = "\n".join([
        f"""<article class="card">
              <span class="pill">{p['type']}</span>
              <h3>{p['name']}</h3>
              <p>{p['description']}</p>
              <div class="price">${float(p['price']):.2f}</div>
              <button class="cta-btn">Choose Plan</button>
            </article>"""
        for p in st.session_state["products"]
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
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
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      color: var(--text);
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: var(--bg);
    }}
    nav {{
      position: sticky; top: 0; z-index: 99;
      background: rgba(255,255,255,0.88);
      backdrop-filter: blur(12px);
      padding: 14px 5%;
      display: flex; justify-content: space-between; align-items: center;
      border-bottom: 1px solid rgba(0,0,0,0.07);
    }}
    nav .logo {{ font-weight: 700; font-size: 1.2rem; color: var(--primary); }}
    nav a {{ text-decoration: none; color: var(--text); margin-left: 24px; font-size: 0.9rem; }}
    .container {{ width: min(1080px, 92%); margin: 0 auto; }}
    /* Hero */
    .hero {{
      min-height: 88vh;
      display: flex; align-items: center;
      background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 60%, var(--bg) 100%);
      padding: 80px 5%;
    }}
    .hero-content {{ max-width: 640px; animation: fadeUp 0.8s ease both; }}
    .hero h1 {{ font-size: clamp(2rem, 5vw, 3.4rem); color: #fff; line-height: 1.18; margin-bottom: 16px; }}
    .hero p {{ color: rgba(255,255,255,0.8); font-size: 1.05rem; line-height: 1.65; margin-bottom: 28px; }}
    .hero-btns {{ display: flex; gap: 12px; flex-wrap: wrap; }}
    .cta-btn {{
      background: var(--accent); color: #fff; border: none;
      padding: 13px 26px; border-radius: 999px;
      font-weight: 600; cursor: pointer; font-size: 0.95rem;
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .cta-btn:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }}
    .cta-btn.alt {{
      background: rgba(255,255,255,0.15);
      border: 2px solid rgba(255,255,255,0.4);
      backdrop-filter: blur(8px);
    }}
    /* Sections */
    .section {{ padding: 80px 5%; }}
    .section-title {{ font-size: 1.9rem; font-weight: 700; color: var(--primary); margin-bottom: 8px; }}
    .section-sub {{ color: #6b7280; margin-bottom: 36px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }}
    .card {{
      background: var(--surface);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.07);
      transition: transform 0.25s, box-shadow 0.25s;
      animation: fadeUp 0.6s ease both;
    }}
    .card:hover {{ transform: translateY(-5px); box-shadow: 0 12px 40px rgba(0,0,0,0.12); }}
    .pill {{
      display: inline-block; padding: 4px 12px;
      border-radius: 999px; background: var(--bg);
      font-size: 0.78rem; font-weight: 600; color: var(--secondary);
      margin-bottom: 12px;
    }}
    .card h3 {{ font-size: 1.05rem; margin-bottom: 8px; color: var(--primary); }}
    .card p {{ font-size: 0.9rem; color: #6b7280; line-height: 1.55; }}
    .price {{ font-size: 1.7rem; font-weight: 800; color: var(--secondary); margin: 14px 0; }}
    .card .cta-btn {{ width: 100%; text-align: center; margin-top: 8px; }}
    /* Enquiry */
    .enquiry-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }}
    .panel {{
      background: var(--surface);
      border-radius: 20px;
      padding: 32px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    }}
    .panel h2 {{ font-size: 1.4rem; color: var(--primary); margin-bottom: 20px; }}
    input, textarea {{
      width: 100%; padding: 12px 14px; margin-bottom: 12px;
      border: 1px solid #e2e8f0; border-radius: 10px;
      font-family: inherit; font-size: 0.9rem;
      transition: border-color 0.2s, box-shadow 0.2s;
      outline: none;
    }}
    input:focus, textarea:focus {{
      border-color: var(--secondary);
      box-shadow: 0 0 0 3px rgba(0,0,0,0.06);
    }}
    textarea {{ resize: vertical; min-height: 110px; }}
    .contact-item {{ display: flex; gap: 12px; align-items: flex-start; margin-bottom: 16px; }}
    .contact-icon {{
      width: 40px; height: 40px; border-radius: 50%;
      background: var(--bg); display: flex; align-items: center; justify-content: center;
      font-size: 1.1rem; flex-shrink: 0;
    }}
    /* Footer */
    footer {{
      background: var(--primary);
      color: rgba(255,255,255,0.7);
      text-align: center;
      padding: 32px;
      font-size: 0.88rem;
    }}
    /* Animations */
    @keyframes fadeUp {{
      from {{ opacity: 0; transform: translateY(22px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @media (max-width: 768px) {{
      .enquiry-grid {{ grid-template-columns: 1fr; }}
      .hero h1 {{ font-size: 2rem; }}
    }}
  </style>
</head>
<body>
  <nav>
    <div class="logo">{st.session_state['business_type'] or 'My Business'}</div>
    <div>
      <a href="#products">Services</a>
      <a href="#enquiry">Contact</a>
    </div>
  </nav>

  <header class="hero">
    <div class="container">
      <div class="hero-content">
        <h1>{st.session_state['business_type'] or 'Your Business'}, built for growth.</h1>
        <p>{st.session_state['brand_story'] or 'A clean, conversion-friendly website generated by AI Website Maker.'}</p>
        <div class="hero-btns">
          <button class="cta-btn" onclick="document.querySelector('#products').scrollIntoView({{behavior:'smooth'}})">Explore Services</button>
          <button class="cta-btn alt" onclick="document.querySelector('#enquiry').scrollIntoView({{behavior:'smooth'}})">Get in Touch</button>
        </div>
      </div>
    </div>
  </header>

  <section id="products" class="section" style="background:var(--bg)">
    <div class="container">
      <h2 class="section-title">Products & Services</h2>
      <p class="section-sub">Everything you need to get started.</p>
      <div class="grid">{cards}</div>
    </div>
  </section>

  <section class="section" style="background:var(--surface)">
    <div class="container">
      <h2 class="section-title">Why clients choose us</h2>
      <p class="section-sub">Trusted by teams of all sizes.</p>
      <div class="grid">
        <div class="card"><h3>Fast Onboarding</h3><p>Get started in under 24 hours with our guided setup process.</p></div>
        <div class="card"><h3>Transparent Pricing</h3><p>No hidden fees. Clear deliverables agreed upfront.</p></div>
        <div class="card"><h3>Dedicated Support</h3><p>Real humans on hand to answer questions and solve problems.</p></div>
        <div class="card"><h3>Proven Results</h3><p>"Excellent team and transparent process from day one."</p></div>
      </div>
    </div>
  </section>

  <section id="enquiry" class="section" style="background:var(--bg)">
    <div class="container">
      <h2 class="section-title">Get in Touch</h2>
      <p class="section-sub">We usually respond within 2 business hours.</p>
      <div class="enquiry-grid">
        <div class="panel">
          <h2>Send an Enquiry</h2>
          <input placeholder="Your name" />
          <input placeholder="Phone number" />
          <input placeholder="Email address" />
          <textarea placeholder="{st.session_state['enquiry_placeholder']}"></textarea>
          <button class="cta-btn" style="width:100%">Submit Enquiry</button>
        </div>
        <div class="panel">
          <h2>Contact Details</h2>
          <div class="contact-item">
            <div class="contact-icon">ðŸ“ž</div>
            <div><strong>Phone</strong><br>{st.session_state['company_phone'] or 'Not configured'}</div>
          </div>
          <div class="contact-item">
            <div class="contact-icon">âœ‰ï¸</div>
            <div><strong>Email</strong><br>{st.session_state['company_email'] or 'Not configured'}</div>
          </div>
          <div class="contact-item">
            <div class="contact-icon">ðŸ¢</div>
            <div><strong>Team</strong><br>{st.session_state['owner_name'] or 'Business Owner'} Â· {st.session_state['team_size']} people</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <footer>
    <p>{st.session_state['owner_name'] or 'Business Owner'} &bull; {st.session_state['business_type'] or 'My Business'} &bull; Template: {st.session_state['template_name']}</p>
    <p style="margin-top:8px;font-size:0.78rem;opacity:0.5">Generated by AI Website Maker</p>
  </footer>
</body>
</html>""".strip()


def claude_generate(prompt: str) -> Tuple[bool, str]:
    key = st.session_state.get("claude_api_key", "").strip()
    if not key:
        return False, "Claude API key is missing."

    body = {
        "model": "claude-opus-4-5",
        "max_tokens": 8192,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers, json=body, timeout=120,
        )
        if resp.status_code >= 300:
            return False, f"Claude API error {resp.status_code}: {resp.text[:300]}"
        data = resp.json()
        html = "\n".join(
            x.get("text", "") for x in data.get("content", []) if x.get("type") == "text"
        ).strip()
        # Strip markdown fences if Claude wrapped the output
        if html.startswith("```"):
            html = "\n".join(html.split("\n")[1:])
        if html.endswith("```"):
            html = "\n".join(html.split("\n")[:-1])
        return (True, html) if html else (False, "Claude returned no text.")
    except Exception as exc:
        return False, f"Claude API call failed: {exc}"



