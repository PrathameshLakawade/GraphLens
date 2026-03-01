"""Streamlit frontend entry point."""

import json
import os
from urllib import error, request

import streamlit as st


def call_backend(query: str) -> str:
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    payload = json.dumps({"query": query}).encode("utf-8")
    req = request.Request(
        f"{backend_url}/api/v1/query",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data["answer"]
    except error.URLError as exc:
        return f"Backend request failed: {exc}"


def main() -> None:
    st.set_page_config(page_title="GraphLens", layout="wide")
    st.title("GraphLens")
    st.caption("Streamlit frontend for the GraphLens API.")

    query = st.text_input("Ask a question")
    if st.button("Run") and query:
        st.write(call_backend(query))


if __name__ == "__main__":
    main()
