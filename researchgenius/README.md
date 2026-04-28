# ResearchGenius AI

**5-feature ML research assistant powered by Claude Sonnet + Streamlit**

## Features
| Feature | What it does |
|---|---|
| 🔍 Topic Scanner | BERT-style originality scoring vs published literature |
| 💡 Gap Suggester | TF-IDF + semantic clustering → underexplored directions |
| 📄 Paper Draft | RAG-powered structured academic draft generator |
| ⚡ Collision Alerts | Bi-directional conflict detection with severity ranking |
| 🗺 Research Roadmap | Interactive D3 force-directed knowledge graph |
| 📊 Tracker | SQLite session history with Keep/Archive/Delete |

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

### 3. Open in browser
```
http://localhost:8501
```

### 4. Enter your API key
Paste your Anthropic API key in the sidebar → Start researching!

## Get an API key
Sign up at https://console.anthropic.com → Create API key

## Tech Stack
- **Frontend**: Streamlit 1.38+ with custom CSS (Yellow #FFD700 theme, Pinyon Script + Nunito fonts)
- **AI Engine**: Claude Sonnet via Anthropic Python SDK
- **Graph**: D3.js v7 force-directed layout (embedded via Streamlit HTML component)
- **Database**: SQLite (auto-created at data/research.db)
- **ML tools**: scikit-learn (TF-IDF), sentence-transformers (similarity)
- **PDF**: ReportLab

## Deploy to Streamlit Cloud (Free)
1. Push to GitHub
2. Go to share.streamlit.io → New app → Select your repo → app.py
3. Add `ANTHROPIC_API_KEY` in Secrets settings

## Deploy to Render.com
1. Connect GitHub repo
2. Build command: `pip install -r requirements.txt`
3. Start command: `streamlit run app.py --server.port $PORT --server.headless true`
4. Add `ANTHROPIC_API_KEY` environment variable
