# 🤖 How Our Recommendation System Works

## **Current Approach: Direct Context Injection (No RAG)**

### What We're Doing ✅

**Simple Answer:** We are **NOT** using:
- ❌ Vector databases (Chroma, Pinecone, FAISS, etc.)
- ❌ Embeddings (OpenAI embeddings, sentence transformers, etc.)
- ❌ Chunking strategies
- ❌ Similarity search
- ❌ RAG (Retrieval Augmented Generation)

**What We ARE Using:**
- ✅ Direct context injection into LLM prompts
- ✅ Full JSON data loaded into memory
- ✅ CrewAI agents with reasoning capabilities
- ✅ Ollama (llama3.2) for text generation

---

## 📊 Current Architecture

```
User Input (age, conditions, budget, needs)
        ↓
FastAPI Backend
        ↓
Load insurance_data.json (9 plans)
        ↓
Create text context string (~2500 chars)
        ↓
Pass entire context to CrewAI agents' prompts
        ↓
LLM reads ALL data + user profile
        ↓
LLM uses reasoning to recommend top 3 plans
        ↓
Return recommendations
```

### How It Works (Line by Line)

**1. Load Data into Memory:**
```python
# Line 28-29: Load JSON file
with open('data/indian_health_insurance_data.json', 'r') as f:
    insurance_data = json.load(f)
```

**2. Create Text Context:**
```python
# Lines 32-54: Convert JSON to text format
def create_insurance_context():
    context = "AVAILABLE HEALTH INSURANCE PLANS:\n\n"
    # Loop through all 9 plans
    for insurer in insurers:
        for plan in insurer['plans']:
            context += f"Plan Name: {plan['plan_name']}\n"
            context += f"Premium: ...\n"
            # ... all plan details
    return context
```

**3. Pass to LLM via Prompt:**
```python
# Line 124: Inject context directly into prompt
description=f"""From these plans:
{insurance_context[:2500]}  # First 2500 characters

Recommend top 3 for user with:
- Age: {request.age}
- Conditions: {request.ped}
- Budget: {request.budget}
"""
```

**4. LLM Reasoning:**
- The LLM (llama3.2) reads the ENTIRE context
- Uses its internal reasoning to:
  - Understand user needs
  - Compare all 9 plans
  - Rank them based on match
  - Generate recommendations

**No embeddings, no similarity search, just pure LLM reasoning!**

---

## 🤔 Why This Approach?

### ✅ Advantages (for our use case)

1. **Small Dataset:** Only 9 insurance plans
   - Easy to fit in LLM context window (8K+ tokens)
   - No need for retrieval

2. **Simple & Fast:**
   - No chunking overhead
   - No embedding computation
   - No vector database queries
   - Direct prompt = faster response

3. **Reasoning-Based:**
   - LLM can understand nuances
   - Can weigh multiple factors
   - Natural language understanding

4. **Easy to Debug:**
   - Just read the prompt to see what LLM sees
   - No complex retrieval pipeline

### ❌ Limitations

1. **Not Scalable:**
   - Won't work with 1000+ plans
   - Context window has limits (~8K-128K tokens)

2. **No Semantic Search:**
   - Not finding "similar" plans
   - Just reading all and reasoning

3. **Slower with Large Data:**
   - Processing 2500 chars every request
   - No caching of relevant plans

---

## 🔬 Alternative Approach: RAG with Embeddings

If you want to use **vector databases and similarity search**, here's how it would work:

### RAG Architecture

```
1. OFFLINE (One-time setup):
   Load insurance_data.json
         ↓
   Chunk each plan into smaller pieces
   (e.g., "Plan X has maternity coverage...")
         ↓
   Generate embeddings for each chunk
   (using OpenAI embeddings or sentence-transformers)
         ↓
   Store in vector database (Chroma, FAISS, Pinecone)

2. ONLINE (Each request):
   User query: "I need maternity coverage"
         ↓
   Generate embedding for user query
         ↓
   Similarity search in vector DB
   (cosine similarity between query embedding and plan embeddings)
         ↓
   Retrieve top 3-5 most similar plan chunks
         ↓
   Pass ONLY those chunks to LLM
         ↓
   LLM generates recommendations
```

### RAG Code Example

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. OFFLINE: Create embeddings
def setup_vector_db():
    # Load insurance data
    with open('data/insurance.json') as f:
        data = json.load(f)
    
    # Create text chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    documents = []
    for plan in data['plans']:
        text = f"""
        Plan: {plan['name']}
        Insurer: {plan['insurer']}
        Premium: {plan['premium']}
        Coverage: {plan['coverage']}
        Maternity: {plan['maternity']}
        """
        chunks = text_splitter.split_text(text)
        documents.extend(chunks)
    
    # Generate embeddings and store
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(
        texts=documents,
        embedding=embeddings
    )
    return vectorstore

# 2. ONLINE: Query
def recommend_with_rag(user_query, vectorstore):
    # Similarity search
    relevant_chunks = vectorstore.similarity_search(
        user_query,
        k=5  # Top 5 most similar chunks
    )
    
    # Pass to LLM
    context = "\n".join([chunk.page_content for chunk in relevant_chunks])
    prompt = f"""
    Based on these plans:
    {context}
    
    Recommend top 3 for user: {user_query}
    """
    # ... call LLM with prompt
```

---

## 📈 Comparison Table

| Feature | Current (Direct Context) | RAG (Embeddings) |
|---------|-------------------------|------------------|
| **Works for** | Small datasets (<50 items) | Large datasets (1000s of items) |
| **Speed** | Fast (no retrieval) | Slower (embedding + search) |
| **Accuracy** | Good (sees all data) | Good (sees relevant data) |
| **Setup** | Simple | Complex |
| **Dependencies** | Just LLM | LLM + embeddings + vector DB |
| **Scalability** | ❌ Limited by context | ✅ Unlimited |
| **Cost** | Low (LLM only) | Higher (embeddings + storage) |
| **Semantic Search** | ❌ No | ✅ Yes |

---

## 🎯 Recommendation

**For Our Use Case (9 plans):**
- ✅ **Current approach is PERFECT**
- No need for RAG complexity
- All plans fit in context window
- Fast and simple

**When to Use RAG:**
- You have 100+ insurance plans
- Dataset > 100KB of text
- Need semantic search ("find similar plans")
- Context window limitations

---

## 🚀 Want to Add RAG?

If you want to implement RAG with embeddings, I can help you:

1. **Choose embedding model:**
   - OpenAI embeddings (paid, best quality)
   - Sentence-transformers (free, good quality)
   - Ollama embeddings (free, local)

2. **Choose vector database:**
   - Chroma (simple, local)
   - FAISS (fast, local)
   - Pinecone (cloud, scalable)
   - Qdrant (cloud/local, feature-rich)

3. **Integrate with CrewAI:**
   - Add RAG tool to agents
   - Use LangChain integration
   - Custom retrieval logic

Let me know if you want to explore this! 🎓

---

**Summary:** We're using **prompt-based reasoning** (simple, fast) instead of **RAG with embeddings** (complex, scalable). Perfect for 9 plans! ✨
