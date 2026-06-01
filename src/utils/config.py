import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("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")
HUGGINGFACE_TOKEN = os.getenv("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")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_PAPERS_DIR = os.path.join(DATA_DIR, "raw", "papers")
RAW_IMAGES_DIR = os.path.join(DATA_DIR, "raw", "images")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ChromaDB
CHROMA_COLLECTION = "fitrag"

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Groq
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_TEMPERATURE = 0.2
GROQ_MAX_TOKENS = 1024