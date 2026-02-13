# 📁 Project Structure Overview

## Final Organized Structure

```
health-insurance/
│
├── 📂 backend/                     # FastAPI Backend
│   ├── backend_api.py             # Main API server with CrewAI
│   ├── data/                      # Insurance JSON data
│   │   └── indian_health_insurance_data.json
│   └── requirements.txt           # Python dependencies
│
├── 📂 frontend/                    # Next.js Website
│   ├── app/                       # Next.js 14 app router
│   │   ├── api/recommend/         # API route
│   │   ├── recommend/             # Recommendation page
│   │   ├── page.tsx               # Home page
│   │   └── layout.tsx             # Layout
│   ├── components/                # React components
│   │   ├── Hero.tsx
│   │   ├── Features.tsx
│   │   └── ui/                    # shadcn components
│   ├── public/                    # Static files
│   ├── package.json               # Node dependencies
│   └── README.md                  # Frontend docs
│
├── 📂 notebooks/                   # Jupyter Notebooks
│   └── health_insurance_recommender.ipynb
│
├── 📂 scripts/                     # Python Scripts
│   ├── app.py                     # Streamlit app
│   └── health_insurance_recommender.py
│
├── 📂 data/                        # Shared data files
│   └── indian_health_insurance_data.json
│
├── 📂 venv/                        # Python virtual environment
│
├── 📄 README.md                    # Main documentation
├── 📄 AI_INTEGRATION_GUIDE.md      # API integration guide
├── 📄 STREAMLIT_GUIDE.md           # Streamlit usage guide
├── 📄 start_website.sh             # Startup script
└── 📄 requirements.txt             # Root Python deps

```

## How to Run Each Component

### 1️⃣ Backend (FastAPI)
```bash
cd backend
source ../venv/bin/activate
python backend_api.py
# → http://localhost:8000
```

### 2️⃣ Frontend (Next.js)
```bash
cd frontend
npm run dev
# → http://localhost:3000
```

### 3️⃣ Streamlit App
```bash
cd scripts
source ../venv/bin/activate
streamlit run app.py
```

### 4️⃣ Jupyter Notebook
```bash
jupyter notebook notebooks/health_insurance_recommender.ipynb
```

### 🚀 Quick Start (All at once)
```bash
./start_website.sh
```

## File Purposes

| File/Folder | Purpose |
|-------------|---------|
| `backend/backend_api.py` | FastAPI server with 3 CrewAI agents |
| `frontend/` | Professional Next.js website with AI integration |
| `notebooks/` | Interactive Jupyter notebook for testing |
| `scripts/app.py` | Streamlit alternative interface |
| `data/` | JSON files with insurance plan details |
| `venv/` | Python virtual environment |

## Technologies Used

**Backend:**
- FastAPI
- CrewAI (3 AI agents)
- Ollama (llama3.2)
- Python 3.13

**Frontend:**
- Next.js 14
- TypeScript
- Tailwind CSS
- ReactMarkdown
- shadcn/ui

**Tools:**
- Jupyter Notebook
- Streamlit

---

**Clean, organized, and production-ready! 🎉**
