# RAG Engine

Semantic search infrastructure using **Ollama embeddings** + **ChromaDB** vector database.

## 🎯 Purpose

Implements Retrieval Augmented Generation (RAG) for intelligent insurance plan recommendations:
- Converts insurance plans to embeddings
- Stores in vector database
- Performs semantic similarity search
- Returns most relevant plans for user queries

## 📦 Components

### `rag_engine.py`
Core RAG functionality:
- `RAGEngine` class
- Embedding generation using Ollama
- ChromaDB vector storage
- Semantic search methods

### `setup_embeddings.py`
One-time setup script to:
1. Load insurance data
2. Create embeddings
3. Store in ChromaDB

### `chroma_db/`
Persistent vector database storage (gitignored)

## 🚀 Setup

**First time only:**

```bash
cd backend/rag
python setup_embeddings.py
```

This creates embeddings for all 9 insurance plans.

## 📚 Usage

The RAG engine is automatically initialized in `backend_api.py`:

```python
from rag.rag_engine import RAGEngine

rag_engine = RAGEngine()
relevant_plans = rag_engine.get_relevant_context(user_profile, top_k=5)
```

## 🔧 Technical Details

- **Embedding Model:** `nomic-embed-text` (768 dimensions)
- **Vector DB:** ChromaDB with cosine similarity
- **Storage:** Persistent SQLite + metadata
- **Search:** Top-K semantic similarity

## 📖 Documentation

See `docs/RAG_GUIDE.md` for comprehensive RAG implementation details.
