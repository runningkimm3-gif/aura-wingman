import streamlit as st
import requests

st.set_page_config(page_title="Aura Wingman", page_icon="✨", layout="centered")

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f8fafc;
    }
    .glass-panel {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        padding: 24px;
        margin-top: 16px;
        color: #e2e8f0;
        line-height: 1.6;
    }
    .glass-panel.alert {
        border: 1px solid rgba(239, 68, 68, 0.5);
        box-shadow: 0 20px 50px rgba(239, 68, 68, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 12px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px 12px 0 0;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(56, 189, 248, 0.15) !important;
        color: #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("✨ Aura: Privacy-First Wingman")
st.markdown("Your Gen-Z / Burmlish chat coach, OSINT detective, and scam shield.")

def get_ai_response(prompt):
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key or api_key == "your_groq_api_key_here":
        return "⚠️ API Key missing. Please add your Groq API key in .streamlit/secrets.toml"
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a street-smart, Gen-Z dating coach based in Yangon, Myanmar. Speak in casual English, internet slang (rn, ngl, fr, sus, rizz), and Burmlish. Chill, helpful, never robotic."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"⚠️ AI Error: {response.status_code}"
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

tab1, tab2, tab3 = st.tabs(["💘 CUPID", "🔍 DETECTIVE", "🛡️ PROTECTIVE"])

with tab1:
    st.markdown("### Get the perfect reply")
    user_text = st.text_input("What do you want to say?", placeholder="e.g., hey what are you doing rn")
    if st.button("Generate Rizz Suggestions"):
        if user_text:
            with st.spinner("Analyzing vibes..."):
                prompt = f"User wants to say: '{user_text}'. Give 3 better, flirtier ways using Gen-Z/Burmlish slang. Use push-pull dynamics. Format as bullet points."
                result = get_ai_response(prompt)
                st.markdown(f'<div class="glass-panel">{result.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### Consent-based Profile Vibe Check")
    profile_info = st.text_area("Paste public bio text", placeholder="e.g., 'Coffee addict ☕ | Travel 🌏'")
    if st.button("Scan Footprint"):
        if profile_info:
            with st.spinner("Scanning..."):
                prompt = f"Analyze this public profile and give a casual vibe check. Interests? Red flags? Gen-Z/Burmlish style: {profile_info}"
                result = get_ai_response(prompt)
                st.markdown(f'<div class="glass-panel">{result.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### Scam & Catfish Shield")
    scam_text = st.text_area("Paste suspicious message", placeholder="e.g., Hey bro I need urgent help with crypto")
    if st.button("Analyze Risk"):
        if scam_text:
            with st.spinner("Running scan..."):
                prompt = f"Analyze for romance scam, catfish, or phishing red flags. Be direct, warn if sus, explain WHY. Gen-Z/Burmlish style: '{scam_text}'"
                result = get_ai_response(prompt)
                st.markdown(f'<div class="glass-panel alert">{result.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align: center; color: #64748b; font-size: 12px;'>Built with ✨ for ethical digital wingman duties.</p>", unsafe_allow_html=True)
