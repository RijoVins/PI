"""
Vector Database Setup Script for Tamil Literature
This script loads CSV data, generates embeddings, and stores them in ChromaDB

Author: Vector DB Setup
Date: 2026
"""

import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import os
from pathlib import Path
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

# Paths to your CSV files
THIRUKURAL_CSV = r"D:\projects\Vector db\Thirukural DB\thirukkural_final.csv"
AATHICHOODI_CSV = r"D:\projects\Vector db\Aathichoodi\aathichoodi.csv"

# Directory to store ChromaDB database
CHROMA_DB_DIR = r"D:\projects\Vector db\chroma_db"

# Embedding model to use
# Options:
# - "all-mpnet-base-v2" (Most accurate, 768-dim, ~330MB) - RECOMMENDED
# - "all-MiniLM-L6-v2" (Faster, 384-dim, ~80MB) - Good for testing
# - "all-distilroberta-v1" (Fast, 768-dim, ~270MB)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ============================================================================
# STEP 1: LOAD CSV DATA
# ============================================================================

def load_thirukural_data():
    """
    Load Thirukural data from CSV
    
    Returns:
    --------
    list of dict: Each dict has 'text', 'meaning', and metadata
    """
    print("\n📚 Loading Thirukural data...")
    
    try:
        df = pd.read_csv(THIRUKURAL_CSV, encoding='utf-8')
        print(f"   ✓ Loaded {len(df)} verses")
        
        # Extract relevant columns
        # We'll combine verse text with one of the meanings for richer embedding
        documents = []
        
        for idx, row in df.iterrows():
            # Get verse number and text
            verse_num = str(row['குறள் எண்'])
            verse_text = str(row['குறள்'])
            
            # Get the first available meaning (we'll use Mu. Varadharasan's commentary)
            meaning = str(row['மு. வரதராசனார் உரை']) if pd.notna(row['மு. வரதராசனார் உரை']) else ""
            
            # Get chapter info for context
            paal = str(row['பால்']) if pd.notna(row['பால்']) else ""
            adhikaram = str(row['அதிகாரம்']) if pd.notna(row['அதிகாரம்']) else ""
            
            # Combine text and meaning for better embeddings
            # This way embeddings capture both literal meaning and interpretation
            combined_text = f"{verse_text} {meaning}"
            
            documents.append({
                'id': f"thirukural_{verse_num}",
                'text': verse_text,
                'meaning': meaning,
                'combined': combined_text,
                'chapter': adhikakaram,
                'section': paal,
                'source': 'Thirukural',
                'verse_num': verse_num
            })
        
        return documents
    
    except Exception as e:
        print(f"   ✗ Error loading Thirukural: {e}")
        return []


def load_aathichoodi_data():
    """
    Load Aathichoodi data from CSV
    
    Returns:
    --------
    list of dict: Each dict has 'text', 'meaning', and metadata
    """
    print("\n📚 Loading Aathichoodi data...")
    
    try:
        df = pd.read_csv(AATHICHOODI_CSV, encoding='utf-8')
        print(f"   ✓ Loaded {len(df)} verses")
        
        documents = []
        
        for idx, row in df.iterrows():
            # Get verse text and meaning
            verse_text = str(row['ஆத்திசூடி']) if pd.notna(row['ஆத்திசூடி']) else ""
            meaning = str(row['பொருள்']) if pd.notna(row['பொருள்']) else ""
            
            # Combine for better embeddings
            combined_text = f"{verse_text} {meaning}"
            
            documents.append({
                'id': f"aathichoodi_{idx+1}",
                'text': verse_text,
                'meaning': meaning,
                'combined': combined_text,
                'chapter': 'Aathichoodi',
                'section': 'Ethics',
                'source': 'Aathichoodi',
                'verse_num': str(idx + 1)
            })
        
        return documents
    
    except Exception as e:
        print(f"   ✗ Error loading Aathichoodi: {e}")
        return []


# ============================================================================
# STEP 2: GENERATE EMBEDDINGS
# ============================================================================

def initialize_embedding_model():
    """
    Initialize the sentence transformer model for generating embeddings
    
    Returns:
    --------
    SentenceTransformer: Loaded model ready to generate embeddings
    """
    print(f"\n🤖 Initializing embedding model: {EMBEDDING_MODEL}")
    print("   This may take 30-60 seconds on first run (downloading model)...")
    
    try:
        model = SentenceTransformer(EMBEDDING_MODEL)
        print("   ✓ Model loaded successfully")
        return model
    except Exception as e:
        print(f"   ✗ Error loading model: {e}")
        raise


