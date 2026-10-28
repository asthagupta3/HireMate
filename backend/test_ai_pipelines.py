from app.ai.pdf_parser import extract_text
from app.ai.chunker import chunk_text
from app.ai.embeddings import create_embeddings
from app.ai.vector_store import create_index



text = extract_text(
    "app/uploads/MA25M102 (6).pdf"
)


chunks = chunk_text(text)


vectors = create_embeddings(
    chunks
)


index=create_index(
    vectors
)


print(
    "Chunks:",
    len(chunks)
)


print(
    "Embedding shape:",
    vectors.shape
)