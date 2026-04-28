import streamlit as st

st.set_page_config(
    page_title="ResearchGenius AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Pinyon+Script&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a1208 0%, #2a1e0a 50%, #1a1208 100%) !important;
    color: #fffbe6 !important;
    font-family: 'Nunito', sans-serif !important;
}
[data-testid="stSidebar"] { background: rgba(42,30,10,0.97) !important; border-right: 1px solid rgba(255,215,0,0.15) !important; }
[data-testid="stSidebar"] * { color: #fffbe6 !important; }
.rg-script { font-family: 'Pinyon Script', cursive !important; font-size: 4rem; background: linear-gradient(135deg, #FFD700, #FFA500, #FF8C00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1.1; text-align:center; }
.rg-sub { font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; color: #7a6030; text-transform: uppercase; text-align:center; }
.rg-badge { display: inline-block; background: rgba(255,215,0,0.1); border: 1px solid rgba(255,215,0,0.3); color: #FFD700; font-size: 0.65rem; font-weight: 700; letter-spacing: 2px; padding: 4px 14px; border-radius: 999px; text-transform: uppercase; }
.rg-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,215,0,0.15); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; }
.rg-card-title { font-family: 'Pinyon Script', cursive !important; font-size: 1.8rem; color: #FFD700; margin-bottom: 0.4rem; }
.rg-result { background: rgba(255,215,0,0.05); border: 1px solid rgba(255,215,0,0.2); border-radius: 12px; padding: 1.2rem; margin-top: 1rem; font-size: 0.85rem; line-height: 1.75; color: #fff8d6; }
.rg-label { font-size: 0.65rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; color: #FFA500; margin-bottom: 0.5rem; }
.alert-high { background: rgba(192,57,43,0.1); border: 1px solid rgba(192,57,43,0.35); border-radius: 11px; padding: 1rem; margin-bottom: 0.75rem; }
.alert-med  { background: rgba(255,165,0,0.07); border: 1px solid rgba(255,165,0,0.28); border-radius: 11px; padding: 1rem; margin-bottom: 0.75rem; }
.alert-low  { background: rgba(45,122,58,0.08); border: 1px solid rgba(45,122,58,0.3); border-radius: 11px; padding: 1rem; margin-bottom: 0.75rem; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,215,0,0.2) !important; border-radius: 10px !important; color: #fffbe6 !important; }
.stSelectbox > div > div { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,215,0,0.2) !important; border-radius: 10px !important; color: #fffbe6 !important; }
.stButton > button { background: linear-gradient(135deg, #FFD700, #FFA500) !important; color: #1a1208 !important; font-weight: 800 !important; border: none !important; border-radius: 10px !important; box-shadow: 0 3px 18px rgba(255,165,0,0.35) !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, #FFD700, #FFA500) !important; }
div[data-testid="metric-container"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,215,0,0.15) !important; border-radius: 10px !important; padding: 1rem !important; }
div[data-testid="metric-container"] label { color: #7a6030 !important; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 2rem !important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,215,0,0.12) !important; border-radius: 12px !important; padding: 4px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #7a6030 !important; font-weight: 700 !important; border-radius: 9px !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg,#FFD700,#FFA500) !important; color: #1a1208 !important; }
hr { border-color: rgba(255,215,0,0.15) !important; }
.stMarkdown p { color: #fffbe6 !important; }
</style>
""", unsafe_allow_html=True)

# ── Initialise session state key ONCE at the top ──────────────────────────
if "groq_api_key" not in st.session_state:
    st.session_state["groq_api_key"] = ""

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem">
        <div style="font-family:'Pinyon Script',cursive;font-size:2.2rem;background:linear-gradient(135deg,#FFD700,#FFA500);-webkit-background-clip:text;-webkit-text-fill-color:transparent">ResearchGenius</div>
        <div style="font-size:0.6rem;letter-spacing:2px;color:#7a6030;text-transform:uppercase">AI Research Assistant</div>
    </div><hr>
    """, unsafe_allow_html=True)

    page = st.radio("Navigate", [
        "🏠 Home", "🔍 Topic Scanner", "💡 Gap Suggester",
        "📄 Paper Draft", "⚡ Collision Alerts", "🗺 Research Roadmap", "📊 Tracker"
    ], label_visibility="collapsed")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Key input — bound directly to session state via key= parameter
    st.text_input(
        "🔑 Groq API Key (free)",
        type="password",
        placeholder="gsk_...",
        key="groq_api_key",          # ← binds directly to st.session_state["groq_api_key"]
        help="Get your free key at console.groq.com — no credit card needed"
    )

    # Live status indicator
    if st.session_state["groq_api_key"].strip():
        st.success("✓ API key saved — ready!")
    else:
        st.warning("Paste your gsk_... key above")
        st.markdown("""<div style="font-size:0.7rem;color:#7a6030;line-height:1.6;margin-top:0.3rem">
        Get a free key at<br>
        <strong style="color:#FFD700">console.groq.com</strong><br>
        → Sign up → API Keys → Create
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="font-size:0.65rem;color:#7a6030;text-align:center;margin-top:1rem;line-height:1.6">
    ResearchGenius AI · Phase 2 MVP<br>Powered by Groq + Llama 3.3 70B</div>""", unsafe_allow_html=True)

# ── Page routing ───────────────────────────────────────────────────────────
if page == "🏠 Home":
    from pages_modules import home; home.render()
elif page == "🔍 Topic Scanner":
    from pages_modules import scanner; scanner.render()
elif page == "💡 Gap Suggester":
    from pages_modules import gap; gap.render()
elif page == "📄 Paper Draft":
    from pages_modules import paper; paper.render()
elif page == "⚡ Collision Alerts":
    from pages_modules import collision; collision.render()
elif page == "🗺 Research Roadmap":
    from pages_modules import roadmap; roadmap.render()
elif page == "📊 Tracker":
    from pages_modules import tracker; tracker.render()
