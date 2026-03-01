import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import json
import time
import random

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GraphLens",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0f1a;
    color: #e8eaf6;
}
.stApp { background-color: #0d0f1a; }

/* ── Hide default streamlit elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; }

/* ── Logo / Title ── */
.logo-text {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f97316, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}
.logo-sub {
    font-size: 0.75rem;
    color: #6b7280;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: -4px;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid #1e2030;
}

/* ── Chat messages ── */
.chat-user {
    background: #1e2030;
    border-left: 3px solid #f97316;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin: 8px 0;
    font-size: 0.9rem;
}
.chat-assistant {
    background: #131525;
    border-left: 3px solid #6366f1;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin: 8px 0;
    font-size: 0.9rem;
    line-height: 1.6;
}
.chat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 6px;
}
.chat-label-user  { color: #f97316; }
.chat-label-bot   { color: #6366f1; }

/* ── Citation pills ── */
.citation-pill {
    display: inline-block;
    background: #1e2030;
    border: 1px solid #6366f1;
    color: #a5b4fc;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    padding: 2px 8px;
    border-radius: 20px;
    margin: 2px;
    cursor: pointer;
}
.citation-pill:hover { background: #6366f1; color: white; }

/* ── Timestamp badge ── */
.timestamp-badge {
    background: #f97316;
    color: white;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 3px 8px;
    border-radius: 4px;
    margin-right: 6px;
}

/* ── Confidence bar ── */
.confidence-wrap {
    background: #1e2030;
    border-radius: 20px;
    height: 6px;
    margin-top: 8px;
    overflow: hidden;
}
.confidence-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, #6366f1, #f97316);
    transition: width 0.8s ease;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0a0c17 !important;
    border-right: 1px solid #1e2030;
}

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: #1e2030 !important;
    border: 1px solid #2d3148 !important;
    color: #e8eaf6 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
}

/* ── Metrics ── */
.metric-box {
    background: #131525;
    border: 1px solid #1e2030;
    border-radius: 10px;
    padding: 12px 16px;
    text-align: center;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.4rem;
    color: #f97316;
    font-weight: 700;
}
.metric-label {
    font-size: 0.7rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Status dot ── */
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Divider ── */
.custom-divider {
    border: none;
    border-top: 1px solid #1e2030;
    margin: 12px 0;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_timestamp" not in st.session_state:
    st.session_state.current_timestamp = None
if "highlighted_nodes" not in st.session_state:
    st.session_state.highlighted_nodes = []
if "graph_data" not in st.session_state:
    # ── Mock knowledge graph data (replace with Neo4j query) ──
    st.session_state.graph_data = {
        "nodes": [
            {"id": "Gradient Descent",  "group": "core"},
            {"id": "Loss Function",     "group": "core"},
            {"id": "Neural Network",    "group": "core"},
            {"id": "Backpropagation",   "group": "core"},
            {"id": "Learning Rate",     "group": "param"},
            {"id": "Chain Rule",        "group": "math"},
            {"id": "Calculus",          "group": "math"},
            {"id": "Weights",           "group": "param"},
            {"id": "Overfitting",       "group": "issue"},
            {"id": "Regularization",    "group": "solution"},
            {"id": "SGD",               "group": "variant"},
            {"id": "Adam Optimizer",    "group": "variant"},
        ],
        "edges": [
            ("Gradient Descent", "Loss Function",   "minimizes"),
            ("Gradient Descent", "Learning Rate",   "uses"),
            ("Gradient Descent", "SGD",             "variant_of"),
            ("Gradient Descent", "Adam Optimizer",  "variant_of"),
            ("Loss Function",    "Neural Network",  "evaluates"),
            ("Backpropagation",  "Chain Rule",      "uses"),
            ("Backpropagation",  "Weights",         "updates"),
            ("Chain Rule",       "Calculus",        "derived_from"),
            ("Neural Network",   "Weights",         "contains"),
            ("Neural Network",   "Overfitting",     "suffers_from"),
            ("Overfitting",      "Regularization",  "solved_by"),
        ]
    }


# ─────────────────────────────────────────────
#  MOCK BACKEND FUNCTIONS
#  → Replace these with your real pipeline calls
# ─────────────────────────────────────────────
def mock_query_graphlens(question: str) -> dict:
    """
    REPLACE THIS with your actual GraphRAG pipeline call.
    Should call: chunker → ANN retrieval → reranker → graph → LLM
    """
    time.sleep(1.2)  # Simulate processing

    responses = {
        "default": {
            "answer": f"Based on the retrieved lecture segments, **{question.split()[0] if question else 'this concept'}** is explained in detail across multiple sections of the course. The knowledge graph reveals strong connections to related concepts that provide deeper context.",
            "citations": [
                {"timestamp": "14:32", "text": "The professor introduces the core concept with a formal definition..."},
                {"timestamp": "22:18", "text": "A worked example demonstrates the practical application..."},
                {"timestamp": "38:45", "text": "The relationship to adjacent concepts is explicitly drawn..."},
            ],
            "highlighted_nodes": random.sample(
                [n["id"] for n in st.session_state.graph_data["nodes"]], 3
            ),
            "confidence": round(random.uniform(0.72, 0.96), 2),
            "chunks_retrieved": random.randint(4, 8),
            "graph_nodes_used": random.randint(2, 5),
        }
    }
    return responses["default"]


def build_knowledge_graph(highlighted: list) -> str:
    """Builds pyvis graph HTML with highlighted nodes."""
    net = Network(height="380px", width="100%", bgcolor="#0d0f1a", font_color="#e8eaf6")
    net.barnes_hut(gravity=-3000, spring_length=120)

    color_map = {
        "core":     "#6366f1",
        "param":    "#f97316",
        "math":     "#22c55e",
        "issue":    "#ef4444",
        "solution": "#3b82f6",
        "variant":  "#a855f7",
    }

    for node in st.session_state.graph_data["nodes"]:
        is_highlighted = node["id"] in highlighted
        color = "#f97316" if is_highlighted else color_map.get(node["group"], "#6366f1")
        size  = 28 if is_highlighted else 18
        border = "#ffffff" if is_highlighted else color

        net.add_node(
            node["id"],
            label=node["id"],
            color={"background": color, "border": border},
            size=size,
            font={"size": 11, "color": "#e8eaf6"},
            borderWidth=2 if is_highlighted else 1,
        )

    for src, dst, label in st.session_state.graph_data["edges"]:
        net.add_edge(src, dst, label=label,
                     color="#2d3148", font={"size": 8, "color": "#6b7280"})

    net.set_options("""
    {
      "interaction": { "hover": true, "navigationButtons": false },
      "physics": { "stabilization": { "iterations": 100 } }
    }
    """)
    return net.generate_html()


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-text">🔭 GraphLens</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-sub">Hybrid GraphRAG System</div>', unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Status
    st.markdown('<div class="section-header">System Status</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="status-dot"></span><span style="font-size:0.75rem;color:#22c55e">Neo4j Live</span>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span class="status-dot"></span><span style="font-size:0.75rem;color:#22c55e">FAISS Ready</span>', unsafe_allow_html=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Config
    st.markdown('<div class="section-header">Retrieval Config</div>', unsafe_allow_html=True)
    top_k = st.slider("Top-K Chunks", 3, 15, 5,
                      help="Number of chunks retrieved by ANN search")
    hop_depth = st.radio("Graph Hop Depth", ["1-hop", "2-hop"],
                         help="1-hop is recommended to avoid noise")
    reranking = st.toggle("Neural Reranking", value=True,
                          help="Cross-encoder reranking of retrieved chunks")
    reliability_score = st.toggle("Reliability Score", value=True,
                                  help="Show confidence score per response")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Video selector
    st.markdown('<div class="section-header">Lecture Source</div>', unsafe_allow_html=True)
    lecture = st.selectbox("Select Lecture", [
        "Lecture 3 — Neural Networks",
        "Lecture 5 — Optimization",
        "Lecture 7 — Backpropagation",
        "Lecture 9 — Regularization",
    ])

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Stats
    st.markdown('<div class="section-header">Index Stats</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="metric-box"><div class="metric-value">1,842</div><div class="metric-label">Chunks</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-box"><div class="metric-value">348</div><div class="metric-label">Nodes</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.highlighted_nodes = []
        st.rerun()


# ─────────────────────────────────────────────
#  MAIN LAYOUT  (3 columns)
# ─────────────────────────────────────────────
col_chat, col_graph = st.columns([1.1, 0.9], gap="medium")


# ══════════════════════════════════════════════
#  LEFT — CHAT PANEL
# ══════════════════════════════════════════════
with col_chat:
    st.markdown('<div class="section-header">💬 Conversational Q&A</div>', unsafe_allow_html=True)

    # Chat history container
    chat_container = st.container(height=460, border=False)
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align:center; padding: 60px 20px; color: #374151;">
                <div style="font-size:2.5rem; margin-bottom:12px">🔭</div>
                <div style="font-family:'Space Mono',monospace; font-size:0.85rem; color:#6366f1; margin-bottom:8px">GRAPHLENS READY</div>
                <div style="font-size:0.85rem; color:#6b7280">Ask anything about the lecture.<br>Answers are grounded with timestamps & citations.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-user">
                        <div class="chat-label chat-label-user">You</div>
                        {msg["content"]}
                    </div>""", unsafe_allow_html=True)
                else:
                    # Citations HTML
                    citations_html = ""
                    if msg.get("citations"):
                        citations_html = '<div style="margin-top:10px">'
                        for c in msg["citations"]:
                            citations_html += f'<span class="timestamp-badge">{c["timestamp"]}</span>'
                            citations_html += f'<span style="font-size:0.78rem; color:#9ca3af">{c["text"][:60]}...</span><br style="margin:4px 0">'
                        citations_html += "</div>"

                    # Confidence bar
                    conf_html = ""
                    if reliability_score and msg.get("confidence"):
                        pct = int(msg["confidence"] * 100)
                        col = "#22c55e" if pct > 85 else "#f97316" if pct > 70 else "#ef4444"
                        conf_html = f"""
                        <div style="margin-top:10px; display:flex; align-items:center; gap:8px">
                            <span style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#6b7280">RELIABILITY</span>
                            <div class="confidence-wrap" style="flex:1">
                                <div class="confidence-fill" style="width:{pct}%; background:{col}"></div>
                            </div>
                            <span style="font-family:'Space Mono',monospace; font-size:0.7rem; color:{col}">{pct}%</span>
                        </div>"""

                    st.markdown(f"""
                    <div class="chat-assistant">
                        <div class="chat-label chat-label-bot">GraphLens</div>
                        {msg["content"]}
                        {citations_html}
                        {conf_html}
                    </div>""", unsafe_allow_html=True)

    # ── Input ──
    with st.container():
        input_col, btn_col = st.columns([5, 1])
        with input_col:
            user_input = st.text_input(
                "query",
                placeholder="e.g. What is gradient descent and how does it connect to backpropagation?",
                label_visibility="collapsed",
                key="chat_input"
            )
        with btn_col:
            send = st.button("Ask →", use_container_width=True)

    # ── Example prompts ──
    st.markdown('<div style="margin-top:6px; display:flex; gap:6px; flex-wrap:wrap">', unsafe_allow_html=True)
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    with ex_col1:
        if st.button("What is gradient descent?", use_container_width=True):
            user_input = "What is gradient descent?"
            send = True
    with ex_col2:
        if st.button("How does backprop work?", use_container_width=True):
            user_input = "How does backpropagation work?"
            send = True
    with ex_col3:
        if st.button("What causes overfitting?", use_container_width=True):
            user_input = "What causes overfitting?"
            send = True

    # ── Handle send ──
    if send and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("🔍 Retrieving chunks → reranking → graph expansion → generating..."):
            result = mock_query_graphlens(user_input)

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "citations": result["citations"],
            "confidence": result["confidence"],
            "chunks": result["chunks_retrieved"],
            "graph_nodes": result["graph_nodes_used"],
        })
        st.session_state.highlighted_nodes = result["highlighted_nodes"]
        st.session_state.current_timestamp = result["citations"][0]["timestamp"] if result["citations"] else None
        st.rerun()


# ══════════════════════════════════════════════
#  RIGHT — GRAPH + VIDEO PANEL
# ══════════════════════════════════════════════
with col_graph:

    # ── Knowledge Graph ──
    st.markdown('<div class="section-header">🗺️ Knowledge Graph</div>', unsafe_allow_html=True)
    graph_html = build_knowledge_graph(st.session_state.highlighted_nodes)
    components.html(graph_html, height=390, scrolling=False)

    if st.session_state.highlighted_nodes:
        st.markdown(
            f'<div style="font-size:0.72rem; color:#6b7280; margin-top:-6px; margin-bottom:8px">✦ Highlighted: '
            + " · ".join(f'<span style="color:#f97316">{n}</span>' for n in st.session_state.highlighted_nodes)
            + "</div>",
            unsafe_allow_html=True
        )

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── Video Jump ──
    st.markdown('<div class="section-header">📹 Video · Jump to Timestamp</div>', unsafe_allow_html=True)

    if st.session_state.messages and st.session_state.current_timestamp:
        last = [m for m in st.session_state.messages if m["role"] == "assistant"]
        if last:
            citations = last[-1].get("citations", [])
            ts_cols = st.columns(len(citations)) if citations else []
            for i, c in enumerate(citations):
                with ts_cols[i]:
                    if st.button(f"▶ {c['timestamp']}", use_container_width=True, key=f"ts_{i}"):
                        st.session_state.current_timestamp = c["timestamp"]
                    st.markdown(f'<div style="font-size:0.7rem; color:#6b7280; margin-top:-6px">{c["text"][:35]}...</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:0.8rem; color:#374151; padding: 12px; text-align:center">Timestamp links will appear here after your first query</div>', unsafe_allow_html=True)

    # Mock video embed area
    video_url = "https://www.youtube.com/embed/aircAruvnKk"  # Replace with actual lecture
    ts_seconds = 0
    if st.session_state.current_timestamp:
        try:
            parts = st.session_state.current_timestamp.split(":")
            ts_seconds = int(parts[0]) * 60 + int(parts[1])
        except:
            ts_seconds = 0

    components.html(f"""
    <div style="border-radius:10px; overflow:hidden; border: 1px solid #1e2030; margin-top:8px">
        <iframe
            width="100%" height="200"
            src="{video_url}?start={ts_seconds}&autoplay=0"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
    </div>
    """, height=215)

    # ── Last response stats ──
    if st.session_state.messages:
        last_bot = [m for m in st.session_state.messages if m["role"] == "assistant"]
        if last_bot:
            m = last_bot[-1]
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            s1, s2, s3 = st.columns(3)
            with s1:
                st.markdown(f'<div class="metric-box"><div class="metric-value">{m.get("chunks", "—")}</div><div class="metric-label">Chunks Used</div></div>', unsafe_allow_html=True)
            with s2:
                st.markdown(f'<div class="metric-box"><div class="metric-value">{m.get("graph_nodes", "—")}</div><div class="metric-label">Graph Nodes</div></div>', unsafe_allow_html=True)
            with s3:
                conf = m.get("confidence", 0)
                st.markdown(f'<div class="metric-box"><div class="metric-value">{int(conf*100)}%</div><div class="metric-label">Confidence</div></div>', unsafe_allow_html=True)
