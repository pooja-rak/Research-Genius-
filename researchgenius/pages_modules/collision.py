import streamlit as st
from utils.api import call_claude, parse_json
from utils.db import save_result

def render():
    st.markdown("""<div style="font-family:'Pinyon Script',cursive;font-size:2.5rem;color:#FFD700;margin-bottom:0.2rem">Collision Alert System</div>
    <div style="font-size:0.8rem;color:#7a6030;margin-bottom:1.5rem">Bi-directional conflict detection · Severity ranking · Pivot suggestions</div>""", unsafe_allow_html=True)

    with st.form("col_form"):
        abstract = st.text_area("Your Research Abstract / Proposal", height=150,
            placeholder="Paste your full abstract, research proposal, or a detailed description of your work...")
        col1, col2 = st.columns(2)
        with col1:
            scope = st.selectbox("Check Against", ["All published literature", "Recent papers (2020–2025)", "Top-tier venues only"])
        with col2:
            sens = st.selectbox("Alert Sensitivity", ["Strict (≥40% overlap)", "Medium (≥60% overlap)", "Lenient (≥75% overlap)"])
        submitted = st.form_submit_button("⚡ Run Collision Check", use_container_width=True)

    if submitted:
        if not abstract.strip():
            st.warning("Please paste your abstract."); return
        thresh = 40 if "Strict" in sens else 60 if "Medium" in sens else 75

        sys = f"""You are a research collision detection engine detecting bi-directional conflicts.
Respond ONLY in valid JSON — no markdown.

Schema:
{{
  "summary": {{"total_alerts":<n>,"high":<n>,"medium":<n>,"low":<n>,"originality_pct":<0-100>}},
  "alerts": [
    {{
      "severity": "high"|"medium"|"low",
      "title": "<collision title>",
      "conflicting_work": "<Author et al., Year — real or plausible venue>",
      "overlap_pct": <integer>,
      "overlap_type": "methodology"|"hypothesis"|"dataset"|"findings"|"framing",
      "description": "<2 sentences describing the collision>",
      "pivot": "<1 concrete suggestion to differentiate>",
      "keywords": ["kw1","kw2"]
    }}
  ]
}}

Scope: {scope}. Sensitivity threshold: {thresh}% overlap. Return 3-6 alerts ordered high→low severity. Be specific."""

        with st.spinner("Scanning for collisions across literature..."):
            raw = call_claude(sys, f"Abstract:\n\"{abstract}\"")
        if not raw: return
        d = parse_json(raw)
        if not d: return

        s = d.get("summary", {})
        orig = s.get("originality_pct", 0)

        st.markdown("<hr>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Originality", f"{orig}%")
        c2.metric("Total Alerts", s.get("total_alerts", 0))
        c3.metric("🔴 High", s.get("high", 0))
        c4.metric("🟡 Medium", s.get("medium", 0))

        st.progress(orig / 100)
        st.markdown("<hr>", unsafe_allow_html=True)

        for a in d.get("alerts", []):
            sev = a.get("severity", "low")
            css = "alert-high" if sev == "high" else "alert-med" if sev == "medium" else "alert-low"
            icon = "🔴" if sev == "high" else "🟡" if sev == "medium" else "🟢"
            badge_color = "#e87868" if sev == "high" else "#FFD700" if sev == "medium" else "#6fcf8a"
            kw_html = " ".join([f'<span style="display:inline-block;padding:1px 8px;border-radius:999px;background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.15);color:#FFD700;font-size:0.65rem;font-weight:700;margin:1px">{k}</span>' for k in a.get("keywords", [])])

            st.markdown(f"""
            <div class="{css}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;flex-wrap:wrap;gap:8px">
                    <span style="background:rgba(255,255,255,0.05);border:1px solid {badge_color}44;border-radius:999px;padding:2px 10px;color:{badge_color};font-size:0.65rem;font-weight:800;text-transform:uppercase;letter-spacing:1px">{icon} {sev.upper()} · {a.get('overlap_pct',0)}% overlap</span>
                    <span style="font-size:0.7rem;color:#7a6030;font-style:italic">{a.get('overlap_type','').replace('_',' ').title()}</span>
                </div>
                <div style="font-size:0.9rem;font-weight:800;color:#fffbe6;margin-bottom:0.3rem">{a.get('title','')}</div>
                <div style="font-size:0.72rem;color:#FFA500;font-weight:700;margin-bottom:0.6rem">{a.get('conflicting_work','')}</div>
                <div style="font-size:0.8rem;color:#7a6030;line-height:1.6;margin-bottom:0.6rem">{a.get('description','')}</div>
                <div style="background:rgba(255,215,0,0.05);border-left:2px solid rgba(255,215,0,0.3);border-radius:0 8px 8px 0;padding:0.6rem 0.8rem;margin-bottom:0.6rem">
                    <span style="font-size:0.65rem;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#FFA500">Pivot: </span>
                    <span style="font-size:0.78rem;color:#fff8d6">{a.get('pivot','')}</span>
                </div>
                <div>{kw_html}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""<div style="font-size:0.72rem;color:#7a6030;line-height:1.7;margin-top:0.5rem;padding:0.8rem;background:rgba(255,255,255,0.02);border-radius:8px">
        ℹ High severity = significant methodological or hypothesis overlap — address these before submission. Medium/low = adjacent work that should appear in your Related Work section.</div>""", unsafe_allow_html=True)

        save_result("collision", abstract[:80], d, orig)
        st.success("✓ Saved to tracker")
