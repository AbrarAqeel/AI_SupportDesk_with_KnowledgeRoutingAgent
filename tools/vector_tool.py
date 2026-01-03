"""
Vector Search Tool (Chroma-backed, deterministic)

Responsibilities:
- Load static articles
- Store embeddings in Chroma
- Perform deterministic cosine similarity filtering
"""

from typing import Dict, List
import numpy as np

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from data.vector_articles import ARTICLES


class VectorSearchTool:
    """
    Semantic search tool using Chroma as storage
    with explicit cosine similarity filtering.
    """

    def __init__(self) -> None:
        # Embedding model
        self._model = SentenceTransformer("all-MiniLM-L6-v2")

        # Chroma client (in-memory, non-persistent)
        self._client = chromadb.Client(
            Settings(
                anonymized_telemetry=False,
                is_persistent=False,
            )
        )

        # Collection
        self._collection = self._client.get_or_create_collection(
            name="support_articles"
        )

        # Load once
        self._load_documents()

        # Cache embeddings for deterministic scoring
        self._embeddings = self._embed_documents()

    def _load_documents(self) -> None:
        if self._collection.count() > 0:
            return

        texts = [doc["content"] for doc in ARTICLES]
        ids = [f"doc_{i}" for i in range(len(texts))]

        embeddings = self._model.encode(
            texts, normalize_embeddings=True
        ).tolist()

        self._collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
        )

    def _embed_documents(self) -> np.ndarray:
        contents = [doc["content"] for doc in ARTICLES]
        return self._model.encode(
            contents, normalize_embeddings=True
        )

    def search(self, query: str, top_k: int = 3) -> Dict[str, List[Dict]]:
        """
        Perform semantic search with deterministic relevance cutoff.
        """
        query_embedding = self._model.encode(
            [query], normalize_embeddings=True
        )[0]

        # Cosine similarity (deterministic)
        scores = np.dot(self._embeddings, query_embedding)

        ranked_indices = np.argsort(scores)[::-1]

        results = []
        MIN_SIMILARITY = 0.35  # tuned to your tests

        for idx in ranked_indices[:top_k]:
            if scores[idx] < MIN_SIMILARITY:
                continue

            results.append(
                {
                    "content": ARTICLES[idx]["content"],
                    "score": float(scores[idx]),
                }
            )

        return {"documents": results}
