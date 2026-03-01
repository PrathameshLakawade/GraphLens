"""Service layer for RAG-backed responses."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from graphlens.pipelines.rag import answer_query


def answer_user_query(query: str) -> str:
    return answer_query(query)
