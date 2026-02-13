from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
import json
import os
import warnings
from rag.rag_engine import RAGEngine

warnings.filterwarnings('ignore')

# Configure Ollama
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3.2"
os.environ["OPENAI_API_KEY"] = "ollama"

app = FastAPI(title="Health Insurance Recommendation API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine
print("🚀 Initializing RAG Engine...")
rag_engine = RAGEngine()
print("✅ RAG Engine ready!")

# Load valid insurer names for validation
with open('data/indian_health_insurance_data.json', 'r') as f:
    insurance_data = json.load(f)

VALID_INSURERS = {
    "Star Health and Allied Insurance Co. Ltd.",
    "HDFC ERGO General Insurance Company Ltd.",
    "ICICI Lombard General Insurance Co. Ltd.",
    "Niva Bupa Health Insurance Co. Ltd.",
    "Care Health Insurance Ltd.",
    "Aditya Birla Health Insurance Co. Ltd."
}

print(f"✅ Loaded {len(VALID_INSURERS)} valid insurers:")
for insurer in VALID_INSURERS:
    print(f"   - {insurer}")

# Create CrewAI agents
user_profiler = Agent(
    role='Health Insurance Needs Analyst',
    goal='Understand user health insurance requirements',
    backstory='Expert at analyzing customer needs for health insurance',
    verbose=False,
    allow_delegation=False
)

recommendation_agent = Agent(
    role='Insurance Plan Matcher',
    goal='Match users with best insurance plans from the provided data',
    backstory='Specialist in comparing insurance plans and finding perfect matches. ONLY uses the exact data provided, never makes up information.',
    verbose=False,
    allow_delegation=False
)

comparison_agent = Agent(
    role='Plan Comparison Specialist',
    goal='Create clear comparison tables using exact data from recommendations',
    backstory='Expert at creating accurate comparison tables. Copies data exactly as provided, never invents information.',
    verbose=False,
    allow_delegation=False
)

# Request/Response models
class RecommendationRequest(BaseModel):
    age: str
    ped: str
    budget: str
    needs: str
    preferences: str

class RecommendationResponse(BaseModel):
    recommendations: str

# Endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "ollama": "connected"}

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    try:
        # Create user profile task
        profile_task = Task(
            description=f"""Analyze this user profile:
            - Age: {request.age} years old
            - Pre-existing Conditions: {request.ped}
            - Annual Budget: ₹{request.budget}
            - Specific Needs: {request.needs}
            - Preferences: {request.preferences}
            
            **CRITICAL: Do NOT make up any information. Only use the data provided.**
            
            Summarize their top 3 requirements in 1-2 lines.""",
            agent=user_profiler,
            expected_output="Brief user requirements summary"
        )
        
        # Use RAG to get relevant plans
        user_profile = {
            'age': request.age,
            'ped': request.ped,
            'budget': request.budget,
            'needs': request.needs,
            'preferences': request.preferences
        }
        
        # Get ONLY top 3 most relevant plans
        relevant_context = rag_engine.get_relevant_context(user_profile, top_k=3)
        
        # Log what RAG is sending
        print("\n" + "="*80)
        print("RAG CONTEXT BEING SENT TO LLM:")
        print("="*80)
        print(relevant_context[:500] + "...")
        print("="*80 + "\n")
        
        recommend_task = Task(
            description=f"""⚠️ STRICT RULES - YOU MUST FOLLOW EXACTLY:

{relevant_context}

**THE 3 PLANS ABOVE ARE THE ONLY PLANS THAT EXIST. DO NOT USE ANY OTHER PLAN NAMES!**

FORBIDDEN COMPANIES (DO NOT MENTION):
- Future Generali
- Bajaj Allianz  
- Reliance
- Tata AIG
- Max Life
- Any company NOT in the data above

REQUIRED ACTIONS:
1. **USE ONLY THE 3 PLANS ABOVE** - No other plan names exist!
2. **COPY PLAN NAMES EXACTLY** - Character-by-character from data above
3. **COPY INSURER NAMES EXACTLY** - From the data above only
4. **COPY ALL VALUES EXACTLY** - Sum insured, CSR, room rent from data above
5. **IF NOT IN DATA ABOVE, DON'T SAY IT**

For each of THE 3 PLANS PROVIDED ABOVE, write:

## [EXACT PLAN NAME FROM DATA ABOVE]
**Insurer:** [EXACT INSURER NAME FROM DATA ABOVE]
**Premium:** ₹10,000 - ₹25,000 per year (typical range)
**Sum Insured:** [COPY EXACT TEXT FROM DATA ABOVE]

**Why This Plan:**
- [Match to user needs]
- [Coverage highlights]
- [Value proposition]

**Key Features:**
- Room rent: [EXACT from data above]
- Maternity: [EXACT from data above or "Not specified"]
- CSR: [EXACT from data above]
- NCB: [EXACT from data above]""",
            agent=recommendation_agent,
            expected_output="Top 3 plans using ONLY the provided data",
            context=[profile_task]
        )
        
        compare_task = Task(
            description="""Create comparison table using ONLY the 3 plans from recommendations above.

⛔ FORBIDDEN:
- Adding companies not in recommendations
- Making up plan names
- Empty columns

REQUIRED:
- Use EXACT plan names as column headers
- Copy all values from recommendations
- All 3 columns must have data

| Feature | [Plan 1 EXACT NAME] | [Plan 2 EXACT NAME] | [Plan 3 EXACT NAME] |
|---------|---------------------|---------------------|---------------------|
| Insurer | [EXACT name] | [EXACT name] | [EXACT name] |
| Annual Premium | ₹XX,000 - ₹XX,000 | ₹XX,000 - ₹XX,000 | ₹XX,000 - ₹XX,000 |
| Sum Insured | [EXACT from data] | [EXACT from data] | [EXACT from data] |
| Room Rent Limit | [EXACT from data] | [EXACT from data] | [EXACT from data] |
| Maternity | [EXACT from data] | [EXACT from data] | [EXACT from data] |
| NCB | [EXACT from data] | [EXACT from data] | [EXACT from data] |
| CSR | [EXACT from data] | [EXACT from data] | [EXACT from data] |

Then add:
## Our Recommendation
We recommend **[Plan Name]** because [reasons based on user needs].""",
            agent=comparison_agent,
            expected_output="Comparison table with exact data",
            context=[profile_task, recommend_task]
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[user_profiler, recommendation_agent, comparison_agent],
            tasks=[profile_task, recommend_task, compare_task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        result_text = str(result)
        
        # Validate response for hallucinations
        print("\n" + "="*80)
        print("VALIDATING AI RESPONSE...")
        print("="*80)
        
        # Check for forbidden companies
        forbidden_companies = ["future generali", "bajaj allianz", "reliance", "tata aig", "max life", "icici direct"]
        result_lower = result_text.lower()
        
        hallucinations_found = []
        for forbidden in forbidden_companies:
            if forbidden in result_lower:
                hallucinations_found.append(f"❌ Found '{forbidden}'")
        
        if hallucinations_found:
            print("\n🚨 HALLUCINATIONS DETECTED:")
            for h in hallucinations_found:
                print(f"  {h}")
            print("\n⚠️ WARNING: Response contains hallucinated companies not in database!")
            print("="*80 + "\n")
        else:
            print("✅ No hallucinations detected")
            print("="*80 + "\n")
        
        return RecommendationResponse(recommendations=result_text)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
