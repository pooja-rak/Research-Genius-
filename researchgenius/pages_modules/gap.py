import streamlit as st
from utils.api import call_claude, parse_json
from utils.db import save_result

def render():
    st.markdown("""<div style="font-family:'Pinyon Script',cursive;font-size:2.5rem;color:#FFD700;margin-bottom:0.2rem">Gap Suggester</div>
    <div style="font-size:0.8rem;color:#7a6030;margin-bottom:1.5rem">TF-IDF ranking · Semantic clustering · Underexplored directions</div>""", unsafe_allow_html=True)

    with st.form("gap_form"):
        topic = st.text_area("Your Research Area", height=100,
            placeholder="e.g. Machine learning methods for early detection of Alzheimer's disease using MRI scans and cognitive assessments...")
        col1, col2 = st.columns(2)
        with col1:
            depth = st.selectbox("Analysis Depth", ["Quick scan (3 gaps)", "Standard (5 gaps)", "Deep dive (5 gaps + methodology)"])
        with col2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("✦ Find Research Gaps", use_container_width=True)

    if submitted:
        if not topic.strip():
            st.warning("Please describe your research area."); return
        n = 3 if "Quick" in depth else 5
        incl_method = "Deep" in depth

        sys = f"""You are a research gap analysis engine combining TF-IDF ranking with semantic clustering.
Respond ONLY in valid JSON — no markdown.

Schema:
{{
  "gaps": [
    {{
      "id": <1-{n}>,
      "title": "<short gap title, max 6 words>",
      "description": "<2-3 sentences explaining the gap and why it matters>",
      "tfidf_score": <0.0-1.0 float, 2 decimals>,
      "novelty": "High" | "Medium" | "Low",
      {"\"methodology\": \"<suggested method to address this gap>\"," if incl_method else ""}
      "keywords": ["kw1","kw2","kw3"],
      "feasibility": "High" | "Medium" | "Low"
    }}
  ],
  "cluster_summary": "<1 sentence about the overall research landscape>"
}}

Return exactly {n} gaps. Make them genuinely distinct and researchable."""

        with st.spinner(f"Running TF-IDF + semantic clustering for {n} gaps..."):
            raw = call_claude(sys, f"Research area: \"{topic}\"")
        if not raw: return
        d = parse_json(raw)
        if not d: return

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"""<div style="background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.15);border-radius:10px;padding:0.8rem 1rem;margin-bottom:1rem;font-size:0.8rem;color:#7a6030">🔬 {d.get('cluster_summary','')}</div>""", unsafe_allow_html=True)

        cols = st.columns(2)
        for i, g in enumerate(d.get("gaps", [])):
            with cols[i % 2]:
                nc_color = "#6fcf8a" if g.get("novelty") == "High" else "#FFD700" if g.get("novelty") == "Medium" else "#e87868"
                kw_html = " ".join([f'<span style="display:inline-block;padding:2px 8px;border-radius:999px;background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.2);color:#FFD700;font-size:0.65rem;font-weight:700;margin:2px">{k}</span>' for k in g.get("keywords", [])])
                method_html = f'<div style="margin-top:0.5rem;font-size:0.72rem;color:#FFA500">→ {g.get("methodology","")}</div>' if incl_method and g.get("methodology") else ""
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,215,0,0.14);border-radius:12px;padding:1.2rem;margin-bottom:1rem;height:240px;overflow:hidden">
                    <div style="font-family:'Pinyon Script',cursive;font-size:2.2rem;color:#FF8C00;line-height:1">{g.get('id','')}</div>
                    <div style="font-size:0.85rem;font-weight:800;color:#fffbe6;margin:0.3rem 0">{g.get('title','')}</div>
                    <div style="display:flex;gap:8px;margin:0.3rem 0;flex-wrap:wrap">
                        <span style="background:rgba(255,255,255,0.05);border:1px solid {nc_color}44;border-radius:999px;padding:1px 8px;color:{nc_color};font-size:0.65rem;font-weight:800">{g.get('novelty','')} novelty</span>
                        <span style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,215,0,0.2);border-radius:999px;padding:1px 8px;color:#7a6030;font-size:0.65rem">TF-IDF: {g.get('tfidf_score','')}</span>
                    </div>
                    <div style="font-size:0.75rem;color:#7a6030;line-height:1.5">{g.get('description','')[:180]}</div>
                    {method_html}
                    <div style="margin-top:0.5rem">{kw_html}</div>
                </div>""", unsafe_allow_html=True)

        save_result("gap_suggester", topic, d, len(d.get("gaps", [])) * 20)
        st.success("✓ Saved to tracker")
