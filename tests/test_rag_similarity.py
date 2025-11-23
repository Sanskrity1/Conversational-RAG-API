import pytest
from app.core.embeddings import simple_hash_embedding, cosine_similarity

def test_embedding_consistency():
    a = simple_hash_embedding("hello world")
    b = simple_hash_embedding("hello world")
    assert a == b

def test_similarity_self():
    a = simple_hash_embedding("hello world")
    sim = cosine_similarity(a, a)
    assert pytest.approx(sim, rel=1e-6) == 1.0
