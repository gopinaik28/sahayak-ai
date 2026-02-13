"""
RAG Engine for Health Insurance Recommendations

This module handles:
- Chunking insurance data into meaningful pieces
- Generating embeddings using Ollama
- Storing embeddings in ChromaDB vector database
- Semantic search for retrieving relevant plans
"""

import chromadb
from chromadb.config import Settings
import ollama
import json
import os
from typing import List, Dict, Any


class RAGEngine:
    """RAG Engine for semantic search of insurance plans"""
    
    def __init__(self, data_path: str = "data/indian_health_insurance_data.json"):
        """
        Initialize RAG Engine
        
        Args:
            data_path: Path to insurance data JSON file
        """
        self.data_path = data_path
        self.embedding_model = "nomic-embed-text"
        
        # Initialize ChromaDB with persistent storage
        self.client = chromadb.PersistentClient(path="./rag/chroma_db")
        
        # Try to get existing collection or create new one
        try:
            self.collection = self.client.get_collection(name="insurance_plans")
            print("✅ Loaded existing vector database")
        except:
            self.collection = None
            print("⚠️  No existing vector database found")
    
    def load_insurance_data(self) -> Dict[str, Any]:
        """Load insurance data from JSON file"""
        with open(self.data_path, 'r') as f:
            return json.load(f)
    
    def chunk_insurance_data(self) -> List[Dict[str, Any]]:
        """
        Create chunks from insurance data
        Each chunk = 1 complete plan with all details
        
        Returns:
            List of chunks with metadata
        """
        data = self.load_insurance_data()
        chunks = []
        
        for insurer in data['insurers']:
            insurer_name = insurer['insurer_name']
            csr = insurer['claim_settlement_ratio']['csr_percentage']
            
            for plan in insurer['plans']:
                plan_name = plan['plan_name']
                coverage = plan['coverage_static']
                waiting = plan['waiting_periods']
                features = plan.get('key_features', [])
                
                # Create comprehensive text for this plan
                chunk_text = f"""
                Plan Name: {plan_name}
                Insurance Company: {insurer_name}
                Claim Settlement Ratio: {csr}%
                
                Coverage Details:
                - Sum Insured Options: {coverage.get('sum_insured_options', 'N/A')}
                - Room Rent Limit: {coverage.get('room_rent_limit', 'N/A')}
                - No Claim Bonus: {coverage.get('no_claim_bonus', 'N/A')}
                - Maternity Coverage: {coverage.get('maternity_coverage', 'Not available')}
                - OPD Coverage: {coverage.get('opd_coverage', 'Not available')}
                - Pre-existing Disease Waiting: {waiting.get('ped_waiting_months', 'N/A')} months
                - Initial Waiting: {waiting.get('initial_waiting_days', 'N/A')} days
                
                Key Features: {', '.join(features)}
                
                Premium Estimate: ₹10,000 - ₹25,000 per year (varies by age and sum insured)
                
                Best For: {self._determine_best_for(coverage, features, waiting)}
                """.strip()
                
                chunks.append({
                    'text': chunk_text,
                    'metadata': {
                        'plan_name': plan_name,
                        'insurer': insurer_name,
                        'csr': csr,
                        'has_maternity': 'maternity' in chunk_text.lower(),
                        'has_opd': coverage.get('opd_coverage', 'Not available') != 'Not available',
                        'ped_waiting': waiting.get('ped_waiting_months', 0)
                    }
                })
        
        return chunks
    
    def _determine_best_for(self, coverage: Dict, features: List, waiting: Dict) -> str:
        """Determine what type of users this plan is best for"""
        best_for = []
        
        if coverage.get('maternity_coverage') and coverage['maternity_coverage'] != 'Not available':
            best_for.append("families planning pregnancy")
        
        if coverage.get('room_rent_limit') == 'No Limit':
            best_for.append("those wanting flexibility in hospital room choice")
        
        if waiting.get('ped_waiting_months', 48) <= 24:
            best_for.append("people with pre-existing conditions")
        
        if coverage.get('opd_coverage') and coverage['opd_coverage'] != 'Not available':
            best_for.append("those needing regular doctor visits")
        
        if not best_for:
            best_for.append("general health coverage")
        
        return ", ".join(best_for)
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using Ollama
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector
        """
        try:
            response = ollama.embeddings(
                model=self.embedding_model,
                prompt=text
            )
            return response["embedding"]
        except Exception as e:
            print(f"❌ Error generating embedding: {e}")
            raise
    
    def setup_vector_database(self) -> None:
        """
        One-time setup: Create embeddings and store in ChromaDB
        """
        print("🚀 Setting up vector database...")
        
        # Delete existing collection if it exists
        try:
            self.client.delete_collection(name="insurance_plans")
            print("🗑️  Deleted old collection")
        except:
            pass
        
        # Create new collection
        self.collection = self.client.create_collection(
            name="insurance_plans",
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        # Get chunks
        chunks = self.chunk_insurance_data()
        print(f"📦 Created {len(chunks)} plan chunks")
        
        # Generate embeddings and store
        print("🧠 Generating embeddings...")
        for i, chunk in enumerate(chunks):
            embedding = self.generate_embedding(chunk['text'])
            
            self.collection.add(
                embeddings=[embedding],
                documents=[chunk['text']],
                metadatas=[chunk['metadata']],
                ids=[f"plan_{i}"]
            )
            print(f"  ✓ Embedded: {chunk['metadata']['plan_name']}")
        
        print(f"\n✅ Vector database ready! {len(chunks)} plans embedded.")
    
    def semantic_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for most relevant insurance plans
        
        Args:
            query: User query (natural language)
            top_k: Number of results to return
            
        Returns:
            List of relevant plan chunks with metadata
        """
        if not self.collection:
            raise ValueError("Vector database not initialized. Run setup_vector_database() first.")
        
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        # Search in vector database
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        relevant_plans = []
        for i in range(len(results['documents'][0])):
            relevant_plans.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'similarity': 1 - results['distances'][0][i]  # Convert distance to similarity
            })
        
        return relevant_plans
    
    def get_relevant_context(self, user_profile: Dict[str, str], top_k: int = 3) -> str:
        """
        Get relevant plan context for user profile
        
        Args:
            user_profile: Dict with age, ped, budget, needs, preferences
            top_k: Number of plans to retrieve
            
        Returns:
            Formatted context string for LLM
        """
        # Create semantic query from user profile
        query = f"""
        User Profile:
        - Age: {user_profile.get('age')} years
        - Pre-existing Conditions: {user_profile.get('ped', 'None')}
        - Budget: ₹{user_profile.get('budget')} per year
        - Specific Needs: {user_profile.get('needs', '')}
        - Preferences: {user_profile.get('preferences', '')}
        
        Find insurance plans that match these requirements.
        """.strip()
        
        # Perform semantic search
        relevant_plans = self.semantic_search(query, top_k=top_k)
        
        # Format context
        context = "RELEVANT INSURANCE PLANS (Based on semantic search):\n\n"
        for i, plan in enumerate(relevant_plans, 1):
            context += f"{'='*60}\n"
            context += f"PLAN {i} (Relevance: {plan['similarity']:.2%})\n"
            context += f"{'='*60}\n"
            context += plan['text'] + "\n\n"
        
        return context


if __name__ == "__main__":
    # Test the RAG engine
    rag = RAGEngine()
    
    # Setup (only needed once)
    print("Setting up vector database...")
    rag.setup_vector_database()
    
    # Test semantic search
    print("\n" + "="*60)
    print("Testing Semantic Search")
    print("="*60)
    
    test_queries = [
        "I need maternity coverage",
        "I have diabetes, need coverage with low waiting period",
        "Low budget plan under 15000 rupees"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        results = rag.semantic_search(query, top_k=2)
        for result in results:
            print(f"  ✓ {result['metadata']['plan_name']} ({result['similarity']:.2%} match)")
