# Health Insurance Recommendation System - Simple Working Version
# This version doesn't pass llm to agents - uses environment variables instead

import json
import pandas as pd
import os
from crewai import Agent, Task, Crew, Process
import warnings
warnings.filterwarnings('ignore')

# Configure environment for Ollama
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3.2"
os.environ["OPENAI_API_KEY"] = "ollama"  # Dummy key for Ollama

print("✅ Libraries imported and Ollama configured via environment!")

# Load insurance data
with open('data/indian_health_insurance_data.json', 'r') as f:
    insurance_data = json.load(f)

insurers = insurance_data['insurers']
total_plans = sum(len(insurer['plans']) for insurer in insurers)

print(f"✅ Loaded data for {len(insurers)} insurers")
print(f"✅ Total plans available: {total_plans}")
print(f"\nInsurers: {', '.join([i['insurer_name'] for i in insurers])}")

# Define CrewAI Agents (no llm parameter - will use env vars)

user_profiler = Agent(
    role='Health Insurance Needs Analyst',
    goal='Analyze user requirements and create a comprehensive profile of their insurance needs',
    backstory="""You are an expert health insurance analyst who specializes in understanding 
    customer needs. You excel at identifying the most important factors for each customer based 
    on their age, health conditions, budget, and preferences.""",
    verbose=True,
    allow_delegation=False
)

recommendation_agent = Agent(
    role='Insurance Plan Matcher',
    goal='Analyze all available insurance plans and rank the top 5 best matches for the user profile',
    backstory="""You are a highly experienced insurance plan matcher with deep knowledge of 
    Indian health insurance products. You excel at analyzing plan features like waiting periods, 
    coverage limits, claim settlement ratios, and special benefits.""",
    verbose=True,
    allow_delegation=False
)

comparison_agent = Agent(
    role='Insurance Comparison Specialist',
    goal='Create a detailed comparison of recommended plans with clear reasoning for rankings',
    backstory="""You are an insurance comparison expert who excels at breaking down complex 
    insurance features into simple, understandable comparisons. You provide clear reasoning for 
    why certain plans are better suited for specific customer needs.""",
    verbose=True,
    allow_delegation=False
)

print("✅ Created 3 specialized agents")

# User Input Collection
print("=" * 60)
print("HEALTH INSURANCE RECOMMENDATION SYSTEM")
print("=" * 60)
print("\nPlease provide your details for personalized recommendations:\n")

user_age = input("1. Your Age: ")
user_ped = input("2. Pre-existing Conditions (comma-separated, or 'None'): ")
user_budget = input("3. Budget Range (e.g., '15000-25000' per year): ")
user_needs = input("4. Specific Needs (e.g., maternity, OPD, no room rent limit): ")
user_preferences = input("5. Preferred Features (e.g., wellness rewards, quick claim settlement): ")

user_profile = {
    'age': user_age,
    'pre_existing_conditions': user_ped,
    'budget': user_budget,
    'specific_needs': user_needs,
    'preferences': user_preferences
}

print("\n✅ User profile collected successfully!")

# Create insurance context (simplified)
def create_insurance_context():
    context = "AVAILABLE HEALTH INSURANCE PLANS:\n\n"
    
    for insurer in insurers:
        context += f"\n{'='*50}\n"
        context += f"INSURER: {insurer['insurer_name']}\n"
        context += f"CSR: {insurer['claim_settlement_ratio']['csr_percentage']}\n"
        
        for plan in insurer['plans']:
            context += f"\n--- {plan['plan_name']} ---\n"
            coverage = plan['coverage_static']
            waiting = plan['waiting_periods']
            
            context += f"Sum Insured: {coverage.get('sum_insured_options', 'N/A')}\n"
            context += f"Room Rent: {coverage.get('room_rent_limit', 'N/A')}\n"
            context += f"NCB: {coverage.get('no_claim_bonus', 'N/A')}\n"
            context += f"Maternity: {coverage.get('maternity_coverage', 'N/A')}\n"
            context += f"OPD: {coverage.get('opd_coverage', 'N/A')}\n"
            context += f"PED Waiting: {waiting.get('ped_waiting_months', 'N/A')} months\n"
            context += f"Key Features: {', '.join(plan.get('key_features', [])[:3])}\n"
    
    return context

insurance_context = create_insurance_context()
print(f"✅ Created insurance context")

# Define Tasks
profile_task = Task(
    description=f"""Analyze this user and list their key insurance needs:
    Age: {user_profile['age']}, PED: {user_profile['pre_existing_conditions']}, 
    Budget: {user_profile['budget']}, Needs: {user_profile['specific_needs']}""",
    agent=user_profiler,
    expected_output="User needs profile with priorities"
)

recommend_task = Task(
    description=f"""Based on user needs, recommend TOP 3 insurance plans from:
    {insurance_context[:2000]}  
    
    Output format: Plan Name | Insurer | Why Recommended""",
    agent=recommendation_agent,
    expected_output="Top 3 ranked plans with reasoning",
    context=[profile_task]
)

compare_task = Task(
    description="""Create a comparison table of the 3 recommended plans with brief reasoning.""",
    agent=comparison_agent,
    expected_output="Comparison table with reasoning",
    context=[profile_task, recommend_task]
)

print("✅ Created tasks")

# Run the crew
print("\n" + "="*60)
print("ANALYZING... This will take 2-3 minutes")
print("="*60 + "\n")

crew = Crew(
    agents=[user_profiler, recommendation_agent, comparison_agent],
    tasks=[profile_task, recommend_task, compare_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()

print("\n" + "="*60)
print("📊 RECOMMENDATIONS:")
print("="*60)
print(result)
print("\n✅ Complete!")
