import json
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Any, Tuple

BASE_DIR = os.path.dirname(__file__)
KNOWLEDGE_PATH = os.path.join(BASE_DIR, "knowledge.json")
INDEX_PATH = os.path.join(BASE_DIR, "rag_index.faiss")
METADATA_PATH = os.path.join(BASE_DIR, "rag_metadata.pkl")

class RAGRetriever:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.metadata = []
        self.dimension = 384  # MiniLM dim
        self._load_index()

    def _load_knowledge(self) -> List[str]:
        """Load and chunk knowledge.json into texts."""
        with open(KNOWLEDGE_PATH, 'r') as f:
            knowledge = json.load(f)
        
        texts = []
        chunks = []
        for entry in knowledge:
            symptoms_str = ', '.join(entry['symptoms'])
            precautions_str = '; '.join(entry['precautions'])
            text = f"Disease: {entry['disease_name']}. Symptoms: {symptoms_str}. Summary: {entry['summary']}. Precautions: {precautions_str}"
            texts.append(text)
            chunks.append(entry)
        
        self.metadata = chunks
        return texts

    def build_index(self):
        """Build FAISS index from knowledge."""
        texts = self._load_knowledge()
        embeddings = self.model.encode(texts)
        
        # FAISS Index
        self.index = faiss.IndexFlatIP(self.dimension)  # Cosine sim (inner product on unit vec)
        faiss.normalize_L2(embeddings)  # For cosine
        self.index.add(embeddings.astype('float32'))
        
        # Save
        faiss.write_index(self.index, INDEX_PATH)
        with open(METADATA_PATH, 'wb') as f:
            pickle.dump(self.metadata, f)
        
        print(f"RAG index built: {len(texts)} docs")

    def _load_index(self):
        """Load existing index."""
        if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(METADATA_PATH, 'rb') as f:
                self.metadata = pickle.load(f)
            print("RAG index loaded")

    def retrieve(self, query: str, k: int = 3, threshold: float = 0.5) -> List[Tuple[Dict[str, Any], float]]:
        """Retrieve top-k relevant docs with scores. Returns [] if no scores >= threshold."""
        if self.index is None:
            raise ValueError("Index not built. Run build_index() first.")
        
        query_emb = self.model.encode([query])
        faiss.normalize_L2(query_emb)
        distances, indices = self.index.search(query_emb.astype('float32'), k)
        scores = distances[0]  # IP scores (cosine since normalized)
        
        print(f"Query: {query}")
        results = []
        for i, (score, idx) in enumerate(zip(scores, indices[0])):
            disease = self.metadata[idx]['disease_name']
            print(f"Candidate {i+1}: {disease}, Score: {score:.3f}")
            if score >= threshold:
                meta = self.metadata[idx]
                print(f"Confident match: {disease}, Score: {score:.3f}")
                results.append((meta, score))
        
        if not results:
            print(f"No confident matches (threshold={threshold})")
        
        return results[:k]

# Global instance
retriever = RAGRetriever()
