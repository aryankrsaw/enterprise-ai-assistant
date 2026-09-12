from app.rag.retrieval import search_similar_chunks


query = "What is working hour?"

results = search_similar_chunks(query, top_k=3)

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print(result)