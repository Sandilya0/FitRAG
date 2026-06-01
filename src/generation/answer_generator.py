from src.ingestion.embedder import embed_chunks
from src.retrieval.vector_store import query_collection
from src.generation.prompt_builder import build_system_prompt, build_user_prompt
from src.generation.llm import generate_response


def get_query_embedding(question: str) -> list[float]:
    """Embed a single query string."""
    temp_chunk = [{
        "text": question,
        "source": "query",
        "page_num": 0,
        "chunk_index": 0,
        "chunk_id": "query_temp"
    }]
    embedded = embed_chunks(temp_chunk)
    return embedded[0]["embedding"]


def format_results(raw_results: dict) -> list[dict]:
    """Convert ChromaDB results into clean list of chunks."""
    chunks = []
    documents = raw_results.get("documents", [[]])[0]
    metadatas = raw_results.get("metadatas", [[]])[0]
    distances = raw_results.get("distances", [[]])[0]

    for doc, meta, dist in zip(documents, metadatas, distances):
        chunks.append({
            "text": doc,
            "source": meta.get("source", "Unknown"),
            "page_num": meta.get("page_num", 0),
            "relevance_score": round(1 - dist, 3)
        })

    return chunks


def ask(question: str, user_profile: dict = {}, n_results: int = 5) -> dict:
    """
    Full RAG pipeline:
    1. Embed the question
    2. Retrieve relevant chunks from ChromaDB
    3. Build prompt with user profile + context
    4. Generate answer with Groq
    5. Return answer + sources
    """
    print(f"\nQuestion: {question}")
    print("Retrieving relevant research...")

    # Step 1 — embed question
    query_embedding = get_query_embedding(question)

    # Step 2 — retrieve chunks
    raw_results = query_collection(query_embedding, n_results=n_results)
    context_chunks = format_results(raw_results)

    print(f"Found {len(context_chunks)} relevant chunks")

    # Step 3 — build prompt
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(question, user_profile, context_chunks)

    # Step 4 — generate answer
    print("Generating answer...")
    answer = generate_response(system_prompt, user_prompt)

    # Step 5 — return result
    sources = list({chunk["source"] for chunk in context_chunks})

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "context_chunks": context_chunks
    }