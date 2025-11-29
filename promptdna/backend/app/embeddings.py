from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL
import numpy as np

_model = None


def load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_text(text: str):
    model = load_model()
    v = model.encode(text, normalize_embeddings=True)
    return np.array(v, dtype='float32')
