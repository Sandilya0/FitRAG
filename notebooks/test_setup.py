import os
from dotenv import load_dotenv

load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HUGGINGFACE_TOKEN")

# Test Groq LLM
from langchain_groq import ChatGroq
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("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")
)
response = llm.invoke("Say hello in one sentence")
print("Groq LLM works:", response.content)

# Test Groq Vision
from groq import Groq
client = Groq(api_key=os.getenv("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"))
response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "user",
            "content": "Say hello in one sentence"
        }
    ]
)
print("Groq Vision works:", response.choices[0].message.content)

# Test Embeddings
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode("Test sentence")
print("Embeddings work, shape:", embedding.shape)

# Test ChromaDB
import chromadb
client = chromadb.Client()
collection = client.create_collection("test")
print("ChromaDB works:", collection.name)

# Test PyMuPDF
import fitz
print("PyMuPDF works:", fitz.__version__)

print("\n✅ All systems go!")