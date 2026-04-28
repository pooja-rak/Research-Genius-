import streamlit as st
from utils.api import call_claude, parse_json
from utils.db import save_result

SYSTEM = """You are a research duplication detection engine simulating BERT sentence-transformer similarity scoring.
Respond ONLY in valid JSON — no markdown, no extra text outside JSON.

Schema:
{
  "originality_score": <0-100 integer>,
  "risk_level": "Low" | "Medium" | "High",
  "similar_papers": [
    {"title":"<paper title>","year":<year>,"similarity_pct":<0-100>,"venue":"<journal/conf>","authors":"<Author et al.>"}
  ],
  "overlap_keywords": ["kw1","kw2","kw3"],
  "verdict": "<2-sentence assessment>",
  "recommendation": "<1 actionable suggestion to differentiate the work>"
}

Return 3-5 similar papers from real published literature. Be accurate to the domain."""

def render():
    st.markdown("""<div style="font-family:'Pinyon Script',cursive;font-size:2.5rem;color:#FFD700;margin-bottom:0.2rem">Topic Scanner</div>
    <div style="font-size:0.8rem;color:#7a6030;margin-bottom:1.5rem">Semantic similarity check · BERT-style embeddings · Originality scoring</div>""", unsafe_allow_html=True)

    with st.form("scan_form"):
        topic = st.text_area("Your Research Topic", height=100,
            placeholder="e.g. Using transformer models to predict antibiotic resistance in multi-drug resistant bacteria using genomic sequence data...")
        col1, col2 = st.columns(2)
        with col1:
            domain = st.selectbox("Research Domain", [
                "Biomedical & Health Sciences", "Computer Science & AI",
                "Natural Language Processing", "Climate & Environmental Science",
                "Physics & Materials Science", "Social Sciences & Psychology"
            ])
        with col2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("✦ Analyze Topic", use_container_width=True)

    if submitted:
        if not topic.strip():
            st.warning("Please enter a research topic."); return

        with st.spinner("Analyzing semantic similarity across literature..."):
            raw = call_claude(SYSTEM, f"Research topic: \"{topic}\"\nDomain: {domain}")
        if not raw: return
        d = parse_json(raw)
        if not d: return

        score = d.get("originality_score", 0)
        risk  = d.get("risk_level", "Unknown")

        st.markdown("<hr>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Originality Score", f"{score}/100")
        c2.metric("Risk Level", risk)
        c3.metric("Similar Papers", len(d.get("similar_papers", [])))

        st.progress(score / 100)

        st.markdown("#### Similar Papers Detected")
        for p in d.get("similar_papers", []):
            pct = p.get("similarity_pct", 0)
            color = "#e87868" if pct >= 60 else "#FFD700" if pct >= 35 else "#6fcf8a"
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,215,0,0.1);border-radius:10px;padding:0.9rem;margin-bottom:0.5rem;display:flex;justify-content:space-between;align-items:center">
                <div>
                    <div style="font-weight:700;font-size:0.85rem;color:#fffbe6">{p.get('title','')}</div>
                    <div style="font-size:0.72rem;color:#7a6030">{p.get('authors','')} · {p.get('year','')} · {p.get('venue','')}</div>
                </div>
                <div style="background:rgba(255,255,255,0.05);border:1px solid {color}33;border-radius:999px;padding:3px 12px;color:{color};font-size:0.75rem;font-weight:800;white-space:nowrap;margin-left:1rem">{pct}% similar</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("#### Overlapping Keywords")
        kw_html = " ".join([f'<span style="display:inline-block;padding:2px 10px;border-radius:999px;background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.2);color:#FFD700;font-size:0.72rem;font-weight:700;margin:2px">{k}</span>' for k in d.get("overlap_keywords", [])])
        st.markdown(kw_html, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.15);border-radius:12px;padding:1.2rem;margin-top:1rem">
            <div style="font-size:0.65rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#FFA500;margin-bottom:0.5rem">VERDICT</div>
            <div style="font-size:0.85rem;color:#fff8d6;line-height:1.7">{d.get('verdict','')}</div>
            <div style="margin-top:0.75rem;font-size:0.8rem;color:#7a6030">💡 {d.get('recommendation','')}</div>
        </div>""", unsafe_allow_html=True)

        save_result("scanner", topic, d, score)
        st.success("✓ Saved to tracker")
