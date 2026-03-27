import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

FAISS_INDEX_FILE = "logs.index"
DOCUMENTS_FILE   = "documents.pkl"

def load_index():
    index = faiss.read_index(FAISS_INDEX_FILE)
    with open(DOCUMENTS_FILE, 'rb') as f:
        documents = pickle.load(f)
    return index, documents

def search(query, index, documents, model, top_k=5):
    """Search logs by meaning, not just keywords"""


    query_vector = model.encode([query]).astype('float32')

    
    distances, indices = index.search(query_vector, top_k)

    
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        doc = documents[idx].copy()
        doc["relevance_score"] = round(float(dist), 4)
        results.append(doc)

    return results

def print_results(query, results):
    print(f"\nQuery: '{query}'")
    print(f"Top {len(results)} results:")
    print("-" * 60)
    for i, doc in enumerate(results):
        print(f"\n#{i+1} [Score: {doc['relevance_score']}]")
        print(f"  Time:      {doc['timestamp']}")
        print(f"  Severity:  {doc['severity']}")
        print(f"  Component: {doc['component']}")
        print(f"  Message:   {doc['message']}")

if __name__ == "__main__":
    print("Loading index and model...")
    index, documents = load_index()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Ready!\n")

    
    queries = [
        "block transfer failed",
        "disk storage error",
        "connection timeout"
    ]

    for query in queries:
        results = search(query, index, documents, model, top_k=3)
        print_results(query, results)
        print("\n" + "="*60)