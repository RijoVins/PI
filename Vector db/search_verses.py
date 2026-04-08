"""
Semantic Search Script for Tamil Literature Vector Database
Perform searches on the stored embeddings using natural language queries

Author: Vector DB Setup
Date: 2026
"""

import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import argparse
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

CHROMA_DB_DIR = r"D:\projects\Vector db\chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "tamil_literature"

# ============================================================================
# SEARCH FUNCTIONS
# ============================================================================

def initialize_search_components():
    """
    Initialize ChromaDB client and embedding model for searching
    
    Returns:
    --------
    tuple: (chromadb_client, sentence_transformer_model, collection)
    """
    print("\n🔄 Initializing search components...")
    
    try:
        # Initialize ChromaDB client
        if not Path(CHROMA_DB_DIR).exists():
            print(f"\n✗ Error: Database not found at {CHROMA_DB_DIR}")
            print("   Please run 'setup_vector_db.py' first to create the database.")
            raise FileNotFoundError("ChromaDB database not found")
        
        client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        print("   ✓ ChromaDB client initialized")
        
        # Get the collection
        try:
            collection = client.get_collection(name=COLLECTION_NAME)
            print(f"   ✓ Collection '{COLLECTION_NAME}' loaded")
            print(f"   ✓ Collection contains {collection.count()} documents")
        except Exception as e:
            print(f"   ✗ Collection not found: {e}")
            print("   Please run 'setup_vector_db.py' first.")
            raise
        
        # Initialize embedding model
        print(f"   Loading embedding model: {EMBEDDING_MODEL}...")
        model = SentenceTransformer(EMBEDDING_MODEL)
        print("   ✓ Embedding model loaded")
        
        return client, model, collection
    
    except Exception as e:
        print(f"✗ Error initializing search: {e}")
        raise


def semantic_search(query, collection, model, num_results=5):
    """
    Perform semantic search on the vector database
    
    Parameters:
    -----------
    query : str
        Search query in natural language
    collection : chromadb.api.models.Collection
        ChromaDB collection to search
    model : SentenceTransformer
        Embedding model for query embedding
    num_results : int
        Number of results to return
    
    Returns:
    --------
    dict: Search results with documents and their similarity scores
    """
    print(f"\n🔍 Searching for: '{query}'")
    print(f"   Returning top {num_results} results...\n")
    
    try:
        # Step 1: Convert query to embedding
        query_embedding = model.encode(query)
        
        # Step 2: Query ChromaDB for similar documents
        # distance: False returns distances (smaller = more similar)
        # include: ['embeddings', 'metadatas', 'documents', 'distances']
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=num_results,
            include=['embeddings', 'metadatas', 'documents', 'distances']
        )
        
        # Step 3: Format and return results
        return results
    
    except Exception as e:
        print(f"✗ Error during search: {e}")
        raise


def display_search_results(results, query):
    """
    Display search results in a formatted manner
    
    Parameters:
    -----------
    results : dict
        Results from ChromaDB query
    query : str
        Original search query
    """
    print("="*80)
    print(f"SEARCH RESULTS FOR: '{query}'")
    print("="*80)
    
    if not results['ids'] or len(results['ids'][0]) == 0:
        print("\n❌ No results found.")
        return
    
    # ChromaDB returns batched results (list of lists)
    ids = results['ids'][0]
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]
    
    for idx, (doc_id, document, metadata, distance) in enumerate(
        zip(ids, documents, metadatas, distances)
    ):
        # Calculate similarity score (inverse of distance)
        # For cosine distance: 0 = identical, 2 = completely different
        # We convert to similarity: 1 - distance/2
        similarity_score = 1 - (distance / 2)
        similarity_percent = similarity_score * 100
        
        # Create visual similarity bar
        bar_length = int(similarity_percent / 5)
        similarity_bar = "█" * bar_length + "░" * (20 - bar_length)
        
        print(f"\n{'─'*80}")
        print(f"RESULT #{idx + 1}")
        print(f"{'─'*80}")
        print(f"ID: {doc_id}")
        print(f"Source: {metadata.get('source', 'Unknown')}")
        print(f"Verse Number: {metadata.get('verse_num', 'N/A')}")
        print(f"Chapter: {metadata.get('chapter', 'N/A')}")
        
        # Display similarity
        print(f"\n📊 Similarity: {similarity_percent:.1f}% [{similarity_bar}]")
        
        # Display the verse
        print(f"\n📖 Verse(Text):")
        print(f"   {document}")
        
        # If we have meaning metadata, display it
        if metadata.get('meaning'):
            print(f"\n💭 Meaning:")
            # Clean up the meaning text
            meaning_text = metadata.get('meaning', '')
            if meaning_text:
                # Wrap long text
                import textwrap
                wrapped = textwrap.fill(meaning_text, width=75, initial_indent='   ', subsequent_indent='   ')
                print(wrapped)
    
    print(f"\n{'='*80}")


