import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from log_parser import load_logs


FAISS_INDEX_FILE = "logs.index"
DOCUMENTS_FILE   = "documents.pkl"
LOG_FILE = r"C:\Users\cyril\Downloads\archive (8)\HDFS_2k\HDFS_2k.log"

def build_index(documents):
    """Convert log messages to vectors and store in FAISS"""
    
    print("Loading embedding model...")
    print("(First time downloads ~90MB, be patient)")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model loaded!")

    
    messages = [doc["message"] for doc in documents]
    print(f"\nEmbedding {len(messages)} log lines...")
    print("This will take 1-2 minutes on CPU...")

    
    embeddings = model.encode(
        messages,
        batch_size=32,        
        show_progress_bar=True
    )

    print(f"\nEmbedding shape: {embeddings.shape}")
    

    
    dimension = embeddings.shape[1]  
    index = faiss.IndexFlatL2(dimension)  

    
    embeddings_float32 = np.array(embeddings).astype('float32')
    index.add(embeddings_float32)
    print(f"Added {index.ntotal} vectors to FAISS index")


    faiss.write_index(index, FAISS_INDEX_FILE)
    print(f"Saved FAISS index to {FAISS_INDEX_FILE}")

    
    with open(DOCUMENTS_FILE, 'wb') as f:
        pickle.dump(documents, f)
    print(f"Saved documents to {DOCUMENTS_FILE}")

    return index, embeddings

def load_index():
    """Load saved index from disk"""
    index = faiss.read_index(FAISS_INDEX_FILE)
    with open(DOCUMENTS_FILE, 'rb') as f:
        documents = pickle.load(f)
    return index, documents

if __name__ == "__main__":
    
    if os.path.exists(FAISS_INDEX_FILE):
        print("Index already exists! Loading from disk...")
        index, documents = load_index()
        print(f"Loaded {index.ntotal} vectors from disk")
    else:
        
        documents = load_logs(LOG_FILE)
        index, embeddings = build_index(documents)
    
    print("\nDay 2 Complete! Embeddings stored in FAISS.")
    print(f"Index contains {index.ntotal} searchable log lines")