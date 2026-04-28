import anthropic
import json
import streamlit as st

def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "") or \
              __import__("os").environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("⚠ ANTHROPIC_API_KEY not found. Add it to .streamlit/secrets.toml")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)

def call_claude(system_prompt: str, user_message: str, max_tokens: int = 1500) -> str:
    client = get_client()
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return "".join(b.text for b in msg.content if hasattr(b, "text"))

def call_claude_json(system_prompt: str, user_message: str, max_tokens: int = 1500) -> dict:
    raw = call_claude(system_prompt, user_message, max_tokens)
    clean = raw.strip()
    if clean.startswith("```"):
        clean = "\n".join(clean.split("\n")[1:])
    if clean.endswith("```"):
        clean = clean[:-3]
    return json.loads(clean.strip())
