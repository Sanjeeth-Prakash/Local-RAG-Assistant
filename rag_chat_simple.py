"""
RAG Chat with Local Docs — Simple Embedding Version
====================================================

Why this version:
- Bypasses chromadb's embedding function bugs
- Uses sentence-transformers directly for embeddings
- Still gives you a working RAG system
"""

import chromadb
from sentence_transformers import SentenceTransformer
import requests
import os

# Initialize embedding model and vector DB
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="D:/OmniRoute/vector_db")
collection = client.get_or_create_collection(name="docs")

def ingest(folder):
    """Read all .py files and store them in vector DB with embeddings."""
    count = 0
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                        text = fp.read()
                    # Create manual embeddings
                    emb = model.encode(text).tolist()
                    collection.add(
                        documents=[text],
                        embeddings=[emb],
                        metadatas=[{"source": path}],
                        ids=[path]
                    )
                    print(f"Ingested: {path}")
                    count += 1
                except Exception as e:
                    print(f"Skipped {path}: {e}")
    print(f"Total files ingested: {count}")

def query(q):
    """Search vector DB and answer with Llama 3.1."""
    # Embed query
    q_emb = model.encode(q).tolist()
    # Find closest documents
    res = collection.query(query_embeddings=[q_emb], n_results=3)
    context = "\n\n=== Context ===\n".join(res["documents"][0])

    # Build grounded prompt
    prompt = f"""
You are a helpful coding assistant. Use ONLY the following context to answer.

Context:
{context}

Question: {q}

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
    ingest("D:/OmniRoute")
    print("\nAsk a question about your code:")
    q = input(">> ")
    print("\nAnswer:")
    print(query(q))
