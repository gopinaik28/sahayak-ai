# 🤖 Real AI Integration Guide

## Overview

Your Next.js website now uses **real CrewAI agents** powered by Ollama instead of mock data!

## Architecture

```
User Browser (localhost:3000)
       ↓
Next.js Frontend
       ↓
FastAPI Backend (localhost:8000)
       ↓
CrewAI Agents
       ↓
Ollama LLM (localhost:11434)
       ↓
Insurance Data (JSON)
```

## Files Created

- **`backend_api.py`** - FastAPI server with CrewAI integration
- **`start_website.sh`** - Script to start all services
- **Updated `website/app/api/recommend/route.ts`** - Calls FastAPI instead of mock data

## 🚀 How to Run

### Option 1: Automatic (Recommended)

```bash
cd "/Users/gopi/Downloads/health insurance"
./start_website.sh
```

This starts all 3 services:
1. Ollama (if not running)
2. FastAPI backend (port 8000)
3. Next.js website (port 3000)

### Option 2: Manual (More Control)

**Terminal 1: Start Ollama**
```bash
ollama serve
```

**Terminal 2: Start FastAPI Backend**
```bash
cd "/Users/gopi/Downloads/health insurance"
source venv/bin/activate
python backend_api.py
```

**Terminal 3: Start Next.js Website**
```bash
cd "/Users/gopi/Downloads/health insurance/website"
npm run dev
```

## 🧪 Testing

1. Open http://localhost:3000
2. Click "Get Started" or "Get Recommendations"
3. Fill the form with your details
4. Click "Get Recommendations"
5. **Wait 20-30 seconds** (CrewAI agents are thinking!)
6. See real AI recommendations!

## API Endpoints

### FastAPI Backend (Port 8000)

- **GET** `/` - API info
- **GET** `/health` - Health check
- **POST** `/recommend` - Get recommendations

**Example Request:**
```json
{
  "age": "28",
  "ped": "Hypertension",
  "budget": "15000-20000",
  "needs": "No room rent limit",
  "preferences": "Good CSR"
}
```

**Example Response:**
```json
{
  "success": true,
  "recommendations": "🎯 **Your Top 3 Recommended...[AI Output]"
}
```

## 🔍 How It Works

1. **User fills form** on website
2. **Next.js sends POST** to `/api/recommend`
3. **Next.js calls FastAPI** at `http://localhost:8000/recommend`
4. **FastAPI creates 3 CrewAI agents:**
   - User Profiler (analyzes needs)
   - Plan Matcher (ranks plans)
   - Comparison Specialist (creates table)
5. **Agents use Ollama** (llama3.2) to analyze
6. **FastAPI returns** AI recommendations
7. **Website displays** real results

## ⚙️ Configuration

### Change Ollama Model

Edit `backend_api.py`:
```python
os.environ["OPENAI_MODEL_NAME"] = "llama3.2"  # Change to llama3.3, etc.
```

### Change Port

**FastAPI:**
Edit `backend_api.py` line 181:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port
```

Then update `website/.env.local`:
```
FASTAPI_URL=http://localhost:YOUR_PORT
```

## 🐛 Troubleshooting

### "Backend API Unavailable" Error

**Symptoms:** Website shows fallback message

**Fixes:**
1. Check FastAPI is running: `curl http://localhost:8000/health`
2. Check Ollama is running: `curl http://localhost:11434/api/tags`
3. Check logs in terminal running `backend_api.py`

### Slow Response (30+ seconds)

**This is normal!** CrewAI runs 3 AI agents sequentially:
- Agent 1: Profiles user (5-10s)
- Agent 2: Analyzes plans (10-15s)
- Agent 3: Creates comparison (5-10s)

**Total: 20-35 seconds**

### CORS Errors

FastAPI is configured to allow:
- `http://localhost:3000`
- `http://localhost:3001`

If using different port, edit `backend_api.py` line 18:
```python
allow_origins=["http://localhost:YOUR_PORT"],
```

## 📊 Monitoring

### Watch FastAPI Logs
```bash
# Terminal running backend_api.py will show:
INFO:     POST /recommend - User request received
INFO:     CrewAI processing...
INFO:     Recommendation generated in 28.3s
```

### Test FastAPI Directly
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "age": "25",
    "ped": "None",
    "budget": "10000-15000",
    "needs": "Maternity coverage",
    "preferences": "HDFC ERGO"
  }'
```

## 🎉 What's Different Now

### Before (Mock Data)
- ✅ Fast response (< 1s)
- ❌ Static recommendations
- ❌ Doesn't analyze user needs
- ❌ Same result for everyone

### After (Real AI)
- ✅ **Personalized** for each user
- ✅ **Analyzes** real insurance data
- ✅ **3 AI agents** working together
- ❌ Slower (20-30s per request)

## 🚦 Production Deployment

For production, you'll need:
1. Host FastAPI on cloud (Render, Railway, AWS)
2. Update `FASTAPI_URL` env variable
3. Deploy Next.js to Vercel
4. Ensure Ollama is accessible (or use cloud LLM)

---

**Built with ❤️ using FastAPI, CrewAI, Next.js, and Ollama**
