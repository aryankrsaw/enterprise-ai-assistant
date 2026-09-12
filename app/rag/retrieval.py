from app.rag.vector_store import collection
from app.rag.embeddings import create_embeddings


def search_similar_chunks(query: str, top_k: int = 3):
    query_embedding = create_embeddings([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    return results["documents"][0]