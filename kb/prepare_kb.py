# kb/prepare_kb.py
import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

# Qdrant config
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "math_kb"
EMBED_MODEL_NAME = "all-mpnet-base-v2"  # sentence-transformers model

def load_docs(path):
    """Load documents from JSONL file"""
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line.strip()))
    return docs

def main():
    print("Loading embedding model:", EMBED_MODEL_NAME)
    model = SentenceTransformer(EMBED_MODEL_NAME)

    # Load KB data
    docs = load_docs("kb/sample_kb.jsonl")
    if not docs:
        print(" No docs found in kb/sample_kb.jsonl")
        return

    # Combine question + solution for embeddings
    texts = [d["question"] + "\n\n" + d.get("solution_text", "") for d in docs]

    print(f"Encoding {len(texts)} docs into embeddings...")
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    # Connect to Qdrant
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    # Create collection (reset each time for now)
    print("Creating collection in Qdrant...")
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=rest.VectorParams(size=embeddings.shape[1], distance=rest.Distance.COSINE),
    )

    # Prepare points with integer IDs
    points = []
    for i, emb in enumerate(embeddings):
        doc = docs[i]
        payload = {
            "question": doc["question"],
            "solution_text": doc.get("solution_text", ""),
            "source": "sample_kb",
        }
        points.append(
            rest.PointStruct(
                id=i+1,   #  use integers (1, 2, 3...)
                vector=emb.tolist(),
                payload=payload,
            )
        )

    # Upload points to Qdrant
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f" Inserted {len(points)} docs into '{COLLECTION_NAME}' collection.")

if __name__ == "__main__":
    main()
