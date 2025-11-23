from typing import List
import os
import numpy as np

# This module provides a small wrapper for requesting embeddings.
# By default, it calls OpenAI embeddings if OPENAI_API_KEY is set; otherwise,
# it falls back to a deterministic embedding (hash -> vector) for local testing.

def simple_hash_embedding(text: str, dim: int = 1536) -> List[float]:
    # deterministic pseudo-embedding for offline tests
    import hashlib
    h = hashlib.sha256(text.encode("utf-8")).digest()
    arr = [b / 255.0 for b in h]
    # tile to requested dim
    out = (arr * ((dim // len(arr)) + 1))[:dim]
    return out

class EmbeddingClient:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self.api_key = os.environ.get("OPENAI_API_KEY")

    async def embed(self, texts: List[str]) -> List[List[float]]:
        # If OPENAI_API_KEY present, you'd call OpenAI embedding endpoint here.
        # For scaffolding we return simple_hash_embedding.
        out = [simple_hash_embedding(t) for t in texts]
        return out

def cosine_similarity(a, b):
    import numpy as np
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