def generate_embeddings(documents, model, batch_size=32):
    """
    Generate embeddings for documents using the sentence transformer model
    
    Parameters:
    -----------
    documents : list of dict
        Documents to generate embeddings for
    model : SentenceTransformer
        The embedding model
    batch_size : int
        Number of documents to process at once (for memory efficiency)
    
    Returns:
    --------
    list of list: Embeddings (vectors) for each document
    """
    print(f"\n⚡ Generating embeddings for {len(documents)} documents...")
    print(f"   Using batch size: {batch_size}")
    
    # Extract the combined text (verse + meaning) for embedding
    texts_to_embed = [doc['combined'] for doc in documents]
    
    try:
        # Generate embeddings
        embeddings = model.encode(texts_to_embed, batch_size=batch_size, show_progress_bar=True)
        print(f"   ✓ Generated {len(embeddings)} embeddings")
        print(f"   Embedding dimension: {len(embeddings[0])} dimensions")
        
        return embeddings
    except Exception as e:
        print(f"   ✗ Error generating embeddings: {e}")
        raise


# ============================================================================
# STEP 3: INITIALIZE CHROMADB AND STORE EMBEDDINGS
# ============================================================================

def initialize_chromadb():
    """
    Initialize and return a ChromaDB client
    
    Returns:
    --------
    chromadb.client.Client: ChromaDB client instance
    """
    print(f"\n💾 Initializing ChromaDB...")
    print(f"   Database path: {CHROMA_DB_DIR}")
    
    # Create directory if it doesn't exist
    Path(CHROMA_DB_DIR).mkdir(parents=True, exist_ok=True)
    
    try:
        # Initialize persistent ChromaDB client
        # This creates a local SQLite database that persists between runs
        client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        print("   ✓ ChromaDB initialized")
        
        return client
    except Exception as e:
        print(f"   ✗ Error initializing ChromaDB: {e}")
        raise


def store_embeddings_in_chromadb(client, documents, embeddings, collection_name="tamil_literature"):
    """
    Store documents and their embeddings in ChromaDB
    
    Parameters:
    -----------
    client : chromadb.client.Client
        ChromaDB client
    documents : list of dict
        Original documents with metadata
    embeddings : list of list
        Generated embeddings
    collection_name : str
        Name of the collection in ChromaDB
    
    Returns:
    --------
    chromadb.api.models.Collection: The collection object
    """
    print(f"\n📦 Storing embeddings in ChromaDB collection: '{collection_name}'")
    
    try:
        # Get or create collection
        # If collection already exists, data will be added/updated
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine distance for similarity
        )
        
        # Prepare data for storing
        ids = [doc['id'] for doc in documents]
        
        # Prepare metadatas (ChromaDB stores JSON-compatible metadata)
        metadatas = []
        for doc in documents:
            metadatas.append({
                'source': doc['source'],
                'verse_num': doc['verse_num'],
                'chapter': doc['chapter'],
                'section': doc['section']
            })
        
        # Prepare documents for storage (the readable text)
        texts = [doc['text'] for doc in documents]
        
        # Prepare meanings
        meanings = [doc['meaning'] for doc in documents]
        
        # Add to ChromaDB collection
        # embeddings: The vector representations
        # metadatas: Additional searchable information
        # documents: The original text for display
        # ids: Unique identifiers
        collection.add(
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            documents=texts,
            ids=ids
        )
        
        print(f"   ✓ Stored {len(documents)} documents with embeddings")
        print(f"   Collection has {collection.count()} total documents")
        
        return collection
    
    except Exception as e:
        print(f"   ✗ Error storing embeddings: {e}")
        raise


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function: orchestrate the entire vector DB setup process
    """
    print("\n" + "="*70)
    print("   TAMIL LITERATURE VECTOR DATABASE SETUP")
    print("="*70)
    
    try:
        # Load data from both CSV files
        thirukural_docs = load_thirukural_data()
        aathichoodi_docs = load_aathichoodi_data()
        
        # Combine all documents
        all_documents = thirukural_docs + aathichoodi_docs
        total_docs = len(all_documents)
        
        print(f"\n✓ Total documents loaded: {total_docs}")
        print(f"  - Thirukural: {len(thirukural_docs)} verses")
        print(f"  - Aathichoodi: {len(aathichoodi_docs)} verses")
        
        if total_docs == 0:
            print("\n✗ No documents loaded. Check CSV file paths.")
            return False
        
        # Initialize embedding model
        model = initialize_embedding_model()
        
        # Generate embeddings
        embeddings = generate_embeddings(all_documents, model)
        
        # Initialize ChromaDB
        client = initialize_chromadb()
        
        # Store embeddings in ChromaDB
        collection = store_embeddings_in_chromadb(client, all_documents, embeddings)
        
        # Print success summary
        print("\n" + "="*70)
        print("   ✓ VECTOR DATABASE SETUP COMPLETED SUCCESSFULLY!")
        print("="*70)
        print(f"\n📊 Summary:")
        print(f"   • Total documents: {total_docs}")
        print(f"   • Embedding model: {EMBEDDING_MODEL}")
        print(f"   • Vector dimension: {len(embeddings[0])}")
        print(f"   • Database location: {CHROMA_DB_DIR}")
        print(f"\n🔍 Next step: Run 'search_verses.py' to perform semantic searches!")
        print(f"\nExample: python search_verses.py --query 'righteousness and morality'")
        
        return True
    
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrupted by user.")
        return False
    except Exception as e:
        print(f"\n✗ Fatal error during setup: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
