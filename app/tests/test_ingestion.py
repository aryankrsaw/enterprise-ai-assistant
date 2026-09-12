from app.rag.ingestion import extract_text_from_pdf, create_chunks
from app.rag.embeddings import create_embeddings


pdf_path = "app/documents/TechNova Solutions Employee Handbook.pdf"

text = extract_text_from_pdf(pdf_path)

# print(text[:5000])

chunks = create_chunks(text)

# for chunk in chunks:
#     print(chunk)
#     print("----------------------------------------------------------------------------------")

embeddings = create_embeddings(chunks)

for i, embedding in enumerate(embeddings):
    print(f"Chunk {i + 1}: {embedding}")