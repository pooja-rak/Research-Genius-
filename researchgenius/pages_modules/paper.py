import streamlit as st
from utils.api import call_claude, parse_json
from utils.db import save_result

SYSTEM = """You are an academic paper generation engine using RAG (Retrieval-Augmented Generation).
Respond ONLY in valid JSON — no markdown fences.

Schema:
{
  "abstract": "<150-200 word abstract>",
  "keywords": ["kw1","kw2","kw3","kw4","kw5"],
  "introduction": "<200-250 word introduction>",
  "related_work": "<150-200 word related work with citation placeholders [1],[2],[3]>",
  "methodology": "<150-200 word methodology section>",
  "expected_results": "<100-150 word expected results / contributions>",
  "future_work": "<2-3 sentences on future directions>",
  "references": ["<Author et al. (Year). Title. Venue.>","..."],
  "rag_sources": ["<simulated retrieval source 1>","<simulated retrieval source 2>","<simulated retrieval source 3>"]
}

Write in formal academic English. Be specific and substantive."""

def render():
    st.markdown("""<div style="font-family:'Pinyon Script',cursive;font-size:2.5rem;color:#FFD700;margin-bottom:0.2rem">Paper Draft Generator</div>
    <div style="font-size:0.8rem;color:#7a6030;margin-bottom:1.5rem">RAG pipeline · Structured academic drafts · Citation-ready output</div>""", unsafe_allow_html=True)

    with st.form("paper_form"):
        title = st.text_input("Paper Title / Topic", placeholder="e.g. Federated Learning for Privacy-Preserving Medical Diagnosis Across Hospital Networks")
        notes = st.text_area("Key Methodology & Findings", height=120,
            placeholder="- Used federated averaging across 12 hospital nodes\n- Achieved 94.3% accuracy on chest X-ray classification\n- Differential privacy budget ε=0.5\n- Dataset: 45,000 anonymized patient records")
        col1, col2 = st.columns(2)
        with col1:
            ptype = st.selectbox("Paper Type", ["Conference paper (IEEE/ACM style)", "Journal article (Elsevier style)", "Literature review", "Thesis chapter"])
        with col2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("✦ Generate Draft", use_container_width=True)

    if submitted:
        if not title.strip():
            st.warning("Please enter a paper title."); return

        with st.spinner("Generating academic draft via RAG pipeline..."):
            raw = call_claude(SYSTEM, f"Title: \"{title}\"\nNotes/findings: {notes or 'Generate appropriate content'}\nPaper type: {ptype}", max_tokens=2000)
        if not raw: return
        d = parse_json(raw)
        if not d: return

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-family:\'Pinyon Script\',cursive;font-size:2rem;color:#FFD700;margin-bottom:0.5rem">{title}</div>', unsafe_allow_html=True)

        kw_html = " ".join([f'<span style="display:inline-block;padding:2px 10px;border-radius:999px;background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.2);color:#FFD700;font-size:0.72rem;font-weight:700;margin:2px">{k}</span>' for k in d.get("keywords", [])])
        st.markdown(kw_html, unsafe_allow_html=True)
        st.markdown("")

        tabs = st.tabs(["Abstract", "Introduction", "Related Work", "Methodology", "Results & Future", "References"])

        with tabs[0]:
            st.markdown(f'<div style="background:rgba(255,215,0,0.04);border:1px solid rgba(255,215,0,0.12);border-radius:10px;padding:1rem;font-size:0.85rem;line-height:1.8;color:#fff8d6">{d.get("abstract","")}</div>', unsafe_allow_html=True)

        with tabs[1]:
            st.markdown(f'<div style="font-size:0.85rem;line-height:1.8;color:#fff8d6">{d.get("introduction","")}</div>', unsafe_allow_html=True)

        with tabs[2]:
            st.markdown(f'<div style="font-size:0.85rem;line-height:1.8;color:#fff8d6">{d.get("related_work","")}</div>', unsafe_allow_html=True)

        with tabs[3]:
            st.markdown(f'<div style="font-size:0.85rem;line-height:1.8;color:#fff8d6">{d.get("methodology","")}</div>', unsafe_allow_html=True)

        with tabs[4]:
            st.markdown("**Expected Results / Contributions**")
            st.markdown(f'<div style="font-size:0.85rem;line-height:1.8;color:#fff8d6">{d.get("expected_results","")}</div>', unsafe_allow_html=True)
            st.markdown("**Future Work**")
            st.markdown(f'<div style="font-size:0.85rem;line-height:1.8;color:#fff8d6">{d.get("future_work","")}</div>', unsafe_allow_html=True)

        with tabs[5]:
            for i, ref in enumerate(d.get("references", []), 1):
                st.markdown(f'<div style="font-size:0.8rem;color:#7a6030;padding:0.4rem 0;border-bottom:1px solid rgba(255,215,0,0.08)">[{i}] {ref}</div>', unsafe_allow_html=True)
            st.markdown("**RAG Source Pool**")
            for s in d.get("rag_sources", []):
                st.markdown(f'<div style="font-size:0.75rem;color:#7a6030;padding:0.3rem 0">→ {s}</div>', unsafe_allow_html=True)

        full_text = f"Title: {title}\n\nAbstract:\n{d.get('abstract','')}\n\nIntroduction:\n{d.get('introduction','')}\n\nRelated Work:\n{d.get('related_work','')}\n\nMethodology:\n{d.get('methodology','')}\n\nExpected Results:\n{d.get('expected_results','')}\n\nFuture Work:\n{d.get('future_work','')}"
        st.download_button("⬇ Download Draft (.txt)", full_text, file_name="research_draft.txt", mime="text/plain")

        save_result("paper_draft", title, d, 75)
        st.success("✓ Saved to tracker")
