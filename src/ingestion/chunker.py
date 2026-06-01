from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_pages(pages: list[dict]) -> list[dict]:
    """
    Split extracted pages into smaller chunks for embedding.
    Each chunk retains metadata about its source and page number.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []

    for page in pages:
        text = page["text"]
        source = page["source"]
        page_num = page["page_num"]

        # Split text into chunks
        split_texts = splitter.split_text(text)

        for i, chunk_text in enumerate(split_texts):
            chunks.append({
                "text": chunk_text,
                "source": source,
                "page_num": page_num,
                "chunk_index": i,
                "chunk_id": f"{source}_page{page_num}_chunk{i}"
            })

    print(f"Total chunks created: {len(chunks)}")
    return chunks