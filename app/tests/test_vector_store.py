from app.rag.ingestion import extract_text_from_pdf, create_chunks
from app.rag.embeddings import create_embeddings
from app.rag.vector_store import store_chunks


pdf_path = "app/documents/TechNova Solutions Employee Handbook.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = create_chunks(text)

embeddings = create_embeddings(chunks)

store_chunks(chunks, embeddings)

print(f"Stored {len(chunks)} chunks successfully.")