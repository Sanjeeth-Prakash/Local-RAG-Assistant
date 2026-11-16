"""
RAG Chat with Keyword Search (Ultra-Lightweight)
=================================================

Why this version:
- No external embedding libraries needed
- Pure Python keyword overlap search
- Teaches RAG concept without dependency hell
- Works immediately on any Python install
"""

import requests
import os

def load_docs(folder):
    """Load all .py files into memory."""
    docs = []
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                        text = fp.read()
                    docs.append({"source": path, "text": text})
                except Exception as e:
                    print(f"Skipped {path}: {e}")
    return docs

def keyword_search(query, docs, top_k=3):
    """Simple keyword overlap scoring."""
    query_words = set(query.lower().split())
    scores = []
    for doc in docs:
        text_words = set(doc["text"].lower().split())
        overlap = len(query_words & text_words)
        scores.append((overlap, doc))
    scores.sort(key=lambda x: x[0], reverse=True)
    # Return top_k docs with non-zero score
    return [doc for score, doc in scores[:top_k] if score > 0]

def answer(query, docs):
    """Retrieve relevant docs and answer using Llama 3.1."""
    relevant = keyword_search(query, docs)

    if not relevant:
        return "No relevant documents found. Try a different question."

    # Build context from relevant docs
    context_parts = []
    for d in relevant:
        snippet = d["text"][:1000]  # Limit snippet size
        context_parts.append(f"Source: {d['source']}\n{snippet}")

    context = "\n\n=== Context ===\n".join(context_parts)

    # Build grounded prompt
    prompt = f"""
You are a helpful coding assistant. Use ONLY the following context to answer.

Context:
{context}

Question: {query}

Answer concisely and cite the source files you used.
"""

    # Call local Ollama
    resp = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "llama3.1", "prompt": prompt, "stream": False}
    )
    return resp.json()["response"]

if __name__ == "__main__":
    print("=== RAG Chat with Your Docs (Keyword Search) ===")
    docs = load_docs("D:/OmniRoute")
    print(f"Loaded {len(docs)} Python files.")
    print("Ask a question about your code:")
    q = input(">> ")
    print("\nAnswer:")
    print(answer(q, docs))
