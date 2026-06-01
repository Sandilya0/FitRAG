import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion.pdf_parser import parse_pdf, parse_all_pdfs
from src.utils.config import RAW_PAPERS_DIR

# Test on one PDF first
pdf_files = [f for f in os.listdir(RAW_PAPERS_DIR) if f.endswith(".pdf")]
first_pdf = os.path.join(RAW_PAPERS_DIR, pdf_files[0])

print("Testing on:", pdf_files[0])
result = parse_pdf(first_pdf)

print("\nFirst 500 chars of page 1:")
print(result["pages"][0]["text"][:500])
print("\nImages found:", len(result["images"]))

# Test chunker
from src.ingestion.chunker import chunk_pages

chunks = chunk_pages(result["pages"])
print(f"\nTotal chunks: {len(chunks)}")
print("\nSample chunk:")
print(chunks[0]["text"])
print("\nChunk metadata:")
print(f"  Source: {chunks[0]['source']}")
print(f"  Page: {chunks[0]['page_num']}")
print(f"  ID: {chunks[0]['chunk_id']}")

# Test embedder
from src.ingestion.embedder import embed_chunks

embedded_chunks = embed_chunks(chunks)
print(f"\nEmbedding sample (first 5 values):")
print(embedded_chunks[0]["embedding"][:5])
print(f"Embedding size: {len(embedded_chunks[0]['embedding'])}")

# Test vector store
from src.retrieval.vector_store import store_chunks, query_collection
from src.ingestion.embedder import embed_chunks as get_embedding

store_chunks(embedded_chunks)

# Test a query
query = "does creatine help with recovery?"
query_embedding = get_embedding([{"text": query, "source": "test", 
                                   "page_num": 0, "chunk_index": 0, 
                                   "chunk_id": "test"}])
results = query_collection(query_embedding[0]["embedding"])

print("\nTop result for query:", query)
print(results["documents"][0][0][:300])
print("\nSource:", results["metadatas"][0][0]["source"])

# Ingest ALL papers
print("\n--- Ingesting all papers ---")
from src.ingestion.pdf_parser import parse_all_pdfs

all_results = parse_all_pdfs()

all_chunks = []
for result in all_results:
    chunks = chunk_pages(result["pages"])
    all_chunks.extend(chunks)

print(f"\nTotal chunks across all papers: {len(all_chunks)}")

embedded_all = embed_chunks(all_chunks)
store_chunks(embedded_all)