def interactive_search(collection, model):
    """
    Interactive search mode - allows user to enter multiple queries
    
    Parameters:
    -----------
    collection : chromadb.api.models.Collection
        ChromaDB collection to search
    model : SentenceTransformer
        Embedding model for query embedding
    """
    print("\n" + "="*80)
    print("   INTERACTIVE SEARCH MODE")
    print("   (Type 'quit' or 'exit' to stop)")
    print("="*80)
    
    while True:
        try:
            print("\n" + "─"*80)
            query = input("\n🔍 Enter search query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                print("⚠ Empty query. Please enter a search term.")
                continue
            
            # Get number of results
            try:
                num_results = int(input("   Number of results (default 5): ") or "5")
                num_results = max(1, min(num_results, 20))  # Limit 1-20
            except ValueError:
                num_results = 5
            
            # Perform search
            results = semantic_search(query, collection, model, num_results)
            display_search_results(results, query)
        
        except KeyboardInterrupt:
            print("\n\n👋 Search interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n✗ Error during search: {e}")
            print("   Please try again.")


# ============================================================================
# EXAMPLE SEARCHES
# ============================================================================

def run_example_searches(collection, model):
    """
    Run predefined example searches to demonstrate the system
    
    Parameters:
    -----------
    collection : chromadb.api.models.Collection
        ChromaDB collection to search
    model : SentenceTransformer
        Embedding model for query embedding
    """
    
    # Define example searches
    example_queries = [
        "righteousness and morality",
        "controlling anger and emotions",
        "importance of learning and education",
        "poverty and generosity",
        "divine worship",
    ]
    
    print("\n" + "="*80)
    print("   EXAMPLE SEMANTIC SEARCHES")
    print("="*80)
    
    for i, query in enumerate(example_queries, 1):
        input_prompt = f"\n[Example {i}/{len(example_queries)}] Press Enter to see results for: '{query}'"
        print(input_prompt, end="")
        try:
            input()
        except KeyboardInterrupt:
            print("\n⚠ Examples interrupted.")
            break
        
        results = semantic_search(query, collection, model, num_results=3)
        display_search_results(results, query)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function: execute search interface
    """
    parser = argparse.ArgumentParser(
        description="Semantic search on Tamil literature vector database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search_verses.py                    # Interactive mode
  python search_verses.py --query "love and compassion"  # Single query
  python search_verses.py --examples        # Run example searches
  python search_verses.py --query "virtue" --results 10  # 10 results
        """
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Search query (single query mode)'
    )
    parser.add_argument(
        '--results', '-r',
        type=int,
        default=5,
        help='Number of results to return (default: 5)'
    )
    parser.add_argument(
        '--examples', '-e',
        action='store_true',
        help='Run example searches'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Interactive search mode (default if no --query)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("   TAMIL LITERATURE SEMANTIC SEARCH")
    print("="*80)
    
    try:
        # Initialize search components
        client, model, collection = initialize_search_components()
        
        # Determine which mode to run
        if args.query:
            # Single query mode
            results = semantic_search(args.query, collection, model, args.results)
            display_search_results(results, args.query)
        
        elif args.examples:
            # Example mode
            run_example_searches(collection, model)
        
        else:
            # Interactive mode (default)
            interactive_search(collection, model)
    
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user.")
        return False
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n✓ Search completed successfully!")
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
