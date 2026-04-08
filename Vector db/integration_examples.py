"""
Integration Example - Using Vector Database in Your Code
Shows how to use the vector database in your Python applications

This file demonstrates:
1. Loading the database programmatically
2. Creating custom search functions
3. Building simple applications on top
4. Integration with other systems
"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import json

# ============================================================================
# BASIC INTEGRATION EXAMPLE
# ============================================================================

class TamilVersesSearcher:
    """
    A reusable class for searching Tamil verses
    
    Example usage:
        searcher = TamilVersesSearcher()
        results = searcher.search("righteousness")
        for result in results:
            print(result)
    """
    
    def __init__(self, db_path: str = r"D:\projects\Vector db\chroma_db"):
        """
        Initialize the searcher
        
        Parameters:
        -----------
        db_path : str
            Path to ChromaDB database
        """
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_collection(name="tamil_literature")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search for verses related to query
        
        Parameters:
        -----------
        query : str
            Search query
        num_results : int
            Number of results to return
        
        Returns:
        --------
        list of dict : Search results with texts, meanings, and similarity scores
        """
        # Generate embedding for query
        query_embedding = self.model.encode(query)
        
        # Query database
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=num_results,
            include=['metadatas', 'documents', 'distances']
        )
        
        # Format results
        formatted_results = []
        
        ids = results['ids'][0]
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]
        
        for doc_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
            # Convert distance to similarity percentage
            similarity_percent = (1 - (distance / 2)) * 100
            
            formatted_results.append({
                'id': doc_id,
                'verse': document,
                'source': metadata.get('source'),
                'verse_number': metadata.get('verse_num'),
                'chapter': metadata.get('chapter'),
                'similarity': similarity_percent
            })
        
        return formatted_results


# ============================================================================
# USAGE EXAMPLE 1: Simple Search
# ============================================================================

def example_simple_search():
    """
    Example 1: Basic search functionality
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple Search")
    print("="*80)
    
    searcher = TamilVersesSearcher()
    
    query = "knowledge and learning"
    print(f"\nSearching for: '{query}'")
    print("-"*80)
    
    results = searcher.search(query, num_results=3)
    
    for i, result in enumerate(results, 1):
        print(f"\n#{i} - Similarity: {result['similarity']:.1f}%")
        print(f"    Source: {result['source']} (Verse {result['verse_number']})")
        print(f"    Verse: {result['verse']}")


# ============================================================================
# USAGE EXAMPLE 2: Theme-Based Search
# ============================================================================

def example_theme_search():
    """
    Example 2: Search for verses about specific themes
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Theme-Based Search")
    print("="*80)
    
    searcher = TamilVersesSearcher()
    
    themes = {
        'Virtue & Ethics': 'righteousness moral duty ethics',
        'Self-Control': 'controlling anger emotions desires',
        'Generosity': 'giving charity generosity compassion',
        'Knowledge': 'learning wisdom knowledge education',
    }
    
    for theme_name, theme_query in themes.items():
        results = searcher.search(theme_query, num_results=1)
        print(f"\n{theme_name}:")
        print(f"  Query: '{theme_query}'")
        if results:
            result = results[0]
            print(f"  Top match (Similarity: {result['similarity']:.0f}%): {result['verse'][:60]}...")


# ============================================================================
# USAGE EXAMPLE 3: Batch Processing
# ============================================================================

def example_batch_search(queries: List[str]):
    """
    Example 3: Search multiple queries and collect results
    
    Parameters:
    -----------
    queries : list of str
        Multiple search queries
    
    Returns:
    --------
    dict : Results organized by query
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Batch Processing Multiple Queries")
    print("="*80)
    
    searcher = TamilVersesSearcher()
    all_results = {}
    
    for query in queries:
        print(f"\n🔍 Processing: '{query}'")
        results = searcher.search(query, num_results=2)
        all_results[query] = results
        print(f"   ✓ Found {len(results)} results")
    
    # Display summary
    print("\n" + "-"*80)
    print("SUMMARY:")
    print("-"*80)
    for query, results in all_results.items():
        print(f"\n{query}:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. [{result['similarity']:.0f}%] {result['verse'][:50]}...")
    
    return all_results


# ============================================================================
# USAGE EXAMPLE 4: Filter by Source
# ============================================================================

def example_filter_by_source():
    """
    Example 4: Search and filter by source (Thirukural vs Aathichoodi)
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Filter Results by Source")
    print("="*80)
    
    searcher = TamilVersesSearcher()
    
    query = "righteousness"
    results = searcher.search(query, num_results=10)
    
    # Group by source
    by_source = {}
    for result in results:
        source = result['source']
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(result)
    
    # Display grouped results
    for source, source_results in by_source.items():
        print(f"\n{source} ({len(source_results)} results):")
        for result in source_results:
            print(f"  • [{result['similarity']:.0f}%] {result['verse'][:60]}...")


