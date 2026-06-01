from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import query, upload

app = FastAPI(
    title="FitRAG API",
    description="AI-powered fitness recovery assistant backed by peer-reviewed research",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# Routes
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": "FitRAG",
        "version": "1.0.0"
    }