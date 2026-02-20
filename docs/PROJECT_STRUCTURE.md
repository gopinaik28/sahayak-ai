# 📁 Project Structure

```
health-insurance/
│
├── backend/                          # FastAPI Backend
│   ├── backend_api.py               # Main API server with CrewAI agents
│   ├── requirements.txt             # Python dependencies
│   ├── data/
│   │   └── indian_health_insurance_data.json
│   └── rag/                         # RAG Infrastructure
│       ├── rag_engine.py            # Semantic search engine
│       ├── setup_embeddings.py      # One-time vector DB setup
│       ├── chroma_db/               # Persistent vector database (gitignored)
│       └── README.md
│
├── frontend/                         # Next.js 14 Website
│   ├── app/
│   │   ├── page.tsx                 # Home page
│   │   ├── layout.tsx               # Root layout
│   │   ├── globals.css              # Global styles
│   │   ├── api/recommend/route.ts   # API proxy route
│   │   └── recommend/page.tsx       # Recommendation page
│   ├── components/
│   │   ├── Hero.tsx                 # Hero section
│   │   └── ui/                      # shadcn/ui components
│   ├── lib/utils.ts
│   ├── public/favicon.ico
│   └── package.json
│
├── notebooks/
│   └── health_insurance_recommender.ipynb
│
├── docs/                             # Documentation
│   ├── ARCHITECTURE_EXPLANATION.md
│   ├── PRODUCTION_ANTI_HALLUCINATION.md
│   ├── PROJECT_STRUCTURE.md          # This file
│   └── RAG_GUIDE.md
│
├── .gitignore
├── README.md
└── start_website.sh                  # Quick-start script
```

## How to Run

### 🚀 Quick Start
```bash
./start_website.sh
```

### Manual Start
```bash
# Terminal 1 — Backend
cd backend
source ../venv/bin/activate
python backend_api.py
# → http://localhost:8000

# Terminal 2 — Frontend
cd frontend
npm run dev
# → http://localhost:3000
```

## Technologies

| Layer | Stack |
|-------|-------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui |
| Backend | FastAPI, CrewAI, Ollama (llama3.2) |
| RAG | ChromaDB, Ollama Embeddings (nomic-embed-text) |
