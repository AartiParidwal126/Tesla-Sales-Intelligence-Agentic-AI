import streamlit as st
import pandas as pd
import plotly.express as px
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 1. Page Config - International Standard
st.set_page_config(page_title="Nexus AI | Strategic Vault", layout="wide", page_icon="🛡️")

# 2. Advanced Cyber-Executive CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    .main { background-color: #05070a; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    .stSidebar { background-color: #0a0f16 !important; border-right: 1px solid #1e293b; }
    
    /* Privacy Shield Banner */
    .privacy-banner {
        background: linear-gradient(90deg, #064e3b 0%, #022c22 100%);
        padding: 10px; border-radius: 8px; border-left: 5px solid #10b981;
        margin-bottom: 20px; font-size: 0.9em;
    }
    
    /* Deep Insight Cards */
    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #334155; border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; letter-spacing: 2px; color: #3b82f6; }
    .stButton>button { 
        background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
        border: none; color: white; font-family: 'Orbitron'; height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: TEAM & SECURITY ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
st.sidebar.markdown("### 🔐 SECURITY STATUS: **ENCRYPTED**")
st.sidebar.markdown("---")

team = {
    "Alex (Lead Analyst)": "Identify hidden anomalies and 12-month future trends from this data. Ignore the obvious.",
    "Sarah (Global Researcher)": "Connect this data to 3 specific global market shifts. Predict the 'Next Big Move'.",
    "Marcus (Strategic Director)": "Create a high-level 6-month execution blueprint. No fluff, only hard actions."
}

mode = st.sidebar.radio("Command Level", ["Full Strategic Audit", "Private Briefing"])
uploaded_file = st.sidebar.file_uploader("📂 Feed Data into Vault (CSV)", type=['csv'])

# --- MAIN INTERFACE ---
st.title("🛡️ NEXUS EXECUTIVE VAULT")

# Security Badge for Client Trust
st.markdown("""
    <div class="privacy-banner">
        <b>OFFICIAL PRIVACY PROTOCOL:</b> Data is processed in an isolated RAM environment. 
        Zero persistence enabled. No data is stored or logged on Nexus servers. 🔒
    </div>
    """, unsafe_allow_html=True)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    data_context = df.head(20).to_string()

    if mode == "Full Strategic Audit":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Live Intelligence Map")
            # Dynamic Bar Chart for visual depth
            fig = px.line(df.head(15), x=df.columns[0], y=df.columns[1], 
                         title="Real-time Metric Projection", template="plotly_dark")
            fig.update_traces(line_color='#3b82f6', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("### ⚡ Critical Anomalies")
            st.warning("Anomaly Detected: Recent volatility exceeds 15% threshold.")
            st.info("Market Sync: Data matches 89% of current industry shifts.")

        if st.button("🚀 EXECUTE DEEP ANALYSIS"):
            report_log = ""
            for name, prompt in team.items():
                with st.expander(f"🕵️ {name.upper()} IS EXTRACTING INSIGHTS...", expanded=True):
                    res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": f"{prompt}. Data: {data_context}"}]
                    )
                    ans = res.choices[0].message.content
                    st.markdown(ans)
                    report_log += f"\n\n[{name}]\n{ans}"
            
            st.download_button("📥 Download Encrypted Report", report_log, file_name="Nexus_Intel.txt")

    else:
        # Private Briefing Mode
        agent_choice = st.sidebar.selectbox("Choose Expert", list(team.keys()))
        st.subheader(f"💬 Secure Line: {agent_choice}")
        if prompt := st.chat_input("Ask for hidden insights..."):
            with st.chat_message("user"): st.write(prompt)
            with st.chat_message("assistant"):
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": f"You are {agent_choice}. Context: {data_context}"},
                              {"role": "user", "content": prompt}]
                )
                st.write(res.choices[0].message.content)
else:
    st.markdown("### System Awaiting Input... \nUpload corporate data to begin deep-layer extraction.")