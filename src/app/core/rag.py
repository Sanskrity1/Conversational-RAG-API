import asyncio
from typing import List
from dataclasses import dataclass
from pathlib import Path
from app.core.embeddings import EmbeddingClient, cosine_similarity

@dataclass
class ContextChunk:
    text: str
    embedding: List[float]
    meta: dict

class Retriever:
    def __init__(self, docs_path: str = "./src/app/data", embedding_model: str = "text-embedding-3-small"):
        self.docs_path = Path(docs_path)
        self.client = EmbeddingClient(model=embedding_model)
        self.chunks: List[ContextChunk] = []

    async def load_documents(self) -> None:
        for p in sorted(self.docs_path.glob("**/*")):
            if p.is_file() and p.suffix in {".txt", ".md"}:
                text = p.read_text(encoding="utf-8")
                paragraphs = [para.strip() for para in text.split("\n\n") if para.strip()]
                for i, para in enumerate(paragraphs):
                    self.chunks.append(ContextChunk(text=para, embedding=[], meta={"source": str(p), "title": p.name, "idx": i}))

        texts = [c.text for c in self.chunks]
        if texts:
            embeddings = await self.client.embed(texts)
            for c, e in zip(self.chunks, embeddings):
                c.embedding = e

    async def get_relevant_chunks(self, query: str, top_k: int = 4) -> List[ContextChunk]:
        q_emb = (await self.client.embed([query]))[0]
        scored = [(cosine_similarity(q_emb, c.embedding), c) for c in self.chunks if c.embedding]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:top_k]]
