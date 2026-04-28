import streamlit as st
import json
from utils.claude_client import call_claude_json
from utils.db import save_scan

SYSTEM = """You are a research duplication detection engine simulating BERT sentence-transformer similarity scoring.
Respond ONLY in valid JSON — no markdown, no text outside the JSON.

Schema:
{
  "originality_score": <0-100 integer>,
  "risk_level": "Low" | "Medium" | "High",
  "similar_papers": [
    { "title": "<paper title>", "year": <year>, "similarity_pct": <0-100>, "venue": "<journal/conf>" }
  ],
  "overlap_keywords": ["kw1","kw2","kw3","kw4"],
  "verdict": "<2-sentence assessment>",
  "recommendation": "<1 concrete actionable suggestion>"
}

Return 3-5 similar papers from real published literature. Be accurate and specific."""

def render():
    st.markdown("""
    <div class="rg-card">
        <div class="rg-card-title">Topic Scanner</div>
        <div class="rg-card-desc">
            Enter your research topic. The ML model analyzes semantic similarity against
            published literature, detects overlaps, and scores originality using BERT-style embeddings.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_area("Your Research Topic", height=100,
            placeholder="e.g. Using transformer models to predict antibiotic resistance in multi-drug resistant bacteria...")
    with col2:
        domain = st.selectbox("Research Domain", [
            "Biomedical & Health Sciences",
            "Computer Science & AI",
            "Natural Language Processing",
            "Climate & Environmental Science",
            "Physics & Materials Science",
            "Social Sciences & Psychology",
        ])
        st.markdown("<br>", unsafe_allow_html=True)
        run = st.button("✦ Analyze Topic", use_container_width=True)

    if run:
        if not topic.strip():
            st.warning("Please enter a research topic.")
            return
        with st.spinner("Analyzing semantic similarity..."):
            try:
                data = call_claude_json(SYSTEM, f'Research topic: "{topic}"\nDomain: {domain}')
                _render_results(data, topic, domain)
                save_scan(topic, domain, data["originality_score"], data["risk_level"], json.dumps(data))
                st.success("✦ Saved to your tracker!")
            except Exception as e:
                st.error(f"Analysis failed: {e}")

def _render_results(d, topic, domain):
    score = d["originality_score"]
    risk  = d["risk_level"]
    risk_color = "#6fcf8a" if risk == "Low" else "#FFD700" if risk == "Medium" else "#e87868"

    c1, c2, c3 = st.columns(3)
    c1.metric("Originality Score", f"{score}/100")
    c2.metric("Risk Level", risk)
    c3.metric("Similar Papers", len(d["similar_papers"]))

    st.markdown("---")

    st.markdown("**Similar Papers Detected**")
    for p in d["similar_papers"]:
        sim = p["similarity_pct"]
        badge = "badge-high" if sim >= 60 else "badge-med" if sim >= 35 else "badge-low"
        st.markdown(f"""
        <div class="rg-result" style="margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px">
                <div>
                    <div style="font-size:13px;font-weight:700;color:#fffbe6">{p['title']}</div>
                    <div style="font-size:11px;color:#7a6030;margin-top:3px">{p['venue']} · {p['year']}</div>
                </div>
                <span class="{badge}" style="flex-shrink:0">{sim}% match</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("**Overlapping Keywords**")
    chips = " ".join([f'<span class="chip">{k}</span>' for k in d["overlap_keywords"]])
    st.markdown(chips, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div class="rg-result">
        <div class="rg-result-label">Verdict</div>
        <div style="font-size:13px;line-height:1.75;color:#fff8d6">{d['verdict']}</div>
        <div style="margin-top:12px;padding:10px 14px;background:rgba(255,215,0,0.06);border-radius:8px;
                    border-left:2px solid rgba(255,215,0,0.3);font-size:12px;color:#7a6030">
            💡 {d['recommendation']}
        </div>
    </div>
    """, unsafe_allow_html=True)
