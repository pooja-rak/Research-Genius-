import streamlit as st

def render():
    st.markdown("""
    <div style="text-align:center;padding:2rem 0 1rem">
        <div style="font-family:'Pinyon Script',cursive;font-size:5rem;background:linear-gradient(135deg,#FFD700,#FFA500,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1">ResearchGenius AI</div>
        <div style="font-size:0.75rem;font-weight:700;letter-spacing:3px;color:#7a6030;text-transform:uppercase;margin-top:0.5rem">Your Intelligent Research Companion</div>
        <div style="margin-top:1rem"><span style="display:inline-block;background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.3);color:#FFD700;font-size:0.65rem;font-weight:700;letter-spacing:2px;padding:5px 16px;border-radius:999px;text-transform:uppercase">✦ Phase 2 MVP · 5 ML Features </span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    cols = st.columns(3)
    features = [
        ("🔍","Topic Scanner","Semantic similarity check against published literature using BERT-style embeddings. Get an originality score, risk level, and similar paper detection."),
        ("💡","Gap Suggester","TF-IDF + semantic clustering finds 3–5 underexplored research directions you can pivot into with novelty scores and keyword mapping."),
        ("📄","Paper Draft","RAG-powered generator creates structured academic drafts — abstract, introduction, methodology, related work — ready to refine."),
        ("⚡","Collision Alerts","Bi-directional conflict detection across the literature. Severity-ranked alerts with pivot suggestions to differentiate your work."),
        ("🗺","Research Roadmap","Force-directed knowledge graph mapping your topic to related subfields, bridging concepts, gaps, and methods. Fully interactive."),
        ("📊","Tracker","SQLite-backed session history. Keep or update every scan, gap analysis, and draft you run."),
    ]
    for i, (icon, title, desc) in enumerate(features):
        col = cols[i % 3]
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,215,0,0.15);border-radius:14px;padding:1.2rem;margin-bottom:1rem;height:180px">
                <div style="font-size:1.8rem;margin-bottom:0.5rem">{icon}</div>
                <div style="font-family:'Pinyon Script',cursive;font-size:1.4rem;color:#FFD700;margin-bottom:0.4rem">{title}</div>
                <div style="font-size:0.75rem;color:#7a6030;line-height:1.5">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.2);border-radius:14px;padding:1.5rem;text-align:center">
        <div style="font-size:0.8rem;color:#7a6030;line-height:1.8">
        <strong style="color:#FFD700">Getting started:</strong> Enter your Anthropic API key in the sidebar → Pick a feature → Start researching<br>
        <span style="font-size:0.7rem">Stack: Streamlit · Claude Sonnet · SentenceTransformers · SQLite · Pyvis · ReportLab</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
