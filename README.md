# 🏥 AI-Powered Health Insurance Recommendation System

An intelligent health insurance recommendation platform powered by **RAG (Retrieval Augmented Generation)**, **CrewAI agents**, and **semantic search** to help users find the perfect health insurance plan in India.

![Tech Stack](https://img.shields.io/badge/Next.js-14-black) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green) ![Ollama](https://img.shields.io/badge/Ollama-llama3.2-blue) ![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-orange)

---

## ✨ Features

- 🤖 **AI-Powered Recommendations** - 3 specialized AI agents analyze user needs
- 🔍 **Semantic Search** - RAG with Ollama embeddings for intelligent plan matching
- 💬 **Natural Language** - Describe your needs in plain language
- 📊 **Smart Comparison** - Side-by-side plan comparison with AI reasoning
- 🎯 **Personalized** - Recommendations based on age, conditions, budget, and preferences
- ⚡ **Real-time** - Powered by local LLM (Ollama llama3.2)

---

## 🏗️ Architecture

```
User Input → Semantic Search (RAG) → Top 5 Relevant Plans → CrewAI Agents → Recommendations
```

**Tech Stack:**
- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS
- **Backend:** FastAPI + CrewAI + Ollama
- **RAG:** ChromaDB + Ollama Embeddings (nomic-embed-text)
- **LLM:** Ollama (llama3.2) - runs locally
- **Data:** 9 curated Indian health insurance plans

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- [Ollama](https://ollama.ai/) installed

### 1. Install Ollama Models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup RAG vector database (one-time)
cd rag
python setup_embeddings.py
cd ..
```

### 3. Setup Frontend

```bash
cd frontend
npm install
```

### 4. Run the Application

**Option A: Use the startup script (recommended)**
```bash
./start_website.sh
```

**Option B: Manual start**
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python backend_api.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 5. Open in Browser

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
health-insurance-ai/
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── start_website.sh         # Quick start script
│
├── backend/                 # FastAPI backend
│   ├── backend_api.py      # Main API server
│   ├── requirements.txt    # Python dependencies
│   ├── data/               # Insurance data JSON
│   └── rag/                # RAG infrastructure
│       ├── rag_engine.py   # Semantic search engine
│       ├── setup_embeddings.py  # Vector DB setup
│       ├── chroma_db/      # Vector database (gitignored)
│       └── README.md       # RAG documentation
│
├── frontend/               # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   └── package.json       # Node dependencies
│
├── notebooks/             # Jupyter notebooks
│
└── docs/                  # Documentation
    ├── ARCHITECTURE_EXPLANATION.md
    ├── PRODUCTION_ANTI_HALLUCINATION.md
    ├── PROJECT_STRUCTURE.md
    └── RAG_GUIDE.md
```

---

## 🤖 How It Works

### 1. **User Input**
User provides: age, pre-existing conditions, budget, specific needs, preferences

### 2. **Semantic Search (RAG)**
- User profile converted to embedding
- ChromaDB finds top 5 most relevant plans
- Cosine similarity matching

### 3. **AI Agents Analysis**
Three specialized CrewAI agents:
- **User Profiler:** Analyzes requirements
- **Plan Matcher:** Recommends top 3 plans
- **Comparison Specialist:** Creates comparison table

### 4. **Results**
- Top 3 personalized recommendations
- Detailed feature comparison
- AI reasoning for each suggestion

---

## 📊 Insurance Coverage

Currently includes **9 premium health insurance plans** from top insurers:

- **Star Health:** Comprehensive, Super Star, Health Assure
- **HDFC ERGO:** Optima Secure
- **ICICI Lombard:** Complete Health, Elevate
- **Niva Bupa:** ReAssure 2.0/3.0
- **Care Health:** Care Supreme
- **Aditya Birla:** Activ Health Platinum

---

## 🔧 Technology Deep Dive

### RAG (Retrieval Augmented Generation)

Instead of passing all insurance data to the LLM, we use semantic search:

1. **Embedding Creation:** Each plan converted to 768-dim vector
2. **Vector Storage:** ChromaDB stores embeddings persistently
3. **Semantic Query:** User needs converted to embedding
4. **Similarity Search:** Find closest matching plans
5. **Context Injection:** Only relevant plans sent to LLM

**Benefits:**
- ✅ More accurate recommendations
- ✅ Faster processing
- ✅ Scalable to 100s of plans
- ✅ Intelligent semantic understanding

### Anti-Hallucination

Strict prompts prevent AI from making up information:
- Use ONLY exact data from vector store
- Copy values precisely (sum insured, CSR, etc.)
- Never guess missing information
- Verify all numbers against source data

See `docs/PRODUCTION_ANTI_HALLUCINATION.md` for details.

---

## 📚 Documentation

- [RAG Guide](docs/RAG_GUIDE.md) - Complete RAG implementation details
- [Architecture](docs/ARCHITECTURE_EXPLANATION.md) - System design
- [Anti-Hallucination](docs/PRODUCTION_ANTI_HALLUCINATION.md) - Accuracy measures
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Directory overview

---

## 🛠️ Development

### Adding New Insurance Plans

1. Edit `backend/data/indian_health_insurance_data.json`
2. Run RAG setup: `cd backend/rag && python setup_embeddings.py`
3. Restart backend

### Modifying AI Prompts

Edit task descriptions in `backend/backend_api.py` (lines 86-165)

### Frontend Customization

- Edit forms: `frontend/app/recommend/page.tsx`
- Modify styles: Tailwind classes
- Add components: `frontend/components/`

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Add more insurance plans
- Improve semantic search accuracy
- Add user feedback loop
- Implement plan filtering
- Add premium calculation API

---

## 📝 License

MIT License - feel free to use for your projects!

---

## 🙏 Acknowledgments

- **Ollama** - Local LLM infrastructure
- **CrewAI** - Multi-agent framework
- **ChromaDB** - Vector database
- **Next.js** - React framework
- **shadcn/ui** - UI components

---

## 📧 Contact

Questions? Found a bug? Open an issue!

---

**Built with ❤️ using AI and modern web technologies**

Star ⭐ this repo if you found it helpful!
