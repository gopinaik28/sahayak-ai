#!/bin/bash

# Health Insurance Website with Real AI - Startup Script

echo "🚀 Starting Health Insurance Website with Real AI Integration"
echo "============================================================="
echo ""

# Root directory
cd "/Users/gopi/Downloads/health insurance"

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "⚠️  WARNING: Ollama is not running!"
    echo "   Please start Ollama in another terminal:"
    echo "   ollama serve"
    echo ""
    read -p "Press Enter when Ollama is running..."
fi

echo "✅ Ollama is running"
echo ""

# Start FastAPI backend in background
echo "🐍 Starting FastAPI backend on port 8000..."
cd backend
python backend_api.py &
FASTAPI_PID=$!
cd ..

# Wait for FastAPI to start
sleep 3

# Check if FastAPI started
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ FastAPI backend is running (PID: $FASTAPI_PID)"
else
    echo "❌ FastAPI backend failed to start"
    kill $FASTAPI_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🌐 Starting Next.js website on port 3000..."
cd frontend
npm run dev &
NEXTJS_PID=$!
cd ..

echo ""
echo "============================================================="
echo "✅ ALL SERVICES RUNNING!"
echo "============================================================="
echo ""
echo "📱 Website: http://localhost:3000"
echo "🔧 FastAPI: http://localhost:8000"
echo "🤖 Ollama:  http://localhost:11434"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping services...'; kill $FASTAPI_PID $NEXTJS_PID 2>/dev/null; exit 0" INT

# Keep script running
wait
