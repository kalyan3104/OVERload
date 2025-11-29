import faiss
import numpy as np
import os
from config import FAISS_INDEX_PATH


class FaissIndex:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = None
        self.ids = []
        if os.path.exists(FAISS_INDEX_PATH):
            try:
                self.index = faiss.read_index(FAISS_INDEX_PATH)
                print("Loaded FAISS index from", FAISS_INDEX_PATH)
            except Exception:
                print("Failed to load FAISS index, creating new.")
                self.index = faiss.IndexFlatIP(self.dim)
        else:
            self.index = faiss.IndexFlatIP(self.dim)

    def _prepare_vector(self, vector: np.ndarray) -> np.ndarray:
        vec = np.asarray(vector, dtype="float32")
        if vec.ndim == 1:
            vec = vec.reshape(1, -1)
        return np.ascontiguousarray(vec)

    def add(self, vector: np.ndarray, id_str: str):
        vec = self._prepare_vector(vector)
        faiss.normalize_L2(vec)
        self.index.add(vec)
        self.ids.append(id_str)
        self.save()

    def save(self):
        faiss.write_index(self.index, FAISS_INDEX_PATH)

    def search(self, vector: np.ndarray, topk=5):
        if self.index.ntotal == 0:
            return [], []
        vec = self._prepare_vector(vector)
        faiss.normalize_L2(vec)
        D, I = self.index.search(vec, topk)
        mapped_ids = [self.ids[i] if 0 <= i < len(self.ids) else None for i in I[0]]
        return D[0].tolist(), mapped_ids
