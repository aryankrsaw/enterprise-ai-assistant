import pymupdf

def extract_text_from_pdf(pdf_path: str)-> str:
    document = pymupdf.open(pdf_path)
    text=""
    for page_number,page in enumerate(document):
        page_text = page.get_text()

        text += f"\n--- Page {page_number + 1} ---\n"
        text += page_text

    document.close()

    return text

def create_chunks(text: str, chunk_size: int = 500, overlap: int = 100):
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks
