# 🔭 GraphLens — Frontend Setup

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

## Project Structure
```
graphlens/
├── app.py              ← Main Streamlit UI (start here)
├── requirements.txt    ← All dependencies
├── pipeline/           ← (you build this)
│   ├── chunker.py      ← Step 1: Preprocessing & Chunking
│   ├── retriever.py    ← Step 2: ANN Retrieval (FAISS)
│   ├── reranker.py     ← Step 3: Cross-encoder Reranking
│   ├── graph.py        ← Step 4: Neo4j Knowledge Graph
│   └── generator.py    ← Step 5: Grounded LLM Response
└── .env                ← API keys (never commit this!)
```

## Connecting Your Real Pipeline

In `app.py`, find the `mock_query_graphlens()` function and replace it:

```python
def mock_query_graphlens(question: str) -> dict:
    # REPLACE THIS ↓ with your real pipeline
    from pipeline.retriever import retrieve_chunks
    from pipeline.reranker import rerank
    from pipeline.graph import get_graph_context
    from pipeline.generator import generate_answer

    chunks    = retrieve_chunks(question, top_k=5)
    reranked  = rerank(question, chunks)
    graph_ctx = get_graph_context(question)
    answer    = generate_answer(question, reranked, graph_ctx)

    return {
        "answer":           answer["text"],
        "citations":        answer["citations"],      # [{timestamp, text}]
        "highlighted_nodes": graph_ctx["nodes"],      # list of node names
        "confidence":       answer["confidence"],     # float 0-1
        "chunks_retrieved": len(reranked),
        "graph_nodes_used": len(graph_ctx["nodes"]),
    }
```

## Environment Variables (.env)
```
OPENAI_API_KEY=your_key_here
# OR
ANTHROPIC_API_KEY=your_key_here

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```
