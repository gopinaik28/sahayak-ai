import { NextRequest, NextResponse } from "next/server";

const FASTAPI_URL = process.env.FASTAPI_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { age, ped, budget, needs, preferences } = body;

        // Call FastAPI backend with real CrewAI integration
        const response = await fetch(`${FASTAPI_URL}/recommend`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                age,
                ped,
                budget,
                needs,
                preferences,
            }),
        });

        if (!response.ok) {
            throw new Error(`Backend API error: ${response.statusText}`);
        }

        const data = await response.json();

        return NextResponse.json({
            success: true,
            recommendations: data.recommendations,
        });
    } catch (error) {
        console.error("API Error:", error);

        // Fallback to mock data if backend is unavailable
        const mockRecommendations = `
⚠️ **Backend API Unavailable - Showing Sample Data**

Please ensure:
1. FastAPI backend is running: \`python backend_api.py\`
2. Ollama is running: \`ollama serve\`

---

🎯 **Sample Recommendations**

Based on typical needs for your profile, here are common recommendations:

🥇 **Star Comprehensive Insurance Policy**
- Comprehensive coverage with maternity benefits
- 50% NCB per claim-free year
- Premium: ₹15,000-18,000/year

🥈 **HDFC ERGO Optima Secure**  
- Excellent CSR of 98.85%
- Higher sum insured options
- Premium: ₹18,000-22,000/year

🥉 **Star Health Assure**
- Budget-friendly option
- Lifelong renewability
- Premium: ₹12,000-15,000/year

---

💡 **To get real AI recommendations:**
\`\`\`bash
# Terminal 1: Start FastAPI backend
cd "/Users/gopi/Downloads/health insurance"
source venv/bin/activate
python backend_api.py

# Terminal 2: Start Next.js (already running)
cd website && npm run dev
\`\`\`
`;

        return NextResponse.json({
            success: false,
            recommendations: mockRecommendations,
            error: error instanceof Error ? error.message : "Unknown error",
        });
    }
}
