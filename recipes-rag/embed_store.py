# embed_store.py
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from typing import List, Tuple

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class EmbedStore:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.docs = []  # list of dict {id, text}
        self.embs = None

    def add(self, doc_id: str, text: str):
        self.docs.append({"id": doc_id, "text": text})
        emb = self.model.encode([text], normalize_embeddings=True)
        self.embs = emb if self.embs is None else np.vstack([self.embs, emb])

    def bulk_add(self, items: List[Tuple[str,str]]):
        texts = [t for _, t in items]
        ids = [i for i, _ in items]
        embs = self.model.encode(texts, normalize_embeddings=True)
        for i, t in zip(ids, texts):
            self.docs.append({"id": i, "text": t})
        self.embs = embs if self.embs is None else np.vstack([self.embs, embs])

    def retrieve(self, query: str, top_k: int = 3):
        q_emb = self.model.encode([query], normalize_embeddings=True)[0]
        sims = (self.embs @ q_emb).astype(float)
        idxs = list(np.argsort(-sims)[:top_k])
        return [(self.docs[i]["id"], self.docs[i]["text"], float(sims[i])) for i in idxs]

    def save(self, path="store.json"):
        data = {"docs": self.docs, "embs": self.embs.tolist() if self.embs is not None else None}
        with open(path, "w") as f:
            json.dump(data, f)

    def load(self, path="store.json"):
        with open(path) as f:
            data = json.load(f)
        self.docs = data["docs"]
        self.embs = np.array(data["embs"]) if data["embs"] is not None else None
