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
    .info-box {
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        font-size: 14px;
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
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a street-smart, Gen-Z dating coach based in Yangon, Myanmar. Speak in casual English, internet slang (rn, ngl, fr, sus, rizz), and Burmlish. Chill, helpful, never robotic."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=15)
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
    
    st.markdown("""
    <div class="info-box">
        <strong>📋 What to copy:</strong><br>
        • Instagram/Facebook bio text<br>
        • Recent post captions (last 6-12 months)<br>
        • Story highlights descriptions<br>
        • Any public "About" sections<br><br>
        <strong>⏰ For Timeline Analysis:</strong> Include dates or years when posts were made (e.g., "Jan 2023: Beach trip", "Dec 2023: New job!")
    </div>
    """, unsafe_allow_html=True)
    
    analysis_type = st.radio("Choose analysis type:", ["Quick Vibe Check", "Timeline Analysis (Year-by-Year)"])
    
    profile_info = st.text_area("Paste the profile text here", placeholder="Example:\nBio: Coffee addict ☕ | Travel 🌏\n\nJan 2022: Started gym\nJun 2022: Trip to Thailand\nDec 2022: New job at tech company\nMar 2023: Got a dog\nAug 2023: Breakup posts\nNov 2023: 'New beginnings' caption")
    
    if st.button("Analyze Profile"):
        if profile_info:
            with st.spinner("Scanning public data..."):
                if analysis_type == "Quick Vibe Check":
                    prompt = f"Analyze this public profile and give a casual vibe check. What are their interests? Any red flags? What icebreakers would work? Keep it Gen-Z/Burmlish style: {profile_info}"
                else:
                    prompt = f"Analyze this profile TIMELINE year-by-year. Show how their interests, lifestyle, and vibe evolved over time. Point out patterns, major life changes, and what this says about them. Format as a timeline with years. Keep it Gen-Z/Burmlish style: {profile_info}"
                
                result = get_ai_response(prompt)
                st.markdown(f'<div class="glass-panel">{result.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### Real-time Scam & Catfish Shield")
    scam_text = st.text_area("Paste a suspicious message you received", placeholder="e.g., Hey bro I need urgent help with crypto investment, click this link")
    if st.button("Analyze Risk"):
        if scam_text:
            with st.spinner("Running heuristic & AI scan..."):
                prompt = f"Analyze this message for romance scam, catfish, or phishing red flags. Be direct, warn the user if it's sus, and explain WHY. Keep it Gen-Z/Burmlish style: '{scam_text}'"
                result = get_ai_response(prompt)
                st.markdown(f'<div class="glass-panel alert">{result.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align: center; color: #64748b; font-size: 12px;'>Built with ✨ for ethical, privacy-first digital wingman duties.</p>", unsafe_allow_html=True)
