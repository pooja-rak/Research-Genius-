import streamlit as st

def inject_styles():
    st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Pinyon+Script&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
/* ── Base ── */
[data-testid="stAppViewContainer"] {
    background: #1a1208 !important;
}
[data-testid="stSidebar"] {
    background: #120d05 !important;
    border-right: 1px solid rgba(255,215,0,0.12) !important;
}
[data-testid="stSidebar"] * { color: #fffbe6 !important; }
body, .stMarkdown, p, label, .stTextInput, .stSelectbox, .stTextArea {
    font-family: 'Nunito', sans-serif !important;
    color: #fffbe6 !important;
}
/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,215,0,0.2) !important;
    border-radius: 10px !important;
    color: #fffbe6 !important;
    font-family: 'Nunito', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #FFA500 !important;
    box-shadow: 0 0 0 3px rgba(255,165,0,0.1) !important;
}
/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #FFD700, #FFA500) !important;
    color: #1a1208 !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-size: 14px !important;
    transition: all 0.2s !important;
    box-shadow: 0 3px 18px rgba(255,165,0,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 24px rgba(255,165,0,0.45) !important;
}
/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,215,0,0.2) !important;
    border-radius: 10px !important;
    color: #fffbe6 !important;
}
/* Sidebar radio */
[data-testid="stSidebarNav"] { display: none; }
.stRadio > label { color: #fffbe6 !important; font-family: 'Nunito', sans-serif !important; }
.stRadio [data-testid="stMarkdownContainer"] { color: #fffbe6 !important; }
/* Cards */
.rg-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,215,0,0.14);
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 16px;
}
.rg-card-title {
    font-family: 'Pinyon Script', cursive;
    font-size: 30px;
    color: #FFD700;
    margin-bottom: 6px;
    line-height: 1.2;
}
.rg-card-desc {
    font-size: 13px;
    color: #7a6030;
    margin-bottom: 18px;
    line-height: 1.6;
}
/* Header */
.rg-header {
    text-align: center;
    padding: 20px 0 10px;
}
.rg-script {
    font-family: 'Pinyon Script', cursive;
    font-size: 64px;
    background: linear-gradient(135deg, #FFD700, #FFA500, #FF8C00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    filter: drop-shadow(0 2px 8px rgba(255,165,0,0.25));
}
.rg-sub {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #7a6030;
    margin-top: 4px;
}
.rg-badge {
    display: inline-block;
    margin-top: 12px;
    background: rgba(255,215,0,0.1);
    border: 1px solid rgba(255,215,0,0.25);
    color: #FFD700;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 5px 14px;
    border-radius: 999px;
}
/* Sidebar logo */
.sidebar-logo { text-align: center; padding: 16px 0 20px; }
.sb-script {
    font-family: 'Pinyon Script', cursive;
    font-size: 44px;
    color: #FFD700;
    line-height: 1;
}
.sb-title { font-size: 13px; font-weight: 800; color: #fffbe6; margin: 4px 0 2px; }
.sb-version { font-size: 10px; color: #7a6030; letter-spacing: 1px; }
/* Result boxes */
.rg-result {
    background: rgba(255,215,0,0.04);
    border: 1px solid rgba(255,215,0,0.16);
    border-radius: 12px;
    padding: 18px;
    margin-top: 16px;
}
.rg-result-label {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FFA500;
    margin-bottom: 10px;
    border-bottom: 1px solid rgba(255,215,0,0.12);
    padding-bottom: 8px;
}
/* Badges */
.badge-high { background:rgba(192,57,43,0.2);border:1px solid rgba(192,57,43,0.4);color:#e87868;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:800; }
.badge-med  { background:rgba(255,165,0,0.15);border:1px solid rgba(255,165,0,0.35);color:#FFD700;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:800; }
.badge-low  { background:rgba(45,122,58,0.15);border:1px solid rgba(45,122,58,0.35);color:#6fcf8a;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:800; }
.chip {
    display:inline-block;padding:2px 9px;border-radius:999px;
    font-size:10px;font-weight:700;background:rgba(255,215,0,0.1);
    border:1px solid rgba(255,215,0,0.2);color:#FFD700;margin:2px;
}
/* Divider */
hr { border-color: rgba(255,215,0,0.1) !important; }
/* Metric */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,215,0,0.12) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
}
[data-testid="stMetricLabel"] { color: #7a6030 !important; font-family: 'Nunito', sans-serif !important; }
[data-testid="stMetricValue"] { color: #FFD700 !important; font-family: 'Pinyon Script', cursive !important; font-size: 36px !important; }
/* Expander */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,215,0,0.12) !important;
    border-radius: 10px !important;
}
/* Success / warning boxes */
.stSuccess { background: rgba(45,122,58,0.15) !important; border: 1px solid rgba(45,122,58,0.3) !important; }
.stWarning { background: rgba(255,165,0,0.1) !important; border: 1px solid rgba(255,165,0,0.3) !important; }
.stError   { background: rgba(192,57,43,0.1) !important; border: 1px solid rgba(192,57,43,0.3) !important; }
/* Spinner */
[data-testid="stSpinner"] > div { border-top-color: #FFD700 !important; }
/* DataFrame */
[data-testid="stDataFrame"] { border: 1px solid rgba(255,215,0,0.12) !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)
