from groq import Groq
import json
import streamlit as st

# Use a single consistent session state key everywhere
_KEY = "groq_api_key"

def get_client():
    key = st.session_state.get(_KEY, "").strip()
    if not key:
        st.error("⚠ Please enter your Groq API key in the sidebar (starts with gsk_...)")
        return None
    return Groq(api_key=key)

def call_claude(system_prompt, user_message, max_tokens=1500):
    client = get_client()
    if not client:
        return None
    try:
        msg = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message}
            ]
        )
        return msg.choices[0].message.content
    except Exception as e:
        st.error(f"Groq API error: {e}")
        return None

def parse_json(raw):
    try:
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception as e:
        st.error(f"JSON parse error: {e}\n\nRaw response:\n{raw[:400]}")
        return None