# ============================================================================
# USAGE EXAMPLE 5: Custom Application - QA System
# ============================================================================

class SimpleTamilQA:
    """
    A simple Question-Answer system using the vector database
    
    Example:
        qa = SimpleTamilQA()
        answer = qa.answer_question("What is the importance of knowledge?")
        print(answer)
    """
    
    def __init__(self):
        """Initialize QA system"""
        self.searcher = TamilVersesSearcher()
    
    def answer_question(self, question: str) -> str:
        """
        Find relevant verses that answer the question
        
        Parameters:
        -----------
        question : str
            Question in natural language
        
        Returns:
        --------
        str : Formatted answer with relevant verses
        """
        # Search for relevant verses
        results = self.searcher.search(question, num_results=3)
        
        if not results:
            return "No relevant verses found."
        
        # Format answer
        answer = f"Question: {question}\n\nRelevant Verses:\n"
        
        for i, result in enumerate(results, 1):
            answer += f"\n{i}. (Similarity: {result['similarity']:.0f}%)\n"
            answer += f"   Verse: {result['verse']}\n"
            answer += f"   Source: {result['source']} #{result['verse_number']}\n"
        
        return answer


def example_qa_system():
    """
    Example 5: Simple QA system
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Simple QA System")
    print("="*80)
    
    qa = SimpleTamilQA()
    
    questions = [
        "What is the importance of righteousness?",
        "How should one control their anger?",
        "Why is education important?",
    ]
    
    for question in questions:
        print("\n" + "-"*80)
        answer = qa.answer_question(question)
        print(answer)


# ============================================================================
# USAGE EXAMPLE 6: Integration Function Template
# ============================================================================

def integrate_into_flask_app():
    """
    Template: How to integrate into a Flask web application
    
    This shows the pattern to use in a Flask app:
    """
    code = '''
from flask import Flask, request, jsonify
from search_integration import TamilVersesSearcher

app = Flask(__name__)
searcher = TamilVersesSearcher()

@app.route('/api/search', methods=['GET'])
def search_verses():
    """API endpoint for searching verses"""
    query = request.args.get('q', '')
    results_count = request.args.get('n', 5, type=int)
    
    if not query:
        return jsonify({'error': 'Query required'}), 400
    
    results = searcher.search(query, num_results=results_count)
    
    return jsonify({
        'query': query,
        'results_count': len(results),
        'results': results
    })

if __name__ == '__main__':
    app.run(debug=True)
'''
    
    print("\n" + "="*80)
    print("EXAMPLE 6: Flask Integration Template")
    print("="*80)
    print(code)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all examples"""
    
    print("\n" + "="*80)
    print("VECTOR DATABASE INTEGRATION EXAMPLES")
    print("="*80)
    print("\nThese examples show how to use the vector database in your own code.")
    print("Uncomment the examples you want to run below.\n")
    
    try:
        # Uncomment the examples you want to run:
        
        # Example 1: Simple search
        example_simple_search()
        
        # Example 2: Theme-based search
        example_theme_search()
        
        # Example 3: Batch processing
        batch_queries = [
            "peace and tranquility",
            "duty and responsibility",
            "friendship and friendship"
        ]
        example_batch_search(batch_queries)
        
        # Example 4: Filter by source
        example_filter_by_source()
        
        # Example 5: QA System
        example_qa_system()
        
        # Example 6: Flask integration (just shows code)
        integrate_into_flask_app()
        
        print("\n" + "="*80)
        print("✓ All examples completed!")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
