# feedback_agent.py
import json
import os
from datetime import datetime
from kb.prepare_kb import load_docs
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
import numpy as np

# Qdrant settings
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "math_kb"
EMBED_MODEL_NAME = "all-mpnet-base-v2"

MODEL = SentenceTransformer(EMBED_MODEL_NAME)
CLIENT = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

FEEDBACK_FILE = "feedback.jsonl"

def log_feedback(query: str, solution: str, feedback: str, correction: str = None):
    """Log human feedback into feedback.jsonl"""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "solution": solution,
        "feedback": feedback,
        "correction": correction
    }
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"✅ Feedback logged: {feedback}")

    # If correction is provided, insert it into KB
    if feedback.lower() == "bad" and correction:
        add_correction_to_kb(query, correction)

def add_correction_to_kb(query: str, correction: str):
    """Add corrected solution into Qdrant KB"""
    emb = MODEL.encode([query + "\n\n" + correction], convert_to_numpy=True)[0]

    point_id = int(datetime.utcnow().timestamp())  # unique integer ID
    payload = {
        "question": query,
        "solution_text": correction,
        "source": "human_feedback"
    }

    CLIENT.upsert(
        collection_name=COLLECTION_NAME,
        points=[rest.PointStruct(id=point_id, vector=emb.tolist(), payload=payload)]
    )
    print(f"📚 Correction added to KB for future queries: {query}")

if __name__ == "__main__":
    # Example demo run
    q = "What is the integral of x^2 from 0 to 1?"
    sol = "Based on web search: (maybe incorrect)"
    print("Q:", q)
    print("Solution:", sol)

    # Simulate human feedback
    feedback = "bad"
    correction = "Step 1: ∫ x^2 dx = x^3/3\nStep 2: Evaluate from 0 to 1 → 1/3\nAnswer: 1/3."
    log_feedback(q, sol, feedback, correction)
