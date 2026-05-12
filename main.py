import streamlit as st
from dotenv import load_dotenv
import time

load_dotenv()

from agent import summarize_topic, ask_memory, memory

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Marwan Hot Assistant (1)",
    page_icon="🧠",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d0d0d;
    color: #e8e8e8;
}

h1, h2, h3 { font-family: 'Space Mono', monospace; }

.stButton > button {
    background: #1a1a2e;
    color: #00ff88;
    border: 1px solid #00ff88;
    border-radius: 4px;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    padding: 10px 24px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #00ff88;
    color: #0d0d0d;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #1a1a1a;
    border: 1px solid #333;
    color: #e8e8e8;
    border-radius: 4px;
    font-family: 'Inter', sans-serif;
}

.step-box {
    background: #111;
    border-left: 3px solid #00ff88;
    padding: 10px 14px;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
}

.summary-box {
    background: #111;
    border: 1px solid #222;
    border-radius: 8px;
    padding: 20px;
    margin-top: 16px;
    line-height: 1.7;
}

.memory-pill {
    display: inline-block;
    background: #1a2e1a;
    color: #00ff88;
    border: 1px solid #00ff8855;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    margin: 3px;
    font-family: 'Space Mono', monospace;
}

.stat-card {
    background: #111;
    border: 1px solid #222;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}

.stat-number {
    font-family: 'Space Mono', monospace;
    font-size: 32px;
    color: #00ff88;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🧠 Marwan's Assistant")
st.markdown("*Multi-agent · RAG · ChromaDB · Gemini · LangChain And Much More*")
st.divider()

# ── Layout ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1.2, 1], gap="large")

# ── Left: Research ────────────────────────────────────────────────────────────
with col1:
    st.markdown("### 🔍 Research a Topic")
    topic = st.text_input("Topic", placeholder="e.g. Quantum computing, LangGraph, RAG systems...")

    if st.button("▶ Research", use_container_width=True):
        if not topic.strip():
            st.warning("Enter a topic first.")
        else:
            with st.spinner("Agent is working..."):
                try:
                    summary, steps = summarize_topic(topic)

                    st.markdown("**Agent Steps:**")
                    for step in steps:
                        st.markdown(
                            f'<div class="step-box"><b>{step["action"]}</b><br>{step["input"]}</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown("**Summary:**")
                    st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
                    st.success(f"✅ Saved to memory! ({memory.count()} total entries)")

                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("Make sure your GOOGLE_API_KEY is set in the .env file")

# ── Right: Chat with Memory ───────────────────────────────────────────────────
with col2:
    st.markdown("### 💬 Ask Your Research")

    # Memory stats
    count = memory.count()
    st.markdown(f'<div class="stat-card"><div class="stat-number">{count}</div><div>items in memory</div></div>', unsafe_allow_html=True)
    st.markdown("")

    if count == 0:
        st.info("Research a topic first — then ask questions about it here.")
    else:
        question = st.text_area("Ask anything about your researched topics", height=100,
                                 placeholder="What did I learn about X?\nHow does Y work?\nCompare X and Y...")

        if st.button("💡 Ask", use_container_width=True):
            if question.strip():
                with st.spinner("Searching memory..."):
                    answer = ask_memory(question)
                    st.markdown("**Answer:**")
                    st.markdown(f'<div class="summary-box">{answer}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<center style='color:#555; font-family: Space Mono, monospace; font-size:11px'>
LangChain · LangGraph · ChromaDB · Gemini 1.5 Flash · DuckDuckGo Search · Streamlit
</center>
""", unsafe_allow_html=True)
