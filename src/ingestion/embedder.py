from sentence_transformers import SentenceTransformer
from src.utils.config import EMBEDDING_MODEL
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load model once globally
model = SentenceTransformer(EMBEDDING_MODEL)


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Generate embeddings for each chunk.
    Adds 'embedding' field to each chunk dict.
    """
    print(f"Embedding {len(chunks)} chunks...")

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()

    print(f"Done. Embedding shape: {embeddings[0].shape}")
    return chunks