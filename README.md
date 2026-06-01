# FitRAG — Recovery Intelligence Platform

A full-stack, retrieval-augmented (RAG) fitness assistant that answers recovery, sleep, and performance questions grounded in peer-reviewed research — and personalizes those answers to a user's biometric data.

Ask *"Why is my recovery low after drinking alcohol?"* and FitRAG retrieves the relevant findings from a corpus of sports-science papers, combines them with your personal metrics, and returns a cited, personalized answer instead of generic advice.

---

## Why this exists

Most fitness advice online is unsourced opinion. FitRAG answers questions using a curated base of peer-reviewed research, returns the sources behind every answer, and tailors the response to the user's own data — whether that comes from a WHOOP export or a manual profile.

---

## Features

- **Research-grounded answers** — every response is generated from retrieved chunks of real sports-science papers, with sources returned alongside the answer.
- **Personalization** — answers factor in the user's sleep, HRV, alcohol, stress, and training inputs.
- **WHOOP integration** — upload a WHOOP CSV export and FitRAG parses your latest metrics (recovery, HRV, resting HR, sleep, strain) and computes personal baselines.
- **Device-optional** — no wearable required; a manual profile feeds the same pipeline.
- **Clean web UI** — a React single-page app with dashboard, ask, profile, WHOOP, and history views.

---

## Architecture

```
                    ┌─────────────────────────────┐
                    │      React Frontend (Vite)   │
                    │  Dashboard · Ask · Profile   │
                    │      WHOOP · History         │
                    └──────────────┬──────────────┘
                                   │  HTTP (REST)
                    ┌──────────────▼──────────────┐
                    │       FastAPI Backend        │
                    │   /ask  /ask/manual          │
                    │   /upload/whoop  /upload/pdf │
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────────────────────────────────────┐
        │                RAG Pipeline                   │
        │                                               │
        │  Question + Profile                           │
        │        │                                      │
        │        ▼                                      │
        │  Embed query  ──►  ChromaDB vector search     │
        │        │                                      │
        │        ▼                                      │
        │  Build prompt (profile + retrieved research)  │
        │        │                                      │
        │        ▼                                      │
        │  Groq LLaMA 3.3 70B  ──►  Answer + sources    │
        └───────────────────────────────────────────────┘

   Ingestion (offline):
   PDFs ─► parse text + images ─► chunk ─► embed ─► ChromaDB
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS |
| Backend | FastAPI, Uvicorn |
| LLM | Groq — LLaMA 3.3 70B |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` (384-dim) |
| Vector store | ChromaDB (persistent, cosine) |
| PDF parsing | PyMuPDF, Tesseract OCR, Poppler |
| Evaluation | Ragas |
| Language | Python 3.11, JavaScript |

**Knowledge base:** 14 peer-reviewed papers → ~2,400 indexed chunks.

---

## Project Structure

```
FitRAG/
├── api/                    # FastAPI app
│   ├── main.py             # App entry, CORS, routers
│   ├── routes/             # /ask and /upload endpoints
│   └── models/             # Pydantic schemas
├── src/
│   ├── ingestion/          # PDF parsing, chunking, embedding
│   ├── retrieval/          # ChromaDB vector store + search
│   ├── generation/         # Prompt building + Groq LLM
│   ├── user_data/          # WHOOP CSV + manual input parsers
│   ├── evaluation/         # Ragas evaluation harness
│   └── utils/              # Config, logging, helpers
├── frontend/               # React + Vite + Tailwind SPA
│   └── src/
│       ├── pages/          # Dashboard, Ask, Profile, WHOOP, History
│       └── components/     # Sidebar, Topbar
├── notebooks/              # Setup + pipeline test scripts
├── data/                   # Research PDFs + processed data (gitignored)
├── config.yaml             # Model + chunking configuration
└── requirements.txt
```

> Note: `backend/` (auth, db, MCP clients) and `ui/` (Streamlit) are scaffolding for planned features and are not part of the active runtime path. The live app is `api/` (backend) + `frontend/` (UI).

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Tesseract](https://github.com/tesseract-ocr/tesseract) and [Poppler](https://poppler.freedesktop.org/) (`brew install tesseract poppler` on macOS)
- A [Groq API key](https://console.groq.com) (free) and a [HuggingFace token](https://huggingface.co/settings/tokens) (free)

### 1. Clone and set up the backend

```bash
git clone https://github.com/Sandilya0/FitRAG.git
cd FitRAG

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add environment variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here
```

### 3. Build the knowledge base

Place research PDFs in `data/raw/papers/`, then run the ingestion pipeline:

```bash
python notebooks/test_ingestion.py
```

This parses, chunks, embeds, and stores everything in ChromaDB.

### 4. Run the backend

```bash
uvicorn api.main:app --reload --port 8000
```

API docs available at `http://127.0.0.1:8000/docs`.

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/ask` | Ask a question with an optional user profile |
| `POST` | `/api/ask/manual` | Ask using structured manual form input |
| `POST` | `/api/upload/whoop` | Upload a WHOOP CSV export, returns parsed metrics |
| `POST` | `/api/upload/pdf` | Add a new research paper to the corpus |
| `GET`  | `/health` | Health check |

**Example:**

```bash
curl -X POST http://127.0.0.1:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Why is my recovery low after drinking alcohol?",
       "user_profile": {"sleep_quality": "poor", "alcohol": true}}'
```

---

## How It Works

1. **Ingestion** — Research PDFs are parsed (text + images), split into overlapping chunks, embedded with a sentence-transformer model, and stored in ChromaDB with source metadata.
2. **Retrieval** — A user question is embedded and matched against the corpus by cosine similarity to pull the most relevant research chunks.
3. **Personalization** — The user's profile (manual or WHOOP-derived) is formatted into the prompt alongside the retrieved research.
4. **Generation** — Groq's LLaMA 3.3 70B produces a conversational, cited answer constrained to the retrieved context.

---

## Roadmap

- [ ] Conversational adaptive intake (diagnose → prescribe) for device-free users
- [ ] Personal recovery prediction from multi-day WHOOP trends
- [ ] Ragas-based evaluation dashboard (faithfulness, relevancy)
- [ ] Deployment (Railway / Render) with a public demo URL
- [ ] MCP integrations (Google Drive ingestion, email summaries)

---

## Disclaimer

FitRAG provides directional, research-informed guidance for educational purposes. It is not a medical device and does not provide medical advice. Consult a qualified professional for health decisions.

---

## License

MIT
