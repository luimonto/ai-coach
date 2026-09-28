from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.knowledge_chunk import KnowledgeChunk


class KnowledgeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, chunk: KnowledgeChunk) -> KnowledgeChunk:
        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)
        return chunk

    def search_similar(
        self,
        embedding: list[float],
        limit: int = 5,
        category: str | None = None,
    ) -> list[KnowledgeChunk]:

        # Find the knowledge chunks whose embeddings are semantically closest to the query embedding.
        distance = KnowledgeChunk.embedding.cosine_distance(
            embedding
        )

        statement = (
            select(KnowledgeChunk)
            .order_by(distance)
            .limit(limit)
        )

        if category:
            statement = statement.where(
                KnowledgeChunk.category == category
            )

        return list(self.db.scalars(statement).all())