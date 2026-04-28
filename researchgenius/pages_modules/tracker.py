import streamlit as st
import json
from utils.db import get_all_results, update_status, delete_result

def render():
    st.markdown("""<div style="font-family:'Pinyon Script',cursive;font-size:2.5rem;color:#FFD700;margin-bottom:0.2rem">Research Tracker</div>
    <div style="font-size:0.8rem;color:#7a6030;margin-bottom:1.5rem">SQLite-backed session history · Keep or remove entries</div>""", unsafe_allow_html=True)

    rows = get_all_results()

    if not rows:
        st.markdown("""<div style="text-align:center;padding:3rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,215,0,0.1);border-radius:14px">
        <div style="font-family:'Pinyon Script',cursive;font-size:2rem;color:#7a6030">No sessions yet</div>
        <div style="font-size:0.8rem;color:#7a6030;margin-top:0.5rem">Run Topic Scanner, Gap Suggester, or any other feature to populate your tracker.</div>
        </div>""", unsafe_allow_html=True)
        return

    # Stats
    total = len(rows)
    active = sum(1 for r in rows if r["status"] == "active")
    avg_score = sum(r["score"] for r in rows) // max(total, 1)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sessions", total)
    c2.metric("Active", active)
    c3.metric("Avg Score", avg_score)

    st.markdown("<hr>", unsafe_allow_html=True)

    feature_icon = {"scanner":"🔍","gap_suggester":"💡","paper_draft":"📄","collision":"⚡","roadmap":"🗺"}

    for r in rows:
        ficon = feature_icon.get(r["feature"], "📊")
        status_color = "#6fcf8a" if r["status"] == "active" else "#e87868" if r["status"] == "archived" else "#7a6030"
        score_color = "#6fcf8a" if r["score"] >= 70 else "#FFD700" if r["score"] >= 40 else "#e87868"

        with st.expander(f"{ficon} {r['feature'].replace('_',' ').title()} · {r['topic'][:60]}... · {r['created_at'][:16]}"):
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                st.markdown(f'<div style="font-size:0.75rem;color:#7a6030">Feature: <strong style="color:#fffbe6">{r["feature"]}</strong> &nbsp;|&nbsp; Score: <strong style="color:{score_color}">{r["score"]}</strong> &nbsp;|&nbsp; Status: <strong style="color:{status_color}">{r["status"]}</strong></div>', unsafe_allow_html=True)
            with col2:
                new_status = "archived" if r["status"] == "active" else "active"
                btn_label = "📦 Archive" if r["status"] == "active" else "♻ Restore"
                if st.button(btn_label, key=f"upd_{r['id']}"):
                    update_status(r["id"], new_status)
                    st.rerun()
            with col3:
                if st.button("🗑 Delete", key=f"del_{r['id']}"):
                    delete_result(r["id"])
                    st.rerun()

            if r.get("result_json"):
                try:
                    data = json.loads(r["result_json"])
                    st.json(data)
                except:
                    st.text(r["result_json"][:500])
