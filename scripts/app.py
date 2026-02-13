import streamlit as st
import json
import os
import pandas as pd
from crewai import Agent, Task, Crew, Process
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Health Insurance Recommender",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .recommendation-card {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
    }
    </style>
""", unsafe_allow_html=True)

# Configure Ollama via environment variables
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3.2"
os.environ["OPENAI_API_KEY"] = "ollama"

# Load insurance data
@st.cache_data
def load_insurance_data():
    with open('data/indian_health_insurance_data.json', 'r') as f:
        return json.load(f)

insurance_data = load_insurance_data()
insurers = insurance_data['insurers']

# Create insurance context
@st.cache_data
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

# Create agents (cached to avoid recreation)
@st.cache_resource
def create_agents():
    user_profiler = Agent(
        role='Health Insurance Needs Analyst',
        goal='Analyze user requirements and create a comprehensive profile',
        backstory="""Expert health insurance analyst specializing in understanding 
        customer needs based on age, health conditions, budget, and preferences.""",
        verbose=True,
        allow_delegation=False
    )
    
    recommendation_agent = Agent(
        role='Insurance Plan Matcher',
        goal='Analyze plans and rank top 3 matches for user profile',
        backstory="""Experienced insurance matcher with deep knowledge of Indian 
        health insurance, analyzing features, waiting periods, and benefits.""",
        verbose=True,
        allow_delegation=False
    )
    
    comparison_agent = Agent(
        role='Insurance Comparison Specialist',
        goal='Create detailed comparison with clear reasoning',
        backstory="""Expert at breaking down complex insurance features into 
        simple comparisons with clear reasoning for recommendations.""",
        verbose=True,
        allow_delegation=False
    )
    
    return user_profiler, recommendation_agent, comparison_agent

# Main app
def main():
    # Header
    st.title("🏥 Health Insurance Recommendation System")
    st.markdown("### AI-Powered Personalized Insurance Recommendations")
    st.markdown("---")
    
    # Sidebar with info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This AI system analyzes **9 insurance plans** from **6 major insurers** 
        and provides personalized recommendations using advanced AI agents.
        
        **Insurers Covered:**
        - Star Health Insurance
        - HDFC ERGO
        - ICICI Lombard
        - Niva Bupa
        - Care Health Insurance
        - Aditya Birla Health Insurance
        """)
        
        st.markdown("---")
        st.header("🤖 AI Agents")
        st.markdown("""
        1. **Profiler**: Analyzes your needs
        2. **Matcher**: Finds best plans
        3. **Comparator**: Creates comparison
        """)
        
        st.markdown("---")
        st.markdown("**Powered by:** CrewAI + Ollama")
    
    # Main content in tabs
    tab1, tab2 = st.tabs(["📝 Get Recommendations", "🎯 Demo Profiles"])
    
    with tab1:
        st.header("Enter Your Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Your Age", min_value=18, max_value=100, value=28, step=1)
            ped = st.text_input("Pre-existing Conditions", 
                               placeholder="e.g., Diabetes, Hypertension or 'None'",
                               value="None")
            budget = st.text_input("Budget Range (₹/year)", 
                                  placeholder="e.g., 15000-20000",
                                  value="15000-20000")
        
        with col2:
            needs = st.text_area("Specific Needs", 
                                placeholder="e.g., Maternity, OPD, No room rent limit",
                                value="No room rent limit, Good claim settlement")
            preferences = st.text_area("Preferred Features", 
                                      placeholder="e.g., Wellness rewards, Quick claim settlement",
                                      value="Wellness rewards, Digital experience")
        
        st.markdown("---")
        
        # Generate button
        if st.button("🚀 Generate Recommendations", type="primary"):
            with st.spinner("🤖 AI Agents are analyzing insurance plans... This may take 2-3 minutes"):
                try:
                    # Create user profile
                    user_profile = {
                        'age': str(age),
                        'pre_existing_conditions': ped,
                        'budget': budget,
                        'specific_needs': needs,
                        'preferences': preferences
                    }
                    
                    # Display user profile
                    st.success("✅ User profile received!")
                    with st.expander("View Your Profile"):
                        st.json(user_profile)
                    
                    # Get agents
                    user_profiler, recommendation_agent, comparison_agent = create_agents()
                    insurance_context = create_insurance_context()
                    
                    # Create tasks
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
                    
                    # Create and run crew
                    crew = Crew(
                        agents=[user_profiler, recommendation_agent, comparison_agent],
                        tasks=[profile_task, recommend_task, compare_task],
                        process=Process.sequential,
                        verbose=False  # Set to False for cleaner Streamlit output
                    )
                    
                    result = crew.kickoff()
                    
                    # Display results
                    st.markdown("---")
                    st.header("📊 Recommendations")
                    
                    # Display the result
                    st.markdown(result)
                    
                    st.success("✅ Analysis Complete!")
                    
                    # Download option
                    st.download_button(
                        label="📥 Download Recommendations",
                        data=str(result),
                        file_name="insurance_recommendations.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("Make sure Ollama is running with llama3.2 model: `ollama serve`")
    
    with tab2:
        st.header("🎯 Pre-configured Demo Profiles")
        st.markdown("Try these example profiles to see how the system works:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-box">
            <h4>👨‍💼 Young Professional</h4>
            <ul>
                <li><b>Age:</b> 28</li>
                <li><b>PED:</b> None</li>
                <li><b>Budget:</b> ₹10,000-15,000</li>
                <li><b>Needs:</b> No room rent limit</li>
                <li><b>Preferences:</b> Wellness rewards</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
            <h4>👨‍👩‍👧‍👦 Family with Kids</h4>
            <ul>
                <li><b>Age:</b> 35</li>
                <li><b>PED:</b> None</li>
                <li><b>Budget:</b> ₹20,000-30,000</li>
                <li><b>Needs:</b> Maternity, Family floater</li>
                <li><b>Preferences:</b> Large hospital network</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="info-box">
            <h4>👴 Senior Citizen</h4>
            <ul>
                <li><b>Age:</b> 62</li>
                <li><b>PED:</b> Diabetes, Hypertension</li>
                <li><b>Budget:</b> ₹30,000-50,000</li>
                <li><b>Needs:</b> Short PED waiting</li>
                <li><b>Preferences:</b> Premium features</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("💡 Tip: Copy these values to the 'Get Recommendations' tab to test!")

if __name__ == "__main__":
    main()
