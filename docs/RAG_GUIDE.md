# RAG Implementation Guide

## 🎯 What Changed?

We upgraded from **simple context injection** to **RAG (Retrieval Augmented Generation)** with semantic search!

### Before: Simple Approach
```python
# Loaded ALL 9 plans into memory
# Passed ALL plans to LLM (2500 characters)
# LLM read everything and recommended
```

### After: RAG with Embeddings
```python
# Created embeddings for all 9 plans using Ollama
# Stored in ChromaDB vector database
# Semantic search finds MOST RELEVANT 5 plans
# LLM only sees relevant plans
```

---

## 🏗️ Architecture

```
User Request
    ↓
Create semantic query from user profile
(age, conditions, budget, needs)
    ↓
Generate query embedding (Ollama)
    ↓
Semantic search in ChromaDB
(Find 5 most similar plans)
    ↓
Pass ONLY relevant plans to CrewAI
    ↓
AI agents analyze & recommend
    ↓
Return top 3 recommendations
```

---

## 📦 Components

### 1. RAG Engine (`backend/rag_engine.py`)

**Key Functions:**
- `chunk_insurance_data()` - Split plans into chunks
- `generate_embedding(text)` - Create embeddings using Ollama
- `setup_vector_database()` - One-time setup
- `semantic_search(query, top_k)` - Find similar plans
- `get_relevant_context(user_profile)` - Get context for user

**Embedding Model:**
- Model: `nomic-embed-text` (274MB)
- Dimensions: 768
- Similarity: Cosine similarity

### 2. Vector Database (ChromaDB)

**Location:** `backend/chroma_db/`
**Storage:** Persistent (survives restarts)
**Collection:** `insurance_plans`
**Documents:** 9 insurance plan chunks

### 3. Updated Backend API

**Changes:**
- Imports `RAGEngine`
- Initializes on startup
- Uses `rag_engine.get_relevant_context()` instead of full data
- Passes only top 5 relevant plans to CrewAI

---

##  How to Use

### One-Time Setup (Already Done!)

```bash
cd backend

# 1. Install dependencies
pip install chromadb langchain langchain-community ollama

# 2. Pull embedding model
ollama pull nomic-embed-text

# 3. Create vector database
python setup_embeddings.py
```

### Running the Server

```bash
cd backend
source ../venv/bin/activate
python backend_api.py
```

**Output:**
```
🚀 Initializing RAG Engine...
✅ Loaded existing vector database
✅ RAG Engine ready!
INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## 🧪 Testing Semantic Search

### Test from Python

```python
from rag_engine import RAGEngine

rag = RAGEngine()

# Test query
query = "I need maternity coverage with good claim settlement"
results = rag.semantic_search(query, top_k=3)

for result in results:
    print(f"{result['metadata']['plan_name']}")
    print(f"  Similarity: {result['similarity']:.2%}")
```

### Expected Behavior

**Query:** "I have diabetes, need low waiting period"
**Results:**
1. Plans with low PED waiting (24 months or less)
2. Good CSR for reliable claims
3. Comprehensive coverage

**Query:** "Budget under 15000, maternity coverage"
**Results:**
1. Care Supreme (budget-friendly + maternity)
2. Star Comprehensive (maternity available)
3. HDFC ERGO Optima (maternity optional)

---

## 🔍 How Semantic Search Works

### Example

**User Input:**
```json
{
  "age": "28",
  "ped": "None",
  "budget": "15000-20000",
  "needs": "Maternity coverage",
  "preferences": "Good claim settlement ratio"
}
```

**Semantic Query Created:**
```
User Profile:
- Age: 28 years
- Pre-existing Conditions: None
- Budget: ₹15000-20000 per year
- Specific Needs: Maternity coverage
- Preferences: Good claim settlement ratio

Find insurance plans that match these requirements.
```

**Embedding Generated:**
```python
[0.023, -0.041, 0.089, ...] # 768 dimensions
```

**Similarity Search:**
```
Plan: Star Comprehensive → 65.88% match
Plan: Super Star → 63.61% match
Plan: HDFC ERGO Optima → 61.23% match
Plan: Care Supreme → 58.45% match
Plan: ICICI Complete → 55.12% match
```

**Top 5 Passed to LLM:**
Only these 5 plans (not all 9!)

---

## 📊 Benefits

### ✅ Advantages

1. **More Accurate**
   - Semantic understanding of user needs
   - Better matching than keyword search

2. **Scalable**
   - Can handle 100s or 1000s of plans
   - Context window not a limitation

3. **Intelligent**
   - Understands "maternity" relates to pregnancy, babies, delivery
   - Understands "diabetes" relates to PED waiting periods

4. **Efficient**
   - LLM sees only relevant 5 plans
   - Faster processing
   - Lower token usage

### 📈 Performance

- **Setup Time:** ~30 seconds (one-time)
- **Query Time:** ~200ms for semantic search
- **Total Request:** ~25-30 seconds (same as before)

---

## 🔧 Troubleshooting

### Issue: "Vector database not initialized"

**Solution:**
```bash
cd backend
python setup_embeddings.py
```

### Issue: "Ollama model not found"

**Solution:**
```bash
ollama pull nomic-embed-text
```

### Issue: "ChromaDB errors"

**Solution:**
```bash
# Delete and recreate
rm -rf backend/chroma_db
cd backend
python setup_embeddings.py
```

---

## 📁 File Structure

```
backend/
├── backend_api.py           # Updated with RAG
├── rag_engine.py           # RAG logic
├── setup_embeddings.py     # Setup script
├── requirements.txt        # Updated deps
├── data/
│   └── indian_health_insurance_data.json
└── chroma_db/              # Vector database
    ├── chroma.sqlite3
    └── [embeddings]
```

---

## 🚀 Next Steps

**Future Enhancements:**

1. **Better Chunking:** Split each plan into features
2. **More Metadata:** Add price ranges, age groups
3. **Hybrid Search:** Combine semantic + keyword
4. **Re-ranking:** Re-rank results based on exact budget match
5. **Feedback Loop:** Learn from user selections

---

## 🎓 Technical Details

### Embedding Model: nomic-embed-text

- **Developer:** Nomic AI
- **Size:** 274MB
- **Dimensions:** 768
- **Context Length:** 8192 tokens
- **Use Case:** Semantic text search
- **License:** Apache 2.0

### Vector Database: ChromaDB

- **Type:** Embedded vector database
- **Storage:** SQLite + HDF5
- **Similarity:** Cosine similarity (default)
- **Index:** HNSW (Hierarchical Navigable Small World)
- **Scalability:** Millions of vectors

---

**Your AI project now has production-grade RAG capabilities!** 🎉
