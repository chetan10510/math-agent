# kb/kb_retriever.py
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import numpy as np

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "math_kb"
EMBED_MODEL_NAME = "all-mpnet-base-v2"

# Load model once
MODEL = SentenceTransformer(EMBED_MODEL_NAME)
CLIENT = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# similarity threshold (tune this later)
KB_SIM_THRESHOLD = 0.72

def embed(text: str):
    """Return normalized embedding vector"""
    v = MODEL.encode([text], convert_to_numpy=True)[0]
    return v / np.linalg.norm(v)

def query_kb(query: str, top_k: int = 3):
    """Search Qdrant for nearest KB entries"""
    q_emb = embed(query).tolist()
    res = CLIENT.search(
        collection_name=COLLECTION_NAME,
        query_vector=q_emb,
        limit=top_k
    )
    return [
        {"id": r.id, "score": r.score, "payload": r.payload}
        for r in res
    ]

def kb_hit(results):
    """Decide if top result is a KB hit"""
    if not results:
        return None
    top = results[0]
    if top["score"] >= KB_SIM_THRESHOLD:
        return top
    return None

if __name__ == "__main__":
    tests = [
        "Solve x^2 - 5x + 6 = 0",
        "What is the integral of x^2 from 0 to 1?",
        "Find area of a triangle with base 10 and height 5",
        "Integrate sin(x) from 0 to pi/2"   # not in KB → should fallback
    ]
    for q in tests:
        print("\nQUERY:", q)
        results = query_kb(q)
        if not results:
            print("No results from KB.")
            continue
        print("Top score:", results[0]["score"])
        hit = kb_hit(results)
        if hit:
            print(" KB HIT → returning stored solution:")
            print(hit["payload"].get("solution_text", "(no solution stored)"))
        else:
            print(" No KB hit (below threshold). This will go to web/MCP fallback.")
