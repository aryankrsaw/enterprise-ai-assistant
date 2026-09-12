from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    try:
        embeddings = model.encode(chunks)
        return embeddings

    except Exception as e:
        print("Error occurred while converting text into vectors:", e)
        return None