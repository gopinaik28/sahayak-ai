"""
One-time Setup Script for RAG Vector Database

This script:
1. Loads insurance data from JSON
2. Creates chunks for each plan
3. Generates embeddings using Ollama
4. Stores in ChromaDB

Run this once before starting the backend server:
    python setup_embeddings.py
"""

from rag_engine import RAGEngine
import sys


def main():
    print("="*70)
    print("  RAG Vector Database Setup")
    print("="*70)
    print()
    print("This will create embeddings for all insurance plans")
    print("and store them in ChromaDB for semantic search.")
    print()
    print("Requirements:")
    print("  ✓ Ollama must be running")
    print("  ✓ nomic-embed-text model must be pulled")
    print()
    print("="*70)
    print()
    
    try:
        # Initialize RAG engine
        rag = RAGEngine()
        
        # Setup vector database
        rag.setup_vector_database()
        
        print()
        print("="*70)
        print("  ✅ SUCCESS!")
        print("="*70)
        print()
        print("Vector database created at: ./chroma_db/")
        print("You can now start the backend server with RAG enabled.")
        print()
        
        # Optional: Test semantic search
        print("Testing semantic search...")
        test_query = "I need maternity coverage with good CSR"
        results = rag.semantic_search(test_query, top_k=3)
        
        print(f"\n🔍 Test Query: '{test_query}'")
        print("\nTop 3 Results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['metadata']['plan_name']} - {result['metadata']['insurer']}")
            print(f"     Similarity: {result['similarity']:.2%}")
        
        print("\n✨ RAG system is ready to use!")
        
    except Exception as e:
        print()
        print("="*70)
        print("  ❌ ERROR")
        print("="*70)
        print()
        print(f"Failed to setup vector database: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Make sure Ollama is running: ollama serve")
        print("  2. Make sure model is pulled: ollama pull nomic-embed-text")
        print("  3. Check that data/indian_health_insurance_data.json exists")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
