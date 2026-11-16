"""
RAG Chat with Local Docs (Day 3 Project)
========================================

What this does:
- Stores your Python files in a vector database (ChromaDB)
- Embeds your code into vectors (numerical representations)
- When you ask a question, finds relevant code snippets
- Sends those snippets + question to Llama 3.1
- Returns an answer grounded in YOUR code

Why this matters for jobs:
- This is the foundation of all enterprise AI apps (ChatGPT for code, Copilot, private knowledge bases)
- Companies pay for RAG engineers who can build private AI assistants
- Solves the "LLM doesn't know your business data" problem

How it works:
1. Ingest: Read your Python files → split into chunks → embed into vectors → store in ChromaDB
2. Retrieve: Embed user question → find closest vectors (cosine similarity)
3. Generate: Send retrieved snippets + question to Llama 3.1 → grounded answer
"""

import chromadb
from chromadb.utils import embedding_functions
import requests
import os

# Initialize vector DB
client = chromadb.PersistentClient(path="D:/OmniRoute/vector_db")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Create (or get) collection
collection = client.get_or_create_collection(
    name="docs",
    embedding_function=ef
)

# Simple ingestion - just load your Python files for now
def ingest_files(folder):
    """Read all .py files and store them in vector DB."""
    count = 0
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                        text = fp.read()
                    collection.add(
                        documents=[text],
                        metadatas=[{"source": path}],
                        ids=[path]
                    )
                    print(f"Ingested: {path}")
                    count += 1
                except Exception as e:
                    print(f"Skipped {path}: {e}")
    print(f"Total files ingested: {count}")

# Search and answer
def rag_query(query):
    """Retrieve relevant docs and answer using Llama 3.1."""
    # Retrieve relevant snippets
    results = collection.query(query_texts=[query], n_results=3)
    context = "\n\n=== Context ===\n".join(results["documents"][0])

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
    print("=== RAG Chat with Your Docs ===")
    ingest_files("D:/OmniRoute")
    print("\nAsk a question about your code:")
    q = input(">> ")
    print("\nAnswer:")
    print(rag_query(q))
