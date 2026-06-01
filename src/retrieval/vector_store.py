import chromadb
from chromadb.config import Settings
from src.utils.config import CHROMA_DIR, CHROMA_COLLECTION


def get_chroma_client():
    """Initialize persistent ChromaDB client."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client


def get_or_create_collection(client):
    """Get or create the FitRAG collection."""
    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )
    return collection


def store_chunks(embedded_chunks: list[dict]):
    """
    Store embedded chunks in ChromaDB.
    """
    client = get_chroma_client()
    collection = get_or_create_collection(client)

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for chunk in embedded_chunks:
        ids.append(chunk["chunk_id"])
        embeddings.append(chunk["embedding"])
        documents.append(chunk["text"])
        metadatas.append({
            "source": chunk["source"],
            "page_num": chunk["page_num"],
            "chunk_index": chunk["chunk_index"]
        })

    # Store in batches of 100
    batch_size = 100
    for i in range(0, len(ids), batch_size):
        collection.upsert(
            ids=ids[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )
        print(f"Stored batch {i//batch_size + 1}")

    print(f"\nTotal chunks stored: {collection.count()}")
    return collection


def query_collection(query_embedding: list[float], n_results: int = 5):
    """
    Search ChromaDB for relevant chunks.
    """
    client = get_chroma_client()
    collection = get_or_create_collection(client)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    return results


def get_collection_count():
    """Return total number of chunks in ChromaDB."""
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    return collection.count